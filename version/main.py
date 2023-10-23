"""
Updates semantic version numbers.
"""

import configparser
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional

import typer
from rich import print as rprint

app = typer.Typer()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class VersionParts(Enum):
    """
    Enum representing version parts: major, minor, and patch.
    """

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


@dataclass
class Version:
    """
    Represents a version with major, minor, and patch components.
    """

    major: int = 0
    minor: int = 0
    patch: int = 0

    def from_file(
        self, version_file: Optional[str] = None, pyproject_file: Optional[str] = None
    ) -> None:
        """
        Load version components from a file.

        Args:
            file (str): Path to the version file.

        Raises:
            FileNotFoundError: If the specified file is not found.
        """
        version_str = self.get_version_str(version_file, pyproject_file)
        self.major, self.minor, self.patch = self._parse_split_versions(version_str)

    def get_version_str(
        self, version_file: Optional[str] = None, pyproject_file: Optional[str] = None
    ) -> str:
        """
        Parses a file to get the version string representasion

        Args:
            file (str | Path): Path to version file.

        Returns:
            str
        """
        if version_file:
            version_file_path = Path(version_file)
            if version_file_path.exists():
                with open(version_file_path, "r", encoding="utf-8") as file:
                    version_str = file.read()
                return version_str.strip()
        if pyproject_file:
            return self.get_version_from_toml(pyproject_file)
        raise FileNotFoundError("No files with version found.")

    def get_version_from_toml(self, pyproject_file: str) -> str:
        """Get version from toml file."""
        config = configparser.ConfigParser()
        config.read(pyproject_file)
        try:
            version_str = config["tool.poetry"]["version"]
        except KeyError:
            logger.exception("Could not ger version from pyproject")
            sys.exit()
        return version_str.replace('"', "")

    def _parse_split_versions(self, version_str: str) -> List[int]:
        """Split sub-versions to list of integers."""
        version = version_str.split(".")
        assert (
            len(version) == 3
        ), f"format of the version must be x.y.z, got {version_str}"
        try:
            return [int(v) for v in version]
        except ValueError:
            logger.exception("Cannot convert parts to integers %s", version_str)
            sys.exit()

    def upgrade_major(self) -> None:
        """Bump up the major version."""
        self.major += 1
        self.minor = 0
        self.patch = 0

    def upgrade_minor(self) -> None:
        """Bump up the minor version."""
        self.minor += 1
        self.patch = 0

    def upgrade_patch(self) -> None:
        """Bump up the patch version."""
        self.patch += 1

    def bump(self, subtype):
        """Checks which version should be bumped."""
        if subtype == "major":
            self.upgrade_major()
        if subtype == "minor":
            self.upgrade_minor()
        if subtype == "patch":
            self.upgrade_patch()

    def update_file(
        self, version_file: Optional[str] = None, pyproject_file: Optional[str] = None
    ) -> None:
        """Update file with new version."""
        if version_file is not None:
            version_file_path = Path(version_file)
            if version_file_path.exists():
                with open(version_file_path, "w", encoding="utf-8") as file:
                    file.write(self.version)
        if pyproject_file is not None:
            if Path(pyproject_file).exists():
                config = configparser.ConfigParser()
                config.read(pyproject_file)
                config["tool.poetry"]["version"] = self.version
                with open(pyproject_file, "w", encoding="utf-8") as configfile:
                    version_str = f'"{self.version}"'
                    configfile.write(version_str)

    @property
    def version(self) -> str:
        """Get the version."""
        return f"{self.major}.{self.minor}.{self.patch}"


@app.command()
def get_version(
    version_file: Optional[str] = None, pyproject_file: Optional[str] = None
):
    """
    Command to get the current version and display it.
    """
    if version_file is None and pyproject_file is None:
        raise FileNotFoundError("pyproject.yml  or version file not found.")
    version = Version()
    version.from_file(version_file, pyproject_file)
    rprint(f"VERSION: {version.version}")
    return version.version


@app.command()
def bump_version(
    bump: VersionParts,
    version_file: Optional[str] = None,
    pyproject_file: Optional[str] = None,
) -> str:
    """
    Command to bump the specified version part (major, minor, or patch).

    Args:
        bump (VersionParts): Enum representing the version part to be bumped.
    """
    if version_file is None and pyproject_file is None:
        raise FileNotFoundError("pyproject.yml  or version file not found.")
    version = Version()
    version.from_file(version_file, pyproject_file)
    older_version = version.version
    version.bump(bump.value)
    if version_file or pyproject_file:
        version.update_file(version_file, pyproject_file)
    rprint(f"Bumped up from {older_version} ---> {version.version}")
    return version.version
