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

import re

from sys import version_info
py2 = version_info[0] == 2

namecheck_re = re.compile('\A[:A-Z_a-z][:A-Z_a-z0-9.-]*\Z')

def namecheck(key, errors):
  if not namecheck_re.match(key):
    if errors == "strict":
      raise Exception("Invalid characters in attribute name: %s" % key)
    elif errors == "replace":
      key = re.sub('[^0-9a-zA-Z_-:]', '?', key)
    elif errors == "ignore":
      pass

  return key


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
    'root': root_node,
    'xml': '',
    'children': [],
    'parent': parent,
    'indent': parent['indent']+indent if parent and indent else ''
  }
  stack.append(top)
  return top

def popTop(stack, indent):
  top = stack.pop()

  # Prepare to build the xml
  end_tag = '>' if len(top['children']) > 0 else '/>'

  # Build the xml:
  if isinstance(top['obj'], dict):
    top['xml'] = (top['indent'] if indent else '') + '<' + top['root'] + top['xml'] + end_tag

    if len(top['children']) > 0:
      for child in reversed(top['children']):
        top['xml'] += ('\n' if indent else '') + child
        
      top['xml'] += ('\n'+top['indent'] if indent else '') + '</' + top['root'] + '>'
  else:
    top['xml'] = (top['indent'] if indent else '') + '"' + top['xml'] + '"'

  if top['parent']:
    top['parent']['children'].append(top['xml'])
    return stack[-1]
  else:
    return top;

def makeValidList(l):
  vList = []

  for v in l:
    if isinstance(v, dict):
      vList.append(v)
    elif isinstance(v, list):
      vList.extend( makeValidList(v) )
    elif py2 and type(v) == unicode:
      vList.append(v)
    else:
      vList.append(str(v))

  return vList

def makeValidString(value):
  for char, code in charmap:
    if py2 and type(value) == unicode:
      value = value.replace(unicode(char), unicode(code))
    else:
      value = str(value).replace(char, code)
  return value

def listToStr(l):
  text = ''
  for v in l:
    if py2 and type(v) == unicode:
      text += '&lt;' + v + '&gt;'
    else:
      text += '&lt;' + str(v) + '&gt;'

  return text

def toXml(d, root='object', indent=None, errors='strict'):
  stack = []
  root = namecheck(root, errors)
  top = pushTop(stack, d, root, None, indent)

  if type(indent) == int:
    indent = ' ' * indent

  while True:
    if 'ready' not in top:
      top['ready'] = True
      if isinstance(top['obj'], dict):
        for key, value in dict.items(top['obj']):
          key = namecheck(key, errors)
          if isinstance(value, dict):
            pushTop(stack, value, key, top, indent)
          elif isinstance(value, list):
            for item in makeValidList(value):
              pushTop(stack, item, key, top, indent)
          elif value != None:
            # Add attributes:
            top['xml'] = ' ' + key + '="' + makeValidString(value) + '"' + top['xml']
        top = stack[-1]
      else:
        top['xml'] = makeValidString(top['obj'])

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
        "first child:",
        { 'name': 'Tom', 'sex': 'male', },
        "second child:",
        { 'name': 'Max', 'sex': 'male', },
        "third child:",
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

  print(toXml({ 'tag': [ 'text_node' ] }))



