"""Inference BigQuery schema from sample data."""

from enum import Enum
import json


class SchemaNotDefined(Exception):

  def __init__(self, detail):
    super().__init__()
    self.detail = detail


class Type(Enum):
  """BigQuery field data type."""
  STRING = 0
  INTEGER = 1
  FLOAT = 2
  BOOLEAN = 3
  RECORD = 4
  DATE = 5
  DATETIME = 6
  TIME = 7
  TIMESTAMP = 8


class Mode(Enum):
  """BigQuery field mode."""
  NULLABLE = 0
  REPEATED = 1
  REQUIRED = 2


def get_schema_from_str(k, s):
  """Get schema from string. 
  String must be fullmatched to each pattern.

  Args:
    k: Key of dictionary.
    s: String.

  Returns:
    String schema.
  """
  import re
  regex_list = [
      (Type.DATE, r'\d{4}-\d{1,2}-\d{1,2}'),
      (Type.DATETIME,
       r'\d{4}-\d{1,2}-\d{1,2}[\s|T]\d{1,2}:\d{1,2}:\d{1,2}(\.\d{1,6})?'),
      (Type.TIME, r'\d{1,2}:\d{1,2}:\d{1,2}(\.\d{1,6})?'),
      (Type.TIMESTAMP,
       r'\d{4}-\d{1,2}-\d{1,2}[\s|T]\d{1,2}:\d{1,2}:\d{1,2}(\.\d{1,6})?(Z|[-|+]\d{1,2}(:\d{1,2})?)?'
      )
  ]
  for regex in regex_list:
    t, pattern = regex
    ret = re.fullmatch(pattern, s)
    if ret:
      return {'name': k, 'type': t.name, 'mode': Mode.NULLABLE.name}

  return {'name': k, 'type': Type.STRING.name, 'mode': Mode.NULLABLE.name}


def get_schema_from_list(k, l):
  """Get schema from list.
  
  Args:
    k: Key of dictionary.
    l: List.
  
  Returns:
    List field schema.
  """
  list_schema = {}
  for elem in l:
    t = type(elem)
    if t == str:
      list_schema = get_schema_from_str(k, elem)
      list_schema['mode'] = Mode.REPEATED.name
    elif t == int:
      list_schema = {
          'name': k,
          'type': Type.INTEGER.name,
          'mode': Mode.REPEATED.name,
      }
    elif t == float:
      list_schema = {
          'name': k,
          'type': Type.FLOAT.name,
          'mode': Mode.REPEATED.name,
      }
    elif t == bool:
      list_schema = {
          'name': k,
          'type': Type.BOOLEAN.name,
          'mode': Mode.REPEATED.name,
      }
    elif t == dict:
      list_schema.update({
          'name': k,
          'type': Type.RECORD.name,
          'mode': Mode.REPEATED.name,
          'fields': get_schema_from_dict(elem),
      })
      # Only in case of dict, update schema for all element.
      continue
    elif t == list:
      raise SchemaNotDefined('list in list is not defined')

  return list_schema


def get_schema_from_dict(d):
  """Get schema from dictionary.
  
  Args:
    d: Dictionary.
    
  Returns:
    Dictionary field schema.
  """
  dict_schema = {}
  for key in d:
    value = d[key]
    t = type(value)
    if t == str:
      schema_field = get_schema_from_str(key, value)
    elif t == int:
      schema_field = {
          'name': key,
          'type': Type.INTEGER.name,
          'mode': Mode.NULLABLE.name,
      }
    elif t == float:
      schema_field = {
          'name': key,
          'type': Type.FLOAT.name,
          'mode': Mode.NULLABLE.name,
      }
    elif t == bool:
      schema_field = {
          'name': key,
          'type': Type.BOOLEAN.name,
          'mode': Mode.NULLABLE.name,
      }
    elif t == list:
      schema_field = get_schema_from_list(key, value)
    elif t == dict:
      schema_field = {
          'name': key,
          'type': Type.RECORD.name,
          'mode': Mode.NULLABLE.name,
          'fields': get_schema_from_dict(value),
      }
    elif t == tuple:
      raise SchemaNotDefined
    dict_schema[key] = schema_field

  return dict_schema


def infer_schema(data):
  """Infer BigQuery schema from sample data.
  
  Args:
    data: String or dictionary.
    
  Returns:
    Schema dictionary. Key is field name.
  """
  json_schema = {}
  data = data if type(data) == list else [data]
  for d in data:
    if type(d) == str:
      d = json.loads(d)
    json_schema.update(get_schema_from_dict(d))

  return json_schema


def get_infered_schema(data):
  """Get infered schema dictionary.
  
  Args:
    data: String or dictionary.

  Returns:
    Schema dictionary.
  """
  json_schema = infer_schema(data)
  return {'fields': [item[1] for item in json_schema.items()]}
