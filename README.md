# pyjson
A  Recursive-Descent JSON parser written in python

## Usage
```python
In [1]: import pyjson

In [2]: json_text = '["foo", {"bar": ["baz", null, 1.0, 2]}]'

In [3]: pyjson.load_from_text(json_text)
Out[3]: ['foo', OrderedDict([('bar', ['baz', None, 1.0, 2])])]

In [4]: json_file = './test/pass1.json'

In [5]: pyjson.load_from_file(json_file)
Out[5]:
['JSON Test Pattern pass1',
 OrderedDict([('object with 1 member', ['array with 1 element'])]),
 OrderedDict(),
 [],
 -42,
 True,
 False,
 None,
 OrderedDict([('integer', 1234567890),
              ('real', -9876.54321),
              ('e', 1.23456789e-13),
              ('E', 1.23456789e+34),
              ('', 2.3456789012e+76),
              ('zero', 0),
              ('one', 1),
              ('space', ' '),
              ('quote', '\\"'),
              ('backslash', '\\\\'),
              ('controls', '\\b\\f\\n\\r\\t'),
              ('slash', '/ & \\/'),
              ('alpha', 'abcdefghijklmnopqrstuvwyz'),
              ('ALPHA', 'ABCDEFGHIJKLMNOPQRSTUVWYZ'),
              ('digit', '0123456789'),
              ('0123456789', 'digit'),
              ('special', "`1~!@#$%^&*()_+-={':[,]}|;.</>?"),
              ('hex', '\\u0123\\u4567\\u89AB\\uCDEF\\uabcd\\uef4A'),
              ('true', True),
              ('false', False),
              ('null', None),
              ('array', []),
              ('object', OrderedDict()),
              ('address', '50 St. James Street'),
              ('url', 'http://www.JSON.org/'),
              ('comment', '// /* <!-- --'),
              ('# -- --> */', ' '),
              (' s p a c e d ', [1, 2, 3, 4, 5, 6, 7]),
              ('compact', [1, 2, 3, 4, 5, 6, 7]),
              ('jsontext',
               '{\\"object with 1 member\\":[\\"array with 1 element\\"]}'),
              ('quotes', '&#34; \\u0022 %22 0x22 034 &#x22;'),
              ('\\/\\\\\\"\\uCAFE\\uBABE\\uAB98\\uFCDE\\ubcda\\uef4A\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?',
               'A key can be any string')]),
 0.5,
 98.6,
 99.44,
 1066,
 10.0,
 1.0,
 0.1,
 1.0,
 2.0,
 2.0,
 'rosebud']
```

## TODO
* escape character support
