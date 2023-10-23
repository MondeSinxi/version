import configparser
import pytest

from version.main import VersionParts, bump_version, get_version


@pytest.fixture
def version_file(tmpdir_factory):
    version_file = tmpdir_factory.mktemp("data").join("VERSION")
    with open(version_file, "w") as file:
        file.write("0.1.0")
    return version_file


@pytest.fixture
def bad_version_file(tmpdir_factory):
    version_file = tmpdir_factory.mktemp("data").join("VERSION")
    with open(version_file, "w") as file:
        file.write("0.1.a")
    return version_file


@pytest.fixture
def pyproject_file(tmpdir_factory):
    config = configparser.ConfigParser()
    config["tool.poetry"] = {}
    config["tool.poetry"]["version"] = "2.0.1"
    config_file = tmpdir_factory.mktemp("data").join("pyproject.yml")
    with open(config_file, "w") as file:
        config.write(file)
    return config_file


@pytest.fixture
def bad_pyproject_file(tmpdir_factory):
    config = configparser.ConfigParser()
    config["tool.poetry"] = {}
    config_file = tmpdir_factory.mktemp("data").join("bad_pyproject.yml")
    with open(config_file, "w") as file:
        config.write(file)
    return config_file


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


def test_get_version_from_pyproject(pyproject_file):
    version = get_version(pyproject_file=pyproject_file)
    assert version == "2.0.1"


def test_bump_patch_from_toml_file(pyproject_file):
    bumped_version = bump_version(VersionParts.PATCH, pyproject_file=pyproject_file)
    assert bumped_version == "2.0.2"


def test_bump_minor_from_toml_file(pyproject_file):
    bumped_version = bump_version(VersionParts.MINOR, pyproject_file=pyproject_file)
    assert bumped_version == "2.1.0"


def test_bump_major_from_toml_file(pyproject_file):
    bumped_version = bump_version(VersionParts.MAJOR, pyproject_file=pyproject_file)
    assert bumped_version == "3.0.0"


def test_bad_version(bad_version_file):
    with pytest.raises(SystemExit):
        bump_version(VersionParts.MAJOR, bad_version_file)


def test_get_version_with_no_files():
    with pytest.raises(FileNotFoundError):
        get_version()


def test_bump_version_with_no_files():
    with pytest.raises(FileNotFoundError):
        bump_version(VersionParts.MAJOR)


def test_bad_pyproject(bad_pyproject_file):
    with pytest.raises(SystemExit):
        get_version(pyproject_file=bad_pyproject_file)
