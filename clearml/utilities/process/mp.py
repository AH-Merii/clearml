import os
import pickle
import struct
import sys
from functools import partial
from multiprocessing import Process, Semaphore, Event as ProcessEvent
from threading import Thread, Event as TrEvent, RLock as ThreadRLock
from time import sleep, time
from types import TracebackType
from typing import List, Dict, Optional, Type, TYPE_CHECKING, Any

import psutil
from six.moves.queue import Empty, Queue as TrQueue

from ..py3_interop import AbstractContextManager

if TYPE_CHECKING:
    from ... import Task

try:
    from multiprocessing import SimpleQueue
except ImportError:
    from multiprocessing.queues import SimpleQueue

# Windows/MacOS compatibility
try:
    from multiprocessing.context import ForkContext  # noqa
except ImportError:
    ForkContext = None

# PY2 compatibility
try:
    from multiprocessing import get_context
except ImportError:

    def get_context(*args: Any, **kwargs: Any) -> module:  # noqa
        import multiprocessing

        return multiprocessing


class _ForkSafeThreadSyncObject(object):
    __process_lock = get_context("fork" if sys.platform == "linux" else "spawn").Lock()

    @classmethod
    def _inner_lock(cls) -> None:
        try:
            # let's agree that 90sec should be enough to get a lock on such a short protected piece of code.
            # if we failed, we have to assume some deadlock happened
            # (Python is not very safe with regrades to Process Locks)
            cls.__process_lock.acquire(block=True, timeout=90)
        except:  # noqa
            pass

    @classmethod
    def _inner_unlock(cls) -> None:
        try:
            cls.__process_lock.release()
        except:  # noqa
            # if we fail to release we might not have locked it in the first place (see timeout)
            pass

    def __init__(self, functor: callable) -> None:
        self._sync = None
        self._instance_pid = None
        self._functor = functor

    def _create(self) -> None:
        # this part is not atomic, and there is not a lot we can do about it.
        if self._instance_pid != os.getpid() or not self._sync:
            # Notice! This is NOT atomic, this means the first time accessed, two concurrent calls might
            # end up overwriting each others, object
            # even tough it sounds horrible, the worst case in our usage scenario
            # is the first call usage is not "atomic"

            # Notice the order! we first create the object and THEN update the pid,
            # this is so whatever happens we Never try to used the old (pre-forked copy) of the synchronization object
            try:
                self._inner_lock()

                # we have to check gain inside the protected locked area
                if self._instance_pid != os.getpid() or not self._sync:
                    self._sync = self._functor()
                    self._instance_pid = os.getpid()
            finally:
                self._inner_unlock()


class ForkSafeRLock(_ForkSafeThreadSyncObject):
    def __init__(self) -> None:
        super(ForkSafeRLock, self).__init__(ThreadRLock)

    def acquire(self, *args: Any, **kwargs: Any) -> bool:
        self._create()
        return self._sync.acquire(*args, **kwargs)

    def release(self, *args: Any, **kwargs: Any) -> Optional[None]:
        if self._sync is None:
            return None
        self._create()
        return self._sync.release(*args, **kwargs)

    def __enter__(self) -> "SingletonLock":
        """Return `self` upon entering the runtime context."""
        self.acquire()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Raise any exception triggered within the runtime context."""
        # Do whatever cleanup.
        self.release()

    def _is_owned(self) -> bool:
        self._create()
        return self._sync._is_owned()  # noqa


class ForkSemaphore(_ForkSafeThreadSyncObject):
    def __init__(self, value: int = 1) -> None:
        super(ForkSemaphore, self).__init__(functor=partial(Semaphore, value))

    def acquire(self, *args: Any, **kwargs: Any) -> Optional[bool]:
        try:
            self._create()
        except BaseException:  # noqa
            return None

        return self._sync.acquire(*args, **kwargs)

    def release(self, *args: Any, **kwargs: Any) -> Optional[None]:
        if self._sync is None:
            return None
        self._create()
        return self._sync.release(*args, **kwargs)

    def get_value(self) -> int:
        self._create()
        return self._sync.get_value()

    def __enter__(self) -> "SingletonLock":
        """Return `self` upon entering the runtime context."""
        self.acquire()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Raise any exception triggered within the runtime context."""
        # Do whatever cleanup.
        self.release()


class ForkEvent(_ForkSafeThreadSyncObject):
    def __init__(self) -> None:
        super(ForkEvent, self).__init__(TrEvent)

    def set(self) -> bool:
        self._create()
        return self._sync.set()

    def clear(self) -> None:
        if self._sync is None:
            return None
        self._create()
        return self._sync.clear()

    def is_set(self) -> bool:
        self._create()
        return self._sync.is_set()

    def wait(self, *args: Any, **kwargs: Any) -> bool:
        self._create()
        return self._sync.wait(*args, **kwargs)


class ForkQueue(_ForkSafeThreadSyncObject):
    def __init__(self) -> None:
        super(ForkQueue, self).__init__(TrQueue)

    def get(self, *args: Any, **kwargs: Any) -> Any:
        self._create()
        return self._sync.get(*args, **kwargs)

    def put(self, *args: Any, **kwargs: Any) -> None:
        self._create()
        return self._sync.put(*args, **kwargs)

    def empty(self) -> bool:
        if not self._sync:
            return True
        self._create()
        return self._sync.empty()

    def full(self) -> bool:
        if not self._sync:
            return False
        self._create()
        return self._sync.full()

    def close(self) -> None:
        if not self._sync:
            return
        self._create()
        return self._sync.close()


class ThreadCalls(object):
    def __init__(self) -> None:
        self._queue = ForkQueue()
        self._thread = Thread(target=self._worker)
        self._thread.daemon = True
        self._thread.start()

    def is_alive(self) -> bool:
        return bool(self._thread) and self._thread.is_alive()

    def apply_async(self, func: callable, args: Optional[List] = None) -> bool:
        if not func:
            return False
        self._queue.put((func, args))
        return True

    def close(self, timeout: float = 5.0) -> None:
        t = self._thread
        if not t:
            return
        try:
            # push something into queue so it knows this is the end
            self._queue.put(None)
            # wait fot thread it should not take long, so we have a 5 second timeout
            # the background thread itself is doing nothing but push into a queue, so it should not take long
            t.join(timeout=timeout)
        except BaseException:  # noqa
            pass
        # mark thread is done
        self._thread = None

    def _worker(self) -> None:
        while True:
            try:
                request = self._queue.get(block=True, timeout=1.0)
                if not request:
                    break
            except Empty:
                continue
            # noinspection PyBroadException
            try:
                if request[1] is not None:
                    request[0](*request[1])
                else:
                    request[0]()
            except Exception:
                pass
        self._thread = None


class SingletonThreadPool(object):
    __thread_pool = None
    __thread_pool_pid = None

    @classmethod
    def get(cls) -> ThreadCalls:
        if os.getpid() != cls.__thread_pool_pid:
            cls.__thread_pool = ThreadCalls()
            cls.__thread_pool_pid = os.getpid()
        return cls.__thread_pool

    @classmethod
    def clear(cls) -> None:
        if cls.__thread_pool:
            cls.__thread_pool.close()
        cls.__thread_pool = None
        cls.__thread_pool_pid = None

    @classmethod
    def is_active(cls) -> bool:
        return cls.__thread_pool and cls.__thread_pool_pid == os.getpid() and cls.__thread_pool.is_alive()


class SafeQueue(object):
    """
    Many writers Single Reader multiprocessing safe Queue
    """

    __thread_pool = SingletonThreadPool()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._reader_thread = None
        self._reader_thread_started = False
        # Fix the python Queue and Use SimpleQueue write so it uses a single OS write,
        # making it atomic message passing
        self._q = SimpleQueue(*args, **kwargs)

        # on Windows, queue communication is done via pipes, no need to override the _send_bytes method
        if sys.platform != "win32":
            # noinspection PyBroadException
            try:
                # noinspection PyUnresolvedReferences,PyProtectedMember
                self._q._writer._send_bytes = partial(SafeQueue._pipe_override_send_bytes, self._q._writer)
            except Exception:
                pass

        self._internal_q = None
        # Note we should Never! assign a new object to `self._q_size`, just work with the initial object
        self._q_size = []  # list of PIDs we pushed, so this is atomic.

    def empty(self) -> bool:
        return self._q.empty() and (not self._internal_q or self._internal_q.empty())

    def is_pending(self) -> bool:
        # check if we have pending requests to be pushed (it does not mean they were pulled)
        # only call from main put process
        return self._get_q_size_len() > 0

    def close(self, event: Optional["SafeEvent"], timeout: float = 3.0) -> None:
        # wait until all pending requests pushed
        tic = time()
        pid = os.getpid()
        prev_q_size = self._get_q_size_len(pid)
        while self.is_pending():
            if event:
                event.set()
            if not self.__thread_pool.is_active():
                break
            sleep(0.1)
            # timeout is for the maximum time to pull a single object from the queue,
            # this way if we get stuck we notice quickly and abort
            if timeout and (time() - tic) > timeout:
                if prev_q_size == self._get_q_size_len(pid):
                    break
                else:
                    prev_q_size = self._get_q_size_len(pid)
                    tic = time()

    def get(self, *args: Any, **kwargs: Any) -> Any:
        return self._get_internal_queue(*args, **kwargs)

    def batch_get(
        self,
        max_items: int = 1000,
        timeout: float = 0.2,
        throttle_sleep: float = 0.1,
    ) -> List[Any]:
        buffer = []
        timeout_count = int(timeout / throttle_sleep)
        empty_count = timeout_count
        while len(buffer) < max_items:
            while not self.empty() and len(buffer) < max_items:
                try:
                    buffer.append(self._get_internal_queue(block=False))
                    empty_count = 0
                except Empty:
                    break
            empty_count += 1
            if empty_count > timeout_count or len(buffer) >= max_items:
                break
            sleep(throttle_sleep)
        return buffer

    def put(self, obj: Any) -> None:
        # not atomic when forking for the first time
        # GIL will make sure it is atomic
        self._q_size.append(os.getpid())
        try:
            # make sure the block put is done in the thread pool i.e. in the background
            obj = pickle.dumps(obj)
            if BackgroundMonitor.get_at_exit_state():
                self._q_put(obj)
                return
            self.__thread_pool.get().apply_async(self._q_put, args=(obj, False))
        except:  # noqa
            pid = os.getpid()
            p = None
            while p != pid and self._q_size:
                p = self._q_size.pop()

    def _get_q_size_len(self, pid: Optional[int] = None) -> int:
        pid = pid or os.getpid()
        return len([p for p in self._q_size if p == pid])

    def _q_put(self, obj: Any, allow_raise: bool = True) -> None:
        # noinspection PyBroadException
        try:
            self._q.put(obj)
        except BaseException:
            # make sure we zero the _q_size of the process dies (i.e. queue put fails)
            self._q_size.clear()
            if allow_raise:
                raise
            return
        pid = os.getpid()
        # GIL will make sure it is atomic
        # pop the First "counter" that is ours (i.e. pid == os.getpid())
        p = None
        while p != pid and self._q_size:
            p = self._q_size.pop()

    def _init_reader_thread(self) -> None:
        if not self._internal_q:
            self._internal_q = ForkQueue()
        if not self._reader_thread or not self._reader_thread.is_alive():
            # read before we start the thread
            self._reader_thread = Thread(target=self._reader_daemon)
            self._reader_thread.daemon = True
            self._reader_thread.start()
            # if we have waiting results
            # wait until thread is up and pushed some results
            while not self._reader_thread_started:
                sleep(0.2)
            # just in case make sure we pulled some stuff if we had any
            # todo: wait until a queue is not empty, but for some reason that might fail
            sleep(1.0)

    def _get_internal_queue(self, *args: Any, **kwargs: Any) -> Any:
        self._init_reader_thread()
        obj = self._internal_q.get(*args, **kwargs)
        # deserialize
        return pickle.loads(obj)

    def _reader_daemon(self) -> None:
        self._reader_thread_started = True
        # pull from process queue and push into thread queue
        while True:
            # noinspection PyBroadException
            try:
                obj = self._q.get()
                if obj is None:
                    break
            except Exception:
                break
            self._internal_q.put(obj)

    @staticmethod
    def _pipe_override_send_bytes(self, buf: bytes) -> None:
        n = len(buf)
        # For wire compatibility with 3.2 and lower
        header = struct.pack("!i", n)
        # Issue #20540: concatenate before sending, to avoid delays due
        # to Nagle's algorithm on a TCP socket.
        # Also note we want to avoid sending a 0-length buffer separately,
        # to avoid "broken pipe" errors if the other end closed the pipe.
        self._send(header + buf)


class SafeEvent(object):
    __thread_pool = SingletonThreadPool()

    def __init__(self) -> None:
        self._event = ProcessEvent()

    def is_set(self) -> bool:
        return self._event.is_set()

    def set(self) -> None:
        if not BackgroundMonitor.is_subprocess_enabled() or BackgroundMonitor.is_subprocess_alive():
            self._event.set()
        # SafeEvent.__thread_pool.get().apply_async(func=self._event.set, args=())

    def clear(self) -> bool:
        return self._event.clear()

    def wait(self, timeout: Optional[float] = None) -> bool:
        return self._event.wait(timeout=timeout)


class SingletonLock(AbstractContextManager):
    _instances = []

    def __init__(self) -> None:
        self._lock = None
        SingletonLock._instances.append(self)

    def acquire(self, *args: Any, **kwargs: Any) -> bool:
        self.create()
        return self._lock.acquire(*args, **kwargs)

    def release(self, *args: Any, **kwargs: Any) -> Optional[bool]:
        if self._lock is None:
            return None
        return self._lock.release(*args, **kwargs)

    def create(self) -> None:
        if self._lock is None:
            self._lock = ForkSafeRLock()

    @classmethod
    def instantiate(cls) -> None:
        for i in cls._instances:
            i.create()

    def __enter__(self) -> "SingletonLock":
        """Return `self` upon entering the runtime context."""
        self.acquire()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Raise any exception triggered within the runtime context."""
        # Do whatever cleanup.
        self.release()


class BackgroundMonitor(object):
    # If we need multiple monitoring contexts (i.e. subprocesses) this will become a dict
    _main_process = None
    _main_process_proc_obj = None
    _main_process_task_id = None
    _parent_pid = None
    _sub_process_started = None
    _at_exit = False
    _instances: Dict[int, List["BackgroundMonitor"]] = {}

    def __init__(self, task: Any, wait_period: float, for_model: bool = False) -> None:
        self._event = ForkEvent()
        self._done_ev = ForkEvent()
        self._start_ev = ForkEvent()
        self._task_pid = os.getpid()
        self._thread = None
        self._thread_pid = None
        self._wait_timeout = wait_period
        self._subprocess = None if not for_model and task.is_main_task() else False
        self._task_id = task.id
        self._task_obj_id = id(task.id)

    def start(self) -> None:
        if not self._thread:
            self._thread = True
        self._event.clear()
        self._done_ev.clear()
        if self._subprocess is False:
            # start the thread we are in threading mode.
            self._start()
        else:
            # append to instances
            if self not in self._get_instances():
                self._get_instances().append(self)

    def wait(self, timeout: Optional[float] = None) -> None:
        if not self._done_ev:
            return
        if not self.is_subprocess_mode() or self.is_subprocess_mode_and_parent_process():
            self._done_ev.wait(timeout=timeout)

    def _start(self) -> None:
        # if we already started do nothing
        if isinstance(self._thread, Thread):
            if self._thread_pid == os.getpid():
                return

        # make sure we start the metrics thread pools before starting the daemon thread
        # workaround for: https://github.com/python/cpython/issues/113964
        from ...backend_interface.metrics.interface import Metrics

        # noinspection PyProtectedMember
        Metrics._initialize_upload_pools()

        self._thread_pid = os.getpid()
        self._thread = Thread(target=self._daemon)
        self._thread.daemon = True
        self._thread.start()

    def stop(self) -> None:
        if not self._thread:
            return

        if not self._is_subprocess_mode_and_not_parent_process() and (
            not self.is_subprocess_mode() or self.is_subprocess_alive()
        ):
            self._event.set()

        if isinstance(self._thread, Thread):
            # should we wait for the thread to finish
            # noinspection PyBroadException
            try:
                # there is a race here, and if someone else closes the
                # thread it can become True/None and we will fail, it is fine
                self._thread.join()
            except BaseException:
                pass

            try:
                self._get_instances().remove(self)
            except ValueError:
                pass
            self._thread = False

    def daemon(self) -> None:
        while True:
            if self._event.wait(self._wait_timeout):
                break
            self._daemon_step()

    def _daemon(self) -> None:
        self._start_ev.set()
        try:
            self.daemon()
        finally:
            self.post_execution()
            self._thread = False

    def post_execution(self) -> None:
        self._done_ev.set()

    def set_subprocess_mode(self) -> None:
        # called just before launching the daemon in a subprocess
        if not self._subprocess:
            self._subprocess = True
        if not isinstance(self._done_ev, SafeEvent):
            self._done_ev = SafeEvent()
        if not isinstance(self._start_ev, SafeEvent):
            self._start_ev = SafeEvent()
        if not isinstance(self._event, SafeEvent):
            self._event = SafeEvent()

    def _daemon_step(self) -> None:
        pass

    @classmethod
    def start_all(cls, task: Any, wait_for_subprocess: bool = True) -> None:
        # noinspection PyProtectedMember
        execute_in_subprocess = task._report_subprocess_enabled

        if not execute_in_subprocess:
            for d in BackgroundMonitor._instances.get(id(task.id), []):
                d._start()
        elif not BackgroundMonitor._main_process:
            cls._parent_pid = os.getpid()
            cls._sub_process_started = SafeEvent()
            cls._sub_process_started.clear()
            cls._main_process_task_id = task.id
            # setup
            for d in BackgroundMonitor._instances.get(id(task.id), []):
                d.set_subprocess_mode()

            # ToDo: solve for standalone spawn subprocess
            # prefer os.fork, because multipprocessing.Process add atexit callback, which might later be invalid.
            cls.__start_subprocess_os_fork(task_obj_id=id(task.id))
            # if ForkContext is not None and isinstance(get_context(), ForkContext):
            #     cls.__start_subprocess_forkprocess(task_obj_id=id(task.id))
            # else:
            #     cls.__start_subprocess_os_fork(task_obj_id=id(task.id))

            # wait until subprocess is up
            if wait_for_subprocess:
                cls._sub_process_started.wait()

    @classmethod
    def __start_subprocess_os_fork(cls, task_obj_id: int) -> None:
        process_args = (task_obj_id, cls._sub_process_started, os.getpid())
        BackgroundMonitor._main_process = os.fork()
        # check if we are the child process
        if BackgroundMonitor._main_process == 0:
            # update to the child process pid
            BackgroundMonitor._main_process = os.getpid()
            BackgroundMonitor._main_process_proc_obj = psutil.Process(BackgroundMonitor._main_process)
            cls._background_process_start(*process_args)
            # force to leave the subprocess
            leave_process(0)
            return

        # update main process object (we are now in the parent process, and we update on the child's subprocess pid)
        # noinspection PyBroadException
        try:
            BackgroundMonitor._main_process_proc_obj = psutil.Process(BackgroundMonitor._main_process)
        except Exception:
            # if we fail for some reason, do not crash, switch to thread mode when you can
            BackgroundMonitor._main_process_proc_obj = None

    @classmethod
    def __start_subprocess_forkprocess(cls, task_obj_id: int) -> None:
        _main_process = Process(
            target=cls._background_process_start,
            args=(task_obj_id, cls._sub_process_started, os.getpid()),
        )
        _main_process.daemon = True
        # Hack allow to create daemon subprocesses (even though python doesn't like it)
        un_daemonize = False
        # noinspection PyBroadException
        try:
            from multiprocessing import current_process

            if current_process()._config.get("daemon"):  # noqa
                un_daemonize = current_process()._config.get("daemon")  # noqa
                current_process()._config["daemon"] = False  # noqa
        except BaseException:
            pass
        # try to start the background process, if we fail retry again, or crash
        for i in range(4):
            try:
                _main_process.start()
                break
            except BaseException:
                if i < 3:
                    sleep(1)
                    continue
                raise
        BackgroundMonitor._main_process = _main_process.pid
        BackgroundMonitor._main_process_proc_obj = psutil.Process(BackgroundMonitor._main_process)
        if un_daemonize:
            # noinspection PyBroadException
            try:
                from multiprocessing import current_process

                current_process()._config["daemon"] = un_daemonize  # noqa
            except BaseException:
                pass

    @classmethod
    def _background_process_start(
        cls,
        task_obj_id: int,
        event_start: Optional[SafeEvent] = None,
        parent_pid: Optional[int] = None,
    ) -> None:
        # noinspection PyProtectedMember
        is_debugger_running = bool(getattr(sys, "gettrace", None) and sys.gettrace())
        # make sure we update the pid to our own
        cls._main_process = os.getpid()
        cls._main_process_proc_obj = psutil.Process(cls._main_process)
        # noinspection PyBroadException
        try:
            from ... import Task

            if Task._Task__current_task and Task._Task__current_task._Task__exit_hook:  # noqa
                Task._Task__current_task._Task__exit_hook.register_signal_and_exception_hooks()  # noqa

            # noinspection PyProtectedMember
            from ...binding.environ_bind import PatchOsFork

            PatchOsFork.unpatch_fork()
            PatchOsFork.unpatch_process_run()
        except:  # noqa
            # Do not change the exception we need to catch base exception as well
            pass

        # if a debugger is running, wait for it to attach to the subprocess
        if is_debugger_running:
            sleep(3)

        instances = BackgroundMonitor._instances.get(task_obj_id, [])
        # launch all the threads
        for d in instances:
            d._start()

        if cls._sub_process_started:
            cls._sub_process_started.set()

        if event_start:
            event_start.set()

        # wait until we are signaled
        for i in instances:
            # DO NOT CHANGE, we need to catch base exception, if the process gte's killed
            try:
                while i._thread is None or (i._thread and i._thread.is_alive()):
                    # thread is still not up
                    if i._thread is None:
                        sleep(0.1)
                        continue

                    # noinspection PyBroadException
                    try:
                        p = psutil.Process(parent_pid)
                        parent_alive = p.is_running() and p.status() != psutil.STATUS_ZOMBIE
                    except Exception:
                        parent_alive = False

                    # if parent process is not here we should just leave!
                    if not parent_alive:
                        return

                    # DO NOT CHANGE, we need to catch base exception, if the process gte's killed
                    try:
                        # timeout so we can detect if the parent process got killed.
                        i._thread.join(timeout=30.0)
                    except:  # noqa
                        break
            except:  # noqa
                pass
        # we are done, leave process
        return

    def is_alive(self) -> bool:
        if not self.is_subprocess_mode():
            return isinstance(self._thread, Thread) and self._thread.is_alive()

        if self.get_at_exit_state():
            return self.is_subprocess_alive() and self._thread

        return self.is_subprocess_alive() and self._thread and self._start_ev.is_set() and not self._done_ev.is_set()

    @classmethod
    def _fast_is_subprocess_alive(cls) -> bool:
        if not cls._main_process_proc_obj:
            return False
        # we have to assume the process actually exists, so we optimize for
        # just getting the object and status.
        # noinspection PyBroadException
        try:
            return (
                cls._main_process_proc_obj.is_running() and cls._main_process_proc_obj.status() != psutil.STATUS_ZOMBIE
            )
        except Exception:
            return False

    @classmethod
    def is_subprocess_alive(cls, task: Optional["Task"] = None) -> bool:
        if not cls._main_process or (task and cls._main_process_task_id != task.id):
            return False
        # noinspection PyBroadException
        try:
            p = psutil.Process(cls._main_process)
            return p.is_running() and p.status() != psutil.STATUS_ZOMBIE
        except Exception:
            current_pid = cls._main_process
            if not current_pid:
                return False
            try:
                parent = psutil.Process(cls._parent_pid)
            except psutil.Error:
                # could not find parent process id
                return
            for child in parent.children(recursive=True):
                # kill ourselves last (if we need to)
                if child.pid == current_pid:
                    return child.is_running() and child.status() != psutil.STATUS_ZOMBIE
            return False

    def is_subprocess_mode(self) -> bool:
        return (
            self._subprocess is not False and bool(self._main_process) and self._task_id == self._main_process_task_id
        )

    def _get_instances(self) -> List["BackgroundMonitor"]:
        return self._instances.setdefault(self._task_obj_id, [])

    def _is_subprocess_mode_and_not_parent_process(self) -> bool:
        return self.is_subprocess_mode() and self._parent_pid != os.getpid()

    def is_subprocess_mode_and_parent_process(self) -> bool:
        return self.is_subprocess_mode() and self._parent_pid == os.getpid()

    def _is_thread_mode_and_not_main_process(self) -> bool:
        if self.is_subprocess_mode():
            return False
        from ... import Task

        # noinspection PyProtectedMember
        return Task._Task__is_subprocess()

    @classmethod
    def is_subprocess_enabled(cls, task: Optional["Task"] = None) -> bool:
        return bool(cls._main_process) and (not task or task.id == cls._main_process_task_id)

    @classmethod
    def clear_main_process(cls, task: "Task") -> None:
        if BackgroundMonitor._main_process_task_id != task.id:
            return
        cls.wait_for_sub_process(task)
        BackgroundMonitor._main_process = None
        BackgroundMonitor._main_process_proc_obj = None
        BackgroundMonitor._main_process_task_id = None
        BackgroundMonitor._parent_pid = None
        BackgroundMonitor._sub_process_started = None
        BackgroundMonitor._instances = {}
        SingletonThreadPool.clear()

    @classmethod
    def wait_for_sub_process(cls, task: Any, timeout: Optional[float] = None) -> None:
        if not cls.is_subprocess_enabled(task=task):
            return

        for d in BackgroundMonitor._instances.get(id(task.id), []):
            d.stop()

        tic = time()
        while cls.is_subprocess_alive(task=task) and (not timeout or time() - tic < timeout):
            sleep(0.03)

    @classmethod
    def set_at_exit_state(cls, state: bool = True) -> None:
        cls._at_exit = bool(state)

    @classmethod
    def get_at_exit_state(cls) -> bool:
        return cls._at_exit


def leave_process(status: int = 0) -> None:
    """
    Exit current process with status-code (status)
    :param status: int exit code
    """
    try:
        sys.exit(status or 0)
    except:  # noqa
        # ipython/jupyter notebook will not allow to call sys.exit
        # we have to call the low level function
        os._exit(status or 0)  # noqa
