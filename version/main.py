import configparser
from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
import sys
from rich import print
from typing import List, Union

import typer

app = typer.Typer()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()


class VersionParts(Enum):
    """
    Enum representing version parts: major, minor, and patch.
    """

    major = "major"
    minor = "minor"
    patch = "patch"


@dataclass
class Version:
    """
    Represents a version with major, minor, and patch components.
    """

    major: int = 0
    minor: int = 0
    patch: int = 0

    def from_file(self, version_file: str | Path) -> None:
        """
        Load version components from a file.

        Args:
            file (str | Path): Path to the version file.

        Raises:
            FileNotFoundError: If the specified file is not found.
        """
        version_str = self.get_version_str(version_file)
        self.major, self.minor, self.patch = self._parse_split_versions(version_str)

    def get_version_str(self, version_file: Path | str) -> str:
        """
        Parses a file to get the version string representasion

        Args:
            file (str | Path): Path to version file.

        Returns:
            str
        """
        if isinstance(version_file, str):
            version_file = Path("version_file")
        if version_file.exists():
            with open(version_file, "r") as file:
                version_str = file.read()
            return version_str.strip()
        # Try parsing pyproject.toml file if no version file is found
        config.read("pyproject.toml")
        version_str = config["tool.poetry"]["version"]
        return version_str.replace('"', "")

    def _parse_split_versions(self, version_str: str) -> List[int]:
        version = [v for v in version_str.split(".")]
        assert len(version) == 3, "format of the version must be x.y.z"
        try:
            return [int(v) for v in version]
        except ValueError:
            logger.exception(f"Cannot convert parts to integers {version_str}")
            sys.exit()

    def upgrade_major(self) -> None:
        self.major += 1
        self.minor = 0
        self.patch = 0

    def upgrade_minor(self) -> None:
        self.minor += 1
        self.patch = 0

    def upgrade_patch(self) -> None:
        self.patch += 1

    def bump(self, subtype):
        if subtype == "major":
            self.upgrade_major()
        if subtype == "minor":
            self.upgrade_minor()
        if subtype == "patch":
            self.upgrade_patch()

    def update_file(self, version_file: Union[str, Path]) -> None:
        if isinstance(version_file, str):
            version_file = Path(version_file)
        if version_file.exists():
            with open(version_file, "w") as file:
                file.write(self.version)
        elif Path("pyproject.toml").exists():
            config.read("pyproject.toml")
            config["tool.poetry"]["version"] = self.version
            with open("pyproject.toml", "w") as configfile:
                config.write(configfile)
        else:
            raise FileNotFoundError("No file to write version to.")

    @property
    def version(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@app.command()
def get_version(version_file: str = "VERSION"):
    """
    Command to get the current version and display it.
    """
    version = Version()
    version.from_file(version_file)
    print(f"VERSION: {version.version}")


@app.command()
def bump_version(bump: VersionParts, version_file: str = "VERSION"):
    """
    Command to bump the specified version part (major, minor, or patch).

    Args:
        bump (VersionParts): Enum representing the version part to be bumped.
    """
    version = Version()
    version.from_file(version_file)
    older_version = version.version
    version.bump(bump.value)
    version.update_file(version_file)
    print(f"Bumped up from {older_version} ---> {version.version}")
    return version.version


if __name__ == "__main__":
    app()
