# ewokssphinx

A set of Sphinx directives for Ewoks

## Quick start

```bash
pip install ewokssphinx
```

Then, add `ewokssphinx` to the list of `extensions` in the Sphinx configuration file:

```python
# conf.py

...

extensions = [
    ...,
    "ewokssphinx"
]
```

## Contents

There is only one directive for now.

### Ewoks tasks directive

The `ewokstasks` directive will generate documentation automatically for the Ewoks **class** tasks contained in the module. As for `autodoc`, the module must be importable.

_Example_: 
```
.. ewokstasks:: ewoksxrpd.tasks.integrate
```

It is also possible to give a pattern for recursive generation. For example, The following command will generate documentation for all class tasks contained in the modules of `ewoksxrpd.tasks`:

```
.. ewokstasks:: ewoksxrpd.tasks.*
```