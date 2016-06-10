# This project was forked from dict2xml
"""
  Simple xml serializer.

  @author Reimund Trost 2013

  Example:
   
  mydict = {
    'name': 'The Andersson\'s',
    'size': 4,
    'children': {
      'total-age': 62,
      'child': [
        { 'name': 'Tom', 'sex': 'male', },
        {
          'name': 'Betty',
          'sex': 'female',
          'grandchildren': {
            'grandchild': [
              { 'name': 'herbert', 'sex': 'male', },
              { 'name': 'lisa', 'sex': 'female', }
            ]
          },
        }
      ]
    },
  }
   
  print(toXml(mydict, 'family'))
   
  Output:
    
    <family name="The Andersson's" size="4">
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

def pushTop(stack, d, root_node):
  root = 'objects' if None == root_node else root_node
  top = {
    'obj': d,
    'wrap': False if None == root_node or isinstance(d, list) else True,
    'root': root,
    'root_singular': root[:-1] if 's' == root[-1] and None == root_node else root,
    'xml': '',
    'children': [],
    'parent': stack[0] if len(stack) > 0 else None
  }
  stack.append(top)
  return top

def popTop(stack):
  top = stack.pop()

  end_tag = '>' if 0 < len(top['children']) else '/>'

  if top['wrap'] or isinstance(top['obj'], dict):
    top['xml'] = '<' + top['root'] + top['xml'] + end_tag

  if 0 < len(top['children']):
    for child in top['children']:
      top['xml'] = top['xml'] + child

    if top['wrap'] or isinstance(top['obj'], dict):
      top['xml'] = top['xml'] + '</' + top['root'] + '>'

  return top;

def isValidList(l):
  if not isinstance(l, list):
    return False

  for v in l:
    if not isinstance(v, dict) or isValidList(v):
      return False

def listToStr(l):
  text = ''
  for v in l:
    if py2 and type(v) == unicode:
      text += '&lt;' + v + '&gt;'
    else:
      text += '&lt;' + str(v) + '&gt;'

  return text

def toXml(d, root_node=None):
  stack = []
  top = pushTop(stack, d, root_node)
  
  while True:
    if 'ready' not in top:
      top['ready'] = True
      if isinstance(top['obj'], dict):
        for key, value in dict.items(top['obj']):
          if isinstance(value, dict):
            top = pushTop(stack, value, key)
          elif isinstance(value, list):
            if isValidList(value):
              top = pushTop(stack, value, key)
            else:
              top['xml'] += ' ' + key + '="' + listToStr(value) + '"'
          elif value != None:
            # Check for invalid characters:
            for char, code in charmap:
              assert(char not in key)
              value = str(value).replace(char, code)
            # Add attributes:
            top['xml'] = top['xml'] + ' ' + key + '="' + value + '"'
      elif isinstance(top['obj'], list):
        for value in top['obj']:
          top = pushTop(stack, value, top['root_singular'])
      else:
        raise Exception(
            "Invalid type `%s` to be converted to XML!" % type(top['obj']))

    if 'ready' in top:
      if top['parent'] == None:
        break
      else:
        top = popTop(stack)
        top['parent']['children'].append('\n'+top['xml'])
        top = stack[-1]
    
  return popTop(stack)['xml']

if __name__ == '__main__':
  
  a = {
    'batata*' : 'feijoada'
  }

  toXml(a)






