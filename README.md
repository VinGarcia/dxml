
## Usage:

```python
> import dxml
> dxml.dumps({'a': 10})
'<object a="10"/>'

> dxml.dumps({'a': 10}, root_node='base')
'<base a="10"/>'

> dxml.dumps({'a': 10, 'b': {'c': 'child_attr'}})
'<objects a="10"><b c="child_attr"/></objects>'

> xml = dxml.dumps({'a': 10, 'b': {'c': 'child_attr'}}, indent=2)
> print(xml)
<objects a="10">
  <b c="child_attr"/>
</objects>
```

## Features:

- unicode compatible even on python2
- escape characters such as '&','<','>' as '&amp;', '&lt;', etc.
- safe against xml injection
- accepts lists of dicts
- provides optional indentation (with the `indent` argument)
- work with iterations instead of recursion (won't reach stack limit)
- easy to use (just like the built-in json module)

