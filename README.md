
## Usage:

```python
> from dxml import toXml
> toXml({'a': 10})
'<object a="10"/>'

> toXml({'a': 10}, root_node='base')
'<base a="10"/>'

> toXml({'a': 10, 'b': {'c': 'child_attr'}})
'<objects a="10"><b c="child_attr"/></objects>'

> xml = toXml({'a': 10, 'b': {'c': 'child_attr'}}, indent=2)
> print(xml)
<objects a="10">
  <b c="child_attr"/>
</objects>
```

## Features:

- unicode compatible
- escape characters such as '&','<','>' as '&amp;', '&lt;', etc.
- accepts lists of dicts
- provides optional indentation (with the `indent` argument)
- work with iterations instead of recursion (won't reach stack limit)
- easy to use



