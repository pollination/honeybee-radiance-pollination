# Pollination Honeybee Radiance plugin.

The honeybee-radiance plugin adds daylight simulation functions to Pollination.

## Dependencies:

- `honeybee-radiance` Python package. [PyPI](https://pypi.org/project/honeybee-radiance/), [source](https://github.com/ladybug-tools/honeybee-radiance)
- `Radiance` ([website](https://www.radiance-online.org/)) libraries.


## Load as Queenbee plugin

Install the package using `pip install .`. Then you can use `queenbee_dsl` to load the
package as a Queenbee Plugin.

```python
from queenbee_dsl.package import load

plugin = load(python_package)
print(plugin.yaml())
```
