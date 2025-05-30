import logging
import sys
from time import time
from typing import Optional, Callable, Any

from ..binding.frameworks import _patched_call  # noqa
from ..config import running_remotely, config, DEBUG_SIMULATE_REMOTE_TASK
from ..utilities.process.mp import ForkSafeRLock


class StdStreamPatch(object):
    _stdout_proxy = None
    _stderr_proxy = None
    _stdout_original_write = None
    _stderr_original_write = None

    @staticmethod
    def patch_std_streams(
        a_logger: logging.Logger,
        connect_stdout: bool = True,
        connect_stderr: bool = True,
        load_config_defaults: bool = True,
    ) -> None:
        if (
            (connect_stdout or connect_stderr)
            and not PrintPatchLogger.patched
            and (not running_remotely() or DEBUG_SIMULATE_REMOTE_TASK.get())
        ):
            StdStreamPatch._stdout_proxy = (
                PrintPatchLogger(
                    sys.stdout,
                    a_logger,
                    level=logging.INFO,
                    load_config_defaults=load_config_defaults,
                )
                if connect_stdout and not sys.stdout.closed
                else None
            )
            StdStreamPatch._stderr_proxy = (
                PrintPatchLogger(
                    sys.stderr,
                    a_logger,
                    level=logging.ERROR,
                    load_config_defaults=load_config_defaults,
                )
                if connect_stderr and not sys.stderr.closed
                else None
            )

            if StdStreamPatch._stdout_proxy:
                # noinspection PyBroadException
                try:
                    if StdStreamPatch._stdout_original_write is None:
                        StdStreamPatch._stdout_original_write = sys.stdout.write

                    # this will only work in python 3, guard it with try/catch
                    if not hasattr(sys.stdout, "_original_write"):
                        sys.stdout._original_write = sys.stdout.write
                    sys.stdout.write = StdStreamPatch._stdout__patched__write__
                except Exception:
                    pass
                sys.stdout = StdStreamPatch._stdout_proxy
                # noinspection PyBroadException
                try:
                    sys.__stdout__ = sys.stdout
                except Exception:
                    pass

            if StdStreamPatch._stderr_proxy:
                # noinspection PyBroadException
                try:
                    if StdStreamPatch._stderr_original_write is None:
                        StdStreamPatch._stderr_original_write = sys.stderr.write
                    if not hasattr(sys.stderr, "_original_write"):
                        sys.stderr._original_write = sys.stderr.write
                    sys.stderr.write = StdStreamPatch._stderr__patched__write__
                except Exception:
                    pass
                sys.stderr = StdStreamPatch._stderr_proxy

                # patch the base streams of sys (this way colorama will keep its ANSI colors)
                # noinspection PyBroadException
                try:
                    sys.__stderr__ = sys.stderr
                except Exception:
                    pass

            # now check if we have loguru and make it re-register the handlers
            # because it stores internally the stream.write function, which we cant patch
            # noinspection PyBroadException
            try:
                from loguru import logger  # noqa

                register_stderr = None
                register_stdout = None
                for k, v in logger._handlers.items():  # noqa
                    if connect_stderr and v._name == "<stderr>":  # noqa
                        register_stderr = k
                    elif connect_stdout and v._name == "<stdout>":  # noqa
                        register_stderr = k
                if register_stderr is not None:
                    logger.remove(register_stderr)
                    logger.add(sys.stderr)
                if register_stdout is not None:
                    logger.remove(register_stdout)
                    logger.add(sys.stdout)
            except Exception:
                pass

        elif (connect_stdout or connect_stderr) and not running_remotely():
            if StdStreamPatch._stdout_proxy and connect_stdout:
                StdStreamPatch._stdout_proxy.connect(a_logger)
            if StdStreamPatch._stderr_proxy and connect_stderr:
                StdStreamPatch._stderr_proxy.connect(a_logger)

    @staticmethod
    def patch_logging_formatter(a_logger: logging.Logger, logging_handler: logging.Handler = None) -> None:
        if not logging_handler:
            import logging

            logging_handler = logging.Handler
        logging_handler.format = _patched_call(logging_handler.format, HandlerFormat(a_logger))

    @staticmethod
    def remove_patch_logging_formatter(logging_handler: logging.Handler = None) -> None:
        if not logging_handler:
            import logging

            logging_handler = logging.Handler
        # remove the function, Hack calling patched logging.Handler.format() returns the original function
        # noinspection PyBroadException
        try:
            logging_handler.format = logging_handler.format()  # noqa
        except Exception:
            pass

    @staticmethod
    def remove_std_logger(logger: Optional[logging.Logger] = None) -> None:
        if isinstance(sys.stdout, PrintPatchLogger):
            # noinspection PyBroadException
            try:
                sys.stdout.disconnect(logger)
            except Exception:
                pass
        if isinstance(sys.stderr, PrintPatchLogger):
            # noinspection PyBroadException
            try:
                sys.stderr.disconnect(logger)
            except Exception:
                pass

    @staticmethod
    def stdout_original_write(*args: Any, **kwargs: Any) -> None:
        if StdStreamPatch._stdout_original_write:
            StdStreamPatch._stdout_original_write(*args, **kwargs)
        else:
            sys.stdout.write(*args, **kwargs)

    @staticmethod
    def stderr_original_write(*args: Any, **kwargs: Any) -> None:
        if StdStreamPatch._stderr_original_write:
            StdStreamPatch._stderr_original_write(*args, **kwargs)
        else:
            sys.stderr.write(*args, **kwargs)

    @staticmethod
    def _stdout__patched__write__(*args: Any, **kwargs: Any) -> Any:
        if StdStreamPatch._stdout_proxy:
            return StdStreamPatch._stdout_proxy.write(*args, **kwargs)
        return sys.stdout._original_write(*args, **kwargs)  # noqa

    @staticmethod
    def _stderr__patched__write__(*args: Any, **kwargs: Any) -> Any:
        if StdStreamPatch._stderr_proxy:
            return StdStreamPatch._stderr_proxy.write(*args, **kwargs)
        return sys.stderr._original_write(*args, **kwargs)  # noqa


class HandlerFormat(object):
    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def __call__(self, original_format_func: Callable, *args: Any) -> Any:
        # hack get back original function, so we can remove it
        if all(a is None for a in args):
            return original_format_func
        if len(args) == 1:
            record = args[0]
            msg = original_format_func(record)
        else:
            handler = args[0]
            record = args[1]
            msg = original_format_func(handler, record)

        self._logger.report_text(msg=msg, level=record.levelno, print_console=False)
        return msg


class PrintPatchLogger(object):
    """
    Allowed patching a stream into the logger.
    Used for capturing and logging stdin and stderr when running in development mode pseudo worker.
    """

    patched = False
    lock = ForkSafeRLock()
    recursion_protect_lock = ForkSafeRLock()
    cr_flush_period = None

    def __init__(
        self,
        stream: Any,
        logger: logging.Logger = None,
        level: int = logging.INFO,
        load_config_defaults: bool = True,
    ) -> None:
        if load_config_defaults and PrintPatchLogger.cr_flush_period is None:
            PrintPatchLogger.cr_flush_period = config.get("development.worker.console_cr_flush_period", 0)
        PrintPatchLogger.patched = True
        self._terminal = stream
        self._log = logger
        self._log_level = level
        self._cur_line = ""
        self._force_lf_flush = False
        self._lf_last_flush = 0

    def write(self, message: str) -> None:
        # make sure that we do not end up in infinite loop (i.e. log.console ends up calling us)
        if self._log and not PrintPatchLogger.recursion_protect_lock._is_owned():  # noqa
            try:
                # make sure we flush from time to time on \r
                self._test_lr_flush()

                self.lock.acquire()
                # noinspection PyBroadException
                try:
                    with PrintPatchLogger.recursion_protect_lock:
                        if hasattr(self._terminal, "_original_write"):
                            self._terminal._original_write(message)  # noqa
                        else:
                            self._terminal.write(message)
                except Exception:
                    pass

                do_flush = "\n" in message
                # check for CR character
                do_cr = "\r" in message
                # check for "Escape Arrow-Up" character (tqdm's way of clearing a line)
                if "\x1b[A" in message:
                    do_cr = True
                    # replace it with \r so it is more standard
                    message = message.replace("\x1b[A", "\r")

                self._cur_line += message

                if not do_flush and do_cr and PrintPatchLogger.cr_flush_period and self._force_lf_flush:
                    self._cur_line += "\n"
                    do_flush = True

                if (not do_flush and (PrintPatchLogger.cr_flush_period or not do_cr)) or not message:
                    return

                if PrintPatchLogger.cr_flush_period and self._cur_line:
                    self._cur_line = "\n".join(line.split("\r")[-1] for line in self._cur_line.split("\n"))

                last_lf = self._cur_line.rindex("\n" if do_flush else "\r")
                next_line = self._cur_line[last_lf + 1 :]
                cur_line = self._cur_line[: last_lf + 1].rstrip()
                self._cur_line = next_line
            finally:
                self.lock.release()

            if cur_line:
                self._force_lf_flush = False
                with PrintPatchLogger.recursion_protect_lock:
                    # noinspection PyBroadException
                    try:
                        if self._log:
                            # noinspection PyProtectedMember
                            self._log._console(cur_line, level=self._log_level, omit_console=True)
                    except Exception:
                        # what can we do, nothing
                        pass
        else:
            # noinspection PyBroadException
            try:
                if hasattr(self._terminal, "_original_write"):
                    self._terminal._original_write(message)  # noqa
                else:
                    self._terminal.write(message)
            except Exception:
                pass

    def connect(self, logger: logging.Logger) -> None:
        # refresh if needed
        if PrintPatchLogger.cr_flush_period is None:
            PrintPatchLogger.cr_flush_period = config.get("development.worker.console_cr_flush_period", 0)

        # if we had a previous log object, call flush before switching
        if self._log and hasattr(self._log, "_flush_into_logger"):
            # since we are not sure how flush should be called, we protect it
            # noinspection PyBroadException
            try:
                # noinspection PyProtectedMember
                self._log._flush_into_logger(a_future_func=logger)
            except Exception:
                pass

        self._cur_line = ""
        self._log = logger

    def disconnect(self, logger: logging.Logger = None) -> None:
        # disconnect the logger only if it was registered
        if not logger or self._log == logger:
            self.connect(None)

    def _test_lr_flush(self) -> None:
        if not self.cr_flush_period:
            return
        if time() - self._lf_last_flush > self.cr_flush_period:
            self._force_lf_flush = True
            self._lf_last_flush = time()

    def __getattr__(self, attr: str) -> Any:
        if attr in [
            "_log",
            "_terminal",
            "_log_level",
            "_cur_line",
            "_cr_overwrite",
            "_force_lf_flush",
            "_lf_last_flush",
        ]:
            return self.__dict__.get(attr)
        return getattr(self._terminal, attr)

    def __setattr__(self, key: str, value: Any) -> None:
        if key in [
            "_log",
            "_terminal",
            "_log_level",
            "_cur_line",
            "_cr_overwrite",
            "_force_lf_flush",
            "_lf_last_flush",
        ]:
            self.__dict__[key] = value
        else:
            return setattr(self._terminal, key, value)
