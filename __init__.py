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
def toXml(d, root_node=None):
  wrap          =     False if None == root_node or isinstance(d, list) else True
  root          = 'objects' if None == root_node else root_node
  root_singular = root[:-1] if 's' == root[-1] and None == root_node else root
  xml           = ''
  children      = []

  charmap = [
    # Note that `&->&amp;` must be the first item.
    ('&', '&amp'),
    ('<', '&lt;'),
    ('>', '&gt;'),
    ('"', '&quot;'),
    ("'", '&apos;'),
    ('\n', '&#xA;')
  ]
  

  if isinstance(d, dict):
    for key, value in dict.items(d):
      if isinstance(value, dict):
        children.append(toXml(value, key))
      elif isinstance(value, list):
        children.append(toXml(value, key))
      else:
        for char, code in charmap:
          assert(char not in key)
          value = str(value).replace(char, code)

        xml = xml + ' ' + key + '="' + value + '"'
  else:
    for value in d:
      children.append(toXml(value, root_singular))

  end_tag = '>' if 0 < len(children) else '/>'

  if wrap or isinstance(d, dict):
    xml = '<' + root + xml + end_tag

  if 0 < len(children):
    for child in children:
      xml = xml + child

    if wrap or isinstance(d, dict):
      xml = xml + '</' + root + '>'
    
  return xml

if __name__ == '__main__':
  
  a = {
    'batata*' : 'feijoada'
  }

  toXml(a)






