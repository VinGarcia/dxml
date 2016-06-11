# This project was forked from dict2xml
"""
  Simple xml serializer.

  @author Reimund Trost 2013

  Example:
   
   
  Output:
    
    <family name="The Andersson&apos;s" size="4">
      <children total-age="62">
        <child name="Tom" sex="male"/>
        <child name="Betty" sex="female">
          <grandchildren>
            <grandchild name="herbert" sex="male"/>
            <grandchild name="lisa" sex="female"/>
          </grandchildren>
        </child>
      </children>
    </family>
"""

from sys import version_info
py2 = version_info[0] == 2

charmap = [
  # Note that `&->&amp;` must be the first item.
  ('&', '&amp'),
  ('<', '&lt;'),
  ('>', '&gt;'),
  ('"', '&quot;'),
  ("'", '&apos;'),
  ('\n', '&#xA;')
]

def pushTop(stack, d, root_node, parent, indent):
  top = {
    'obj': d,
    'root': 'objects' if root_node == None else root_node,
    'xml': '',
    'children': [],
    'parent': parent,
    'indent': parent['indent']+indent if parent else ''
  }
  stack.append(top)
  return top

def popTop(stack, indent):
  top = stack.pop()

  # Prepare to build the xml
  end_tag = '>' if len(top['children']) > 0 else '/>'

  # Build the xml:
  top['xml'] = (top['indent'] if indent else '') + '<' + top['root'] + top['xml'] + end_tag

  if len(top['children']) > 0:
    for child in top['children']:
      top['xml'] += ('\n' if indent else '') + child
      
    top['xml'] += ('\n'+top['indent'] if indent else '') + '</' + top['root'] + '>'

  if top['parent']:
    top['parent']['children'].append(top['xml'])
    return stack[-1]
  else:
    return top;

def isValidList(l):
  for v in l:
    if not isinstance(v, dict) and not isValidList(v):
      return False

  return True

def listToStr(l):
  text = ''
  for v in l:
    if py2 and type(v) == unicode:
      text += '&lt;' + v + '&gt;'
    else:
      text += '&lt;' + str(v) + '&gt;'

  return text

def toXml(d, root=None, indent=None):
  stack = []
  top = pushTop(stack, d, root, None, indent)

  if type(indent) == int:
    indent = ' ' * indent

  while True:
    if 'ready' not in top:
      top['ready'] = True
      if isinstance(top['obj'], dict):
        for key, value in dict.items(top['obj']):
          if isinstance(value, dict):
            pushTop(stack, value, key, top, indent)
          elif isinstance(value, list):
            if isValidList(value):
              for item in value:
                pushTop(stack, item, key, top, indent)
            else:
              top['xml'] += ' ' + key + '="' + listToStr(value) + '"'
          elif value != None:
            # Check for invalid characters:
            for char, code in charmap:
              assert(char not in key)
              if py2 and type(value) == unicode:
                value = value.replace(unicode(char), unicode(code))
              else:
                value = str(value).replace(char, code)
            # Add attributes:
            top['xml'] = top['xml'] + ' ' + key + '="' + value + '"'
        top = stack[-1]
      else:
        raise Exception(
            "Invalid type `%s` to be converted to XML!" % type(top['obj']))

    if 'ready' in top:
      if top['parent'] == None:
        break
      else:
        top = popTop(stack, indent)
    
  return popTop(stack, indent)['xml']

if __name__ == '__main__':

  mydict = {
    'name': 'The Andersson\'s',
    'family-size': 4,
    'children': {
      'total-children': 3,
      'child': [
        { 'name': 'Tom', 'sex': 'male', },
        { 'name': 'Max', 'sex': 'male', },
        {
          'name': 'Betty',
          'sex': 'female',
          'grandchildren': {
            'grandchild': [
              { 'name': 'herbert', 'sex': 'male' },
              { 'name': 'lisa', 'sex': 'female' }
            ]
          }
        }
      ]
    }
  }
   
  print(toXml(mydict, 'family', indent=2))



