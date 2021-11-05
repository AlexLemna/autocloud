import logging
from logging import DEBUG, INFO, WARNING
from pathlib import Path

# To enable verbose debugging in a logfile or on the console, directly edit
# the values below.
VERBOSE_CONSOLE = False
VERBOSE_LOGFILE = False

REPO_DIR = Path(__file__).absolute().parent  # this file's directory
LOG_DIR = (REPO_DIR / "logs")

class SetupLogger(logging.Logger):
    FILE_RECORD_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    FILE_FORMATTER = logging.Formatter(FILE_RECORD_FORMAT)

    def __init__(self, name: str = "root", level=DEBUG) -> None:
        super().__init__(name, level=level)

        LOG_DIR.mkdir(mode=0o755, parents=True, exist_ok=True)

        self._file = logging.FileHandler(f"{LOG_DIR}/autocloud_setup.log")
        self._file.setFormatter(self.FILE_FORMATTER)
        if VERBOSE_LOGFILE is False:
            self._file.setLevel(INFO)
        else:
            self._file.setLevel(DEBUG)

        self._console = logging.StreamHandler()
        if VERBOSE_CONSOLE is False:
            self._console.setLevel(WARNING)
        else:
            self._console.setLevel(DEBUG)

        self.addHandler(self._file)
        self.addHandler(self._console)
        self.info(f"SetupLogger {self.name} initialized in {__file__}")


log = SetupLogger()

USER_LOCAL_BIN = Path(Path().home() / ".local/bin")

if USER_LOCAL_BIN.exists() is False:
    log.debug(f"{USER_LOCAL_BIN} does not exist ...")
    log.debug(f"Creating {USER_LOCAL_BIN} and any necessary parent directories ...")
    USER_LOCAL_BIN.mkdir(mode=0o0755, parents=True)
elif USER_LOCAL_BIN.is_file():
    log.critical(f"{USER_LOCAL_BIN} is a file, not a directory.")
    log.critical("Cannot continue. Exiting.")
    raise FileExistsError

PATH_SYMLINK = USER_LOCAL_BIN / "autocloud"
ENTRY_FILE = REPO_DIR / "autocloud.sh"
MAIN_FILE = REPO_DIR / "main.py"

log.info(f"Creating {PATH_SYMLINK} ...")
try:
    log.debug(f"Symlink {PATH_SYMLINK} will point to {ENTRY_FILE} ...")
    PATH_SYMLINK.symlink_to(f"{ENTRY_FILE}")
except FileExistsError as e:
    log.critical(f"ERROR! {PATH_SYMLINK} already exists.")
    log.critical("Setup has already happened. Cannot continue. Exiting.")
    raise e

with ENTRY_FILE.open(mode="w") as f:
    log.debug(f"Pointing {ENTRY_FILE} to {MAIN_FILE} ...")
    lines = [
        "#!/bin/bash",
        # Specifically not using a path below for Python so can be used
        # with venv
        f"python {MAIN_FILE}",
    ]
    f.writelines("\n".join(line for line in lines) + "\n")

log.debug(f"Making {ENTRY_FILE} executable ...")
ENTRY_FILE.chmod(mode=0o740)

log.info(f"Setup complete.")
