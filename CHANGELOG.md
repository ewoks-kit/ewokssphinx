# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-12-02

### Added

- New Sphinx directive setup option `ewokssphinx_task_cache_path`: Ewoks task caching.
- New Sphinx directive setup option `ewokssphinx_ignore_discovery_error`: Ignore task discovery errors.

### Changed

- The task section Sphinx id is now the task identifier not the task name.

## [1.0.0] - 2025-06-16

### Removed

- No longer supports Python 3.8 and Python 3.9.

### Added

- Add rich display of inputs `ewokstasks` directive when specified with a pydantic model: type annotation, description and examples.

### Changed

- `ewokstasks` directive now displays inputs and outputs as lists rather than on a single line.

## [0.4.0] - 2025-04-09

### Changed

- When rendered by the `ewokstasks` directive, the name of `ppfmethod` tasks are now the module name instead of the ambiguous `run` function name.

## [0.3.0] - 2025-04-07

### Removed

- `:task_type:` option was renamed `:task-type:`.

### Added

- New option `:ignore-import-error:` to ignore import errors raised when tasks are discovered by the `ewokstasks` directive.

### Fixed

- `ewokstasks` directive no longer include tasks whose name starts with a `_`.

## [0.2.0] - 2025-02-18

### Added

- `ewokstasks` directive now generates documentation for all task types (`class`, `method` and `ppfmethod`).
- New `:task_type:` option for `ewokstasks` to generate documentation for only one task type.

### Changed

- Task descriptions are now parsed with RST rather than stringified.

### Fixed

- Fix inconsistent order of class task input and output fields.

## [0.1.1] - 2025-02-03

### Fixed

- Fix title level of generated task names.

## [0.1.0] - 2025-02-03

### Added

- Add `ewokstasks` directive.

[unreleased]: https://gitlab.esrf.fr/workflow/ewoks/ewokssphinx/compare/v2.0.0...HEAD
[2.0.0]: https://gitlab.esrf.fr/workflow/ewoks/ewokssphinx/compare/v1.0.0...v2.0.0
[1.0.0]: https://gitlab.esrf.fr/workflow/ewoks/ewokssphinx/compare/v0.4.0...v1.0.0
[0.4.0]: https://gitlab.esrf.fr/workflow/ewoks/ewokssphinx/compare/v0.3.0...v0.4.0
[0.3.0]: https://gitlab.esrf.fr/workflow/ewoks/ewokssphinx/compare/v0.2.0...v0.3.0
[0.2.0]: https://gitlab.esrf.fr/workflow/ewoks/ewokssphinx/compare/v0.1.1...v0.2.0
[0.1.1]: https://gitlab.esrf.fr/workflow/ewoks/ewokssphinx/compare/v0.1.0...v0.1.1
[0.1.0]: https://gitlab.esrf.fr/workflow/ewoks/ewokssphinx/-/tags/v0.1.0
