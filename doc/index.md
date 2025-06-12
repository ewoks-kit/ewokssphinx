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

#### Basic use

The `ewokstasks` directive will generate documentation automatically for all Ewoks tasks (be it `class`, `method` or `ppfmethod`) contained in the module. As for `autodoc`, the module must be importable.


_Example_: 
```
.. ewokstasks:: ewoksxrpd.tasks.integrate
```

It is also possible to give a pattern for recursive generation. For example, The following command will generate documentation for all tasks contained in the modules of `ewoksxrpd.tasks`:

```
.. ewokstasks:: ewoksxrpd.tasks.*
```

```{caution}
The `ewokstasks` directive adds the name of the tasks as title. That means it may break the title order and hierarchy of the document if placed in another directive (admonition or other). This may lead to errors in the generation of table of contents, for example.

Therefore, the safest use of the directive is to place it in the main section of the document.
```

```{seealso}
The [Examples page](./examples) contains real examples with Python code, RST syntax and the associated Sphinx output for all task types.  
```

#### Options

- `:task-type:`: (`class`, `method` or `ppfmethod`)

    Generates documentation only for the specified task type.

    _Example_:

    To generate documentation for the Ewoks **class** tasks in `ewoksxrpd.tasks.integrate`: 

    ```
    .. ewokstasks:: ewoksxrpd.tasks.integrate
        :task-type: class
    ```

- `:ignore-import-error:`

    Print a warning instead of raising an error when an import fails.

    _Example_:
    
    ```
    .. ewokstasks:: ewoksxrpd.tasks.integrate
        :ignore-import-error:
    ```


```{toctree}
:hidden:

changelog
examples
```
