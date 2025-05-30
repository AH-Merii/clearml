import tempfile

from pathlib2 import Path

from ..backend_config import EnvEntry
from ..backend_config.converters import base64_to_text, or_

SESSION_CACHE_FILE = ".session.json"
DEFAULT_CACHE_DIR = str(Path(tempfile.gettempdir()) / "clearml_cache")

TASK_ID_ENV_VAR = EnvEntry("CLEARML_TASK_ID", "TRAINS_TASK_ID")
DOCKER_IMAGE_ENV_VAR = EnvEntry("CLEARML_DOCKER_IMAGE", "TRAINS_DOCKER_IMAGE")
DOCKER_BASH_SETUP_ENV_VAR = EnvEntry("CLEARML_DOCKER_BASH_SCRIPT")
LOG_TO_BACKEND_ENV_VAR = EnvEntry("CLEARML_LOG_TASK_TO_BACKEND", "TRAINS_LOG_TASK_TO_BACKEND", type=bool)
NODE_ID_ENV_VAR = EnvEntry("CLEARML_NODE_ID", "TRAINS_NODE_ID", type=int)
PROC_MASTER_ID_ENV_VAR = EnvEntry("CLEARML_PROC_MASTER_ID", "TRAINS_PROC_MASTER_ID", type=str)
LOG_STDERR_REDIRECT_LEVEL = EnvEntry("CLEARML_LOG_STDERR_REDIRECT_LEVEL", "TRAINS_LOG_STDERR_REDIRECT_LEVEL")
DEV_WORKER_NAME = EnvEntry("CLEARML_WORKER_NAME", "TRAINS_WORKER_NAME")
DEV_TASK_NO_REUSE = EnvEntry("CLEARML_TASK_NO_REUSE", "TRAINS_TASK_NO_REUSE", type=bool)
TASK_LOG_ENVIRONMENT = EnvEntry("CLEARML_LOG_ENVIRONMENT", "TRAINS_LOG_ENVIRONMENT", type=str)
CLEARML_CACHE_DIR = EnvEntry("CLEARML_CACHE_DIR", "TRAINS_CACHE_DIR")
DEBUG_SIMULATE_REMOTE_TASK = EnvEntry("CLEARML_SIMULATE_REMOTE_TASK", type=bool)
DEV_DEFAULT_OUTPUT_URI = EnvEntry("CLEARML_DEFAULT_OUTPUT_URI", type=str)
TASK_SET_ITERATION_OFFSET = EnvEntry("CLEARML_SET_ITERATION_OFFSET", type=int)
HOST_MACHINE_IP = EnvEntry("CLEARML_AGENT_HOST_IP", type=str)

LOG_LEVEL_ENV_VAR = EnvEntry("CLEARML_LOG_LEVEL", "TRAINS_LOG_LEVEL", converter=or_(int, str))

SUPPRESS_UPDATE_MESSAGE_ENV_VAR = EnvEntry(
    "CLEARML_SUPPRESS_UPDATE_MESSAGE", "TRAINS_SUPPRESS_UPDATE_MESSAGE", type=bool
)

MAX_SERIES_PER_METRIC = EnvEntry("CLEARML_MAX_SERIES_PER_METRIC", default=100, type=int)

# values are 0/None (task per node), 1/2 (multi-node reporting, colored console), -1 (only report rank 0 node)
ENV_MULTI_NODE_SINGLE_TASK = EnvEntry("CLEARML_MULTI_NODE_SINGLE_TASK", type=int, default=None)

JUPYTER_PASSWORD = EnvEntry("CLEARML_JUPYTER_PASSWORD")

# Repository detection
VCS_REPO_TYPE = EnvEntry("CLEARML_VCS_REPO_TYPE", "TRAINS_VCS_REPO_TYPE", default="git")
VCS_REPOSITORY_URL = EnvEntry("CLEARML_VCS_REPO_URL", "TRAINS_VCS_REPO_URL")
VCS_COMMIT_ID = EnvEntry("CLEARML_VCS_COMMIT_ID", "TRAINS_VCS_COMMIT_ID")
VCS_BRANCH = EnvEntry("CLEARML_VCS_BRANCH", "TRAINS_VCS_BRANCH")
VCS_ROOT = EnvEntry("CLEARML_VCS_ROOT", "TRAINS_VCS_ROOT")
VCS_WORK_DIR = EnvEntry("CLEARML_VCS_WORK_DIR")
VCS_ENTRY_POINT = EnvEntry("CLEARML_VCS_ENTRY_POINT")
VCS_STATUS = EnvEntry("CLEARML_VCS_STATUS", "TRAINS_VCS_STATUS", converter=base64_to_text)
VCS_DIFF = EnvEntry("CLEARML_VCS_DIFF", "TRAINS_VCS_DIFF", converter=base64_to_text)
"""
Handles repository or script diff

Environment variable primarily for internal use. Expects a base64 encoded string.
If explicitly set to an empty string, will not log the diff, shown in the UI under "Uncommitted Changes".

.. note::
    Overriding `CLEARML_VCS_DIFF` may change the results of a task when executed remotely.
"""
