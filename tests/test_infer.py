"""Tests."""

from pybqinfer import infer


def test_infer_schema1():
  data = {'name': 'Koichiro Okamoto', 'age': 34, 'point': 34.333, 'cert': True}
  schema = infer.infer_schema(data)
  assert len(schema) == 4

  name = schema['name']
  assert name['name'] == 'name'
  assert name['type'] == 'STRING'
  assert name['mode'] == 'NULLABLE'

  age = schema['age']
  assert age['name'] == 'age'
  assert age['type'] == 'INTEGER'
  assert age['mode'] == 'NULLABLE'

  point = schema['point']
  assert point['name'] == 'point'
  assert point['type'] == 'FLOAT'
  assert point['mode'] == 'NULLABLE'

  cert = schema['cert']
  assert cert['name'] == 'cert'
  assert cert['type'] == 'BOOLEAN'
  assert cert['mode'] == 'NULLABLE'


def test_infer_schema2():
  import json
  data = {'name': 'Koichiro Okamoto', 'age': 34, 'point': 34.333, 'cert': True}
  schema = infer.infer_schema(json.dumps(data))
  assert len(schema) == 4

  name = schema['name']
  assert name['name'] == 'name'
  assert name['type'] == 'STRING'
  assert name['mode'] == 'NULLABLE'

  age = schema['age']
  assert age['name'] == 'age'
  assert age['type'] == 'INTEGER'
  assert age['mode'] == 'NULLABLE'

  point = schema['point']
  assert point['name'] == 'point'
  assert point['type'] == 'FLOAT'
  assert point['mode'] == 'NULLABLE'

  cert = schema['cert']
  assert cert['name'] == 'cert'
  assert cert['type'] == 'BOOLEAN'
  assert cert['mode'] == 'NULLABLE'


def test_infer_schema3():
  import json
  data = {
      'name':
      'Koichiro Okamoto',
      'age':
      34,
      'point':
      34.333,
      'cert':
      True,
      'family': [{
          'relation': 'mother',
          'age': 60
      }, {
          'relation': 'brother',
          'age': 40
      }],
      'hobby': ['music', 'programming', 'sing'],
      'job': {
          'name': 'Software Engineer',
          'current': True,
          'span': 3.5
      }
  }

  schema = infer.infer_schema(data)
  assert len(schema) == 7

  name = schema['name']
  assert name['name'] == 'name'
  assert name['type'] == 'STRING'
  assert name['mode'] == 'NULLABLE'

  age = schema['age']
  assert age['name'] == 'age'
  assert age['type'] == 'INTEGER'
  assert age['mode'] == 'NULLABLE'

  point = schema['point']
  assert point['name'] == 'point'
  assert point['type'] == 'FLOAT'
  assert point['mode'] == 'NULLABLE'

  cert = schema['cert']
  assert cert['name'] == 'cert'
  assert cert['type'] == 'BOOLEAN'
  assert cert['mode'] == 'NULLABLE'

  family = schema['family']
  assert family['name'] == 'family'
  assert family['type'] == 'RECORD'
  assert family['mode'] == 'REPEATED'
  assert family['fields'] == {
      'relation': {
          'name': 'relation',
          'type': 'STRING',
          'mode': 'NULLABLE'
      },
      'age': {
          'name': 'age',
          'type': 'INTEGER',
          'mode': 'NULLABLE'
      }
  }

  hobby = schema['hobby']
  assert hobby['name'] == 'hobby'
  assert hobby['type'] == 'STRING'
  assert hobby['mode'] == 'REPEATED'

  job = schema['job']
  assert job['name'] == 'job'
  assert job['type'] == 'RECORD'
  assert job['mode'] == 'NULLABLE'
  assert job['fields'] == {
      'name': {
          'name': 'name',
          'type': 'STRING',
          'mode': 'NULLABLE'
      },
      'current': {
          'name': 'current',
          'type': 'BOOLEAN',
          'mode': 'NULLABLE'
      },
      'span': {
          'name': 'span',
          'type': 'FLOAT',
          'mode': 'NULLABLE'
      }
  }


def test_get_infered_schema():
  data = {
      'name':
      'Koichiro Okamoto',
      'age':
      34,
      'point':
      34.333,
      'cert':
      True,
      'family': [{
          'relation': 'mother',
          'age': 60
      }, {
          'relation': 'brother',
          'age': 40
      }],
      'hobby': ['music', 'programming', 'sing'],
      'job': {
          'name': 'Software Engineer',
          'current': True,
          'span': 3.5
      }
  }

  schema = infer.get_infered_schema(data)
  assert 'fields' in schema
  schema = schema['fields']
  assert len(schema) == 7

  name = schema[0]
  assert name['name'] == 'name'
  assert name['type'] == 'STRING'
  assert name['mode'] == 'NULLABLE'

  age = schema[1]
  assert age['name'] == 'age'
  assert age['type'] == 'INTEGER'
  assert age['mode'] == 'NULLABLE'

  point = schema[2]
  assert point['name'] == 'point'
  assert point['type'] == 'FLOAT'
  assert point['mode'] == 'NULLABLE'

  cert = schema[3]
  assert cert['name'] == 'cert'
  assert cert['type'] == 'BOOLEAN'
  assert cert['mode'] == 'NULLABLE'

  family = schema[4]
  assert family['name'] == 'family'
  assert family['type'] == 'RECORD'
  assert family['mode'] == 'REPEATED'
  assert family['fields'] == [{
      'name': 'relation',
      'type': 'STRING',
      'mode': 'NULLABLE'
  }, {
      'name': 'age',
      'type': 'INTEGER',
      'mode': 'NULLABLE'
  }]

  hobby = schema[5]
  assert hobby['name'] == 'hobby'
  assert hobby['type'] == 'STRING'
  assert hobby['mode'] == 'REPEATED'

  job = schema[6]
  assert job['name'] == 'job'
  assert job['type'] == 'RECORD'
  assert job['mode'] == 'NULLABLE'
  assert job['fields'] == [{
      'name': 'name',
      'type': 'STRING',
      'mode': 'NULLABLE'
  }, {
      'name': 'current',
      'type': 'BOOLEAN',
      'mode': 'NULLABLE'
  }, {
      'name': 'span',
      'type': 'FLOAT',
      'mode': 'NULLABLE'
  }]
