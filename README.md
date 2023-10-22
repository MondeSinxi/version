# Version

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

There are two command line arguments for `version`, these are `get-version` and `bump-version`. When a patch has been made, to bump up the version run

```
version bump-version patch
```

If the current version is 0.1.0 it will bumped up tp 0.1.1. If a file with the version specified in a file, e.g. `VERSION`, patth the `--version-file` option to the `bump-version` argument. If no arument is supplied, `version` will assume a `pyproject.toml` file is present and bump it up there. 

## Contributing 

All pull requests are welcome.

## Licence

[MIT](https://choosealicense.com/licenses/mit/)
