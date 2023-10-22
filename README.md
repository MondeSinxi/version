# Version Bump Tool

A tool for bumping up [semantic versions](https://semver.org/).

## Installation

This has not yet been published to PyPi, to use is clone the repository and install

```
poetry install
```

## Usage


To get help run:
```
version --help
```

The tool offers two primary commands: get-version and bump-version. After making a patch, bump up the version using:

```
version bump-version patch
```

For example, if the current version is 0.1.0, it will be bumped up to 0.1.1. If a file with the version specified in it is present (e.g., VERSION), pass the --version-file option to the bump-version argument. If no argument is supplied, the tool will assume a pyproject.toml file is present and update the version there.


## Contributing 

All pull requests are welcome.

## Licence

This project is licensed under the [MIT Lincence](https://choosealicense.com/licenses/mit/).
