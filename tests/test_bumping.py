from pathlib import Path

import pytest

from version.main import VersionParts, bump_version, get_version


@pytest.fixture
def version_file(tmpdir_factory):
    version_file = tmpdir_factory.mktemp("data").join("VERSION")
    with open(version_file, "w") as file:
        file.write("0.1.0")
    return version_file


def test_bump_patch_from_version_file(version_file):
    bumped_version = bump_version(VersionParts.PATCH, version_file)
    assert bumped_version == "0.1.1"


def test_bump_minor_from_version_file(version_file):
    bumped_version = bump_version(VersionParts.MINOR, version_file)
    assert bumped_version == "0.2.0"


def test_bump_major_from_version_file(version_file):
    bumped_version = bump_version(VersionParts.MAJOR, version_file)
    assert bumped_version == "1.0.0"

def test_get_version(version_file):
    version = get_version(version_file)
    assert version == "0.1.0"
