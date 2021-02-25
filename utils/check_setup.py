from pathlib import Path
import sys
import json


def run_checks(base_dir=None):
    """Checks the project setup by running check_config() and set_up_archive()
    Arguments:
        base_dir: Path to the directory in which archives will be created
    Returns:
        checks: A dictionary of checks that passed and failed
        config: A dictionary loaded from the config file
        archive: The archive directory as a pathlib.Path object
    """
    # print("Running config check")
    # passed, message, config = check_config(path)
    # if not passed:
    #     error = f"Config check failed with the following error: {message}"
    #     return False, error, None, None
    # print(message)

    print("Running archive setup")
    passed, message, archive = set_up_archive(base_dir)
    if not passed:
        error = f"Archive setup failed with the following error: {message}"
    print(message)

    message = "All checks passed and everything is setup correctly"
    return True, message, config, archive


def set_up_archive(base_dir=None):
    """Sets up the archive with all of its sub-directories
    Arguments:
        base_dir: Path to directory in which archives will be created, if
        no path is provided, function will use the current working directory
    Returns:
        passed: Boolean indicating whether the set up passed
        message: A message describing the set up
        archive_dir: pathlib.Path object to the archive directory
    """

    if not base_dir:
        base_dir = Path.cwd()

    archive_dir = base_dir / "archive"

    archive_dir.mkdir(parents=True, exist_ok=True)

    return True, "Archives folder is setup correctly", archive_dir
