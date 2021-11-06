import os
import sys
from pathlib import Path

import venv

CWD = Path(__file__).cwd()
COMMON_VENV_NAMES = (".env", ".venv", "env", "venv", "ENV", "VENV")


def currently_in_venv() -> bool:
    """Checks to see if we're currently in a venv. Returns True or False."""
    # From https://stackoverflow.com/questions/1871549/determine-if-python-is-running-inside-virtualenv
    # In venv or virtualenv, sys.prefix is /path/to/venv-or-whatever. Otherwise
    # it is /path/to/folder-with-base-python.
    current_prefix = sys.prefix
    # In venv or virtualenv, sys.base_prefix will return /path/to/venv-or-whatever.
    # Some older versions of virtualenv called it `real_prefix` instead, so we
    # check for that too.
    base_prefix = (
        getattr(sys, "base_prefix", None)
        or getattr(sys, "real_prefix", None)
        or sys.prefix
    )

    print(f"sys.prefix: {sys.prefix}")
    print(f"base.prefix: {sys.base_prefix}")
    if current_prefix == base_prefix:
        return False
    else:
        return True


def detect_common_venv_dirs() -> Path | None:
    """Looks for common venv / virtualenv folders. If one is detected, returns
    the Path for that folder. Otherwise, returns None.
    """
    for name in COMMON_VENV_NAMES:
        if (venv_dir := CWD / name).is_dir():
            return venv_dir
    # else ...
    return None


def upgrade_pip() -> int:
    """Issues command `python -m pip install --upgrade pip`, and returns that
    command's exit code.
    """
    if not currently_in_venv:
        activate_venv()
    return os.system("python -m pip install --upgrade pip")


def upgrade_setuptools() -> int:
    """Issues command `pip install --upgrade setuptools`, and returns that
    command's exit code.
    """
    if not currently_in_venv:
        activate_venv()
    return os.system("pip install --upgrade setuptools")


def install_requirements(req_file: str | Path = "requirements.txt") -> int:
    """Issues command `pip install -r req_file`, and returns that command's
    exit code.
    """
    if not currently_in_venv:
        activate_venv()
    return os.system(f"pip install -r {req_file}")


def create_venv() -> int:
    """Issues command `python -m venv venv`, and returns that command's exit
    code.
    """
    os.chdir(str(CWD))  # just in case we got moved somewhere else
    return os.system("python -m venv venv")


def get_activate_script(venv_dir: Path | None = None) -> Path:
    """The venv activation script can vary depending on OS. This function
    returns the Path of the correct script.
    - Linux: venv_dir/bin/activate
    - MacOS: venv_dir/bin/activate
    - Windows: venv_dir/bin/Activate.ps1
    """
    if venv_dir is None:
        venv_dir = detect_common_venv_dirs()
        if venv_dir is None:  # still
            raise FileNotFoundError  # Technically, directory not found

    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        return venv_dir / "bin/activate"
    elif sys.platform.startswith("win"):
        return venv_dir / "bin/Activate.ps1"
    else:
        # TODO: log the fact that platform is unknown
        return venv_dir / "bin/activate"


def activate_venv():
    activate_script = get_activate_script()
    print("Activating venv with".upper() + str(activate_script))
    return os.system(f". {activate_script}")


def create_activate_convenience_script() -> Path:
    script_file = CWD / "activate_venv"
    if script_file.exists():
        if script_file.is_file():
            return script_file
        else:
            # Technically it must be something other than a file, but
            # basically the same error
            raise FileExistsError
    else:
        print(f"CREATING {script_file}")
        sf_lines = [
            "#!/bin/bash",
            "# call with command '. activate_venv'",
            f". {get_activate_script().relative_to(CWD)}",
        ]
        sf_contents = "\n".join(sf_lines) + "\n"
        with script_file.open(mode="w") as sf:
            sf.write(sf_contents)


def check_venv():
    """Checks to see if a venv exists.
    - If no venv exists, create it and activate it and install/update reqs
    - If a venv exists but is not active, activate it and install/update reqs
    - If we are currently in an active venv, install/update reqs
    - If we are currently in an active venv and no install/updates needed, pass
    """
    # venv doesn't need to be in folder named venv. That's hard to handle,
    # but for now we'll just check the most obvious case where we are in
    # an *already active* arbitrarily-named venv.
    if currently_in_venv():
        print("CURRENTLY IN VENV")
        pass
    elif detect_common_venv_dirs():
        # venv installed but not active
        print("venv installed but not active".upper())
        create_activate_convenience_script()
        activate_venv()
    else:
        # we probably need to install venv
        print("we probably need to install venv".upper())
        create_venv()
        create_activate_convenience_script()
        activate_venv()
    print("updating pip, setuptools, and installing reqs".upper())
    upgrade_pip()
    upgrade_setuptools()
    install_requirements()


if __name__ == "__main__":
    check_venv()
