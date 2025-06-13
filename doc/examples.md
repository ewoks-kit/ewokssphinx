# Examples

## Class

::::{tab-set}

:::{tab-item} Python

```{literalinclude} ../src/ewokssphinx/tests/dummy_tasks.py
:language: python
:lines: 1-13
```

:::

:::{tab-item} reST

```rst
.. ewokstasks:: ewokssphinx.tests.dummy_tasks
    :task-type: class
```

:::

:::{tab-item} Sphinx

```{ewokstasks} ewokssphinx.tests.dummy_tasks
:task-type: class
```

:::

::::


## Class with pydantic model

::::{tab-set}

:::{tab-item} Python

```{literalinclude} ../src/ewokssphinx/tests/dummy_tasks_pydantic.py
:language: python
```

:::

:::{tab-item} reST

```rst
.. ewokstasks:: ewokssphinx.tests.dummy_tasks_pydantic
    :task-type: class
```

:::

:::{tab-item} Sphinx

```{ewokstasks} ewokssphinx.tests.dummy_tasks_pydantic
:task-type: class
```

:::

::::

:::{tip}

To use attribute docstrings instead of `description` to document the fields, set the `use_attribute_docstrings` of the `ConfigDict` to `True`

```python
from ewokscore.model import BaseInputModel
from pydantic import ConfigDict

class Inputs(BaseInputModel):
    model_config = ConfigDict(use_attribute_docstrings=True) 
    
    planet: str = "Earth"
    """The planet on which the search will be made"""

    ...
```

See [the relevant page in the Pydantic documentation](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.use_attribute_docstrings)

:::


## Method

::::{tab-set}

:::{tab-item} Python

```{literalinclude} ../src/ewokssphinx/tests/dummy_tasks.py
:language: python
:lines: 16-23
```

:::

:::{tab-item} reST

```rst
.. ewokstasks:: ewokssphinx.tests.dummy_tasks
    :task-type: method
```

:::

:::{tab-item} Sphinx

```{ewokstasks} ewokssphinx.tests.dummy_tasks
:task-type: method
```

:::

::::


## Ppfmethod

::::{tab-set}

:::{tab-item} Python

```{literalinclude} ../src/ewokssphinx/tests/dummy_tasks.py
:language: python
:lines: 20-23
```

:::

:::{tab-item} reST

```rst
.. ewokstasks:: ewokssphinx.tests.dummy_tasks
    :task-type: ppfmethod
```

:::

:::{tab-item} Sphinx

```{ewokstasks} ewokssphinx.tests.dummy_tasks
:task-type: ppfmethod
```

:::

::::