import pytest
from pathlib import Path


def assert_archive_exists(base_dir, sub_names):

    directories = [base_dir / sub for sub in sub_names]
    directories.append(base_dir)

    for dir in directories:
        print(dir)
        assert dir.exists()


class TestSetUpArchive:
    def test_archive_missing(self, archive_dir):
        """Tests set_up_archive() with the archive directory missing. It
        expects the function to create the archive and sub directories"""

        # setup
        archive_dir.rmdir()
        assert archive_dir.exists() == False

        # execution
        temp_dir = archive_dir.parent
        passed, message, dir = set_up_archive(base_dir=temp_dir)

        # validation
        assert_dirs_exist(archive_dir, ARCHIVE_SUBS)
        assert dir is not None
        assert passed
        assert message == "Archives folder is setup correctly"

