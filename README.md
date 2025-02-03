# ewokssphinx

A set of Sphinx directives for Ewoks

## Ewoks tasks directive

The `ewokstasks` directive will generate documentation automatically for the Ewoks **class** tasks contained in the module. As for `autodoc`, the module must be importable.

_Example_: 
```
.. ewokstasks:: ewoksxrpd.tasks.integrate
```

It is also possible to give a pattern for recursive generation. For example, The following command will generate documentation for all class tasks contained in the modules of `ewoksxrpd.tasks`:

```
.. ewokstasks:: ewoksxrpd.tasks.*
```