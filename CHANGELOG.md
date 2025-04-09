# CHANGELOG.md

## 0.4.0

- ✨ When rendered by the `ewokstasks` directive, the name of `ppfmethod` tasks are now the module name instead of the ambiguous `run` function name.

## 0.3.0

- **⚠️ Breaking change:** `:task_type:` option was renamed `:task-type:`
- ✨ New option `:ignore-import-error:` to ignore import errors raised when tasks are discovered by the `ewokstasks` directive
- 🐛 `ewokstasks` directive no longer include tasks whose name starts with a `_`

## 0.2.0

- ✨ Task descriptions are now parsed with RST rather than stringified.
- ✨ `ewokstasks` directive now generates documentation for all task types (`class`, `method` and `ppfmethod`).
- ✨ New `:task_type:` option for `ewokstasks` to generate documentation for only one task type
- 🐛 Fix inconsistent order of class task input and output fields

## 0.1.1

Fix title level of generated task names

## 0.1.0

Add `ewokstasks` directive
