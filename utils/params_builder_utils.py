import json
from datetime import datetime

def is_empty(value, empty_legal):
  if len(value) == 0 and empty_legal is False:
    return None
  elif len(value) == 0 and empty_legal:
    return ''
  else:
    return value

def to_date(date_str):
  if date_str is not None and len(date_str) == 0:
    return date_str
  try:
    return datetime.strptime(date_str, '%Y-%m-%d').date()
  except:
    print("incorrect format for date")
    return None

def to_int(int_str):
  if int_str is not None and len(int_str) == 0:
    return int_str
  try:
    return int(int_str)
  except:
    print(f"incorrect format for number: '{int_str}'")
    return None

def bool_assert(bool_str):
  if bool_str == 'y':
    return True
  elif bool_str == 'n':
    return False
  else:
    print("enter 'y' or 'n' ")

def days_of_week_assert(list_by_comma):
  days = [to_int(day) for day in list_by_comma.split(",")]
  weekdays = list(range(7))
  for day in days:
    if day not in weekdays:
      return None
  return days

def days_assert(list_by_comma):
  days = [to_int(day) for day in list_by_comma.split(",")]
  for day in days:
    if day is None:
      return None
  return days

def get_plain_input():
  return input().strip().lower()

def get_date_input(empty_legal = False):
  value = None
  while value is None:
    value = get_plain_input()
    value = is_empty(value, empty_legal)
    value = to_date(value)
  return value

def get_int_input(empty_legal = False):
  value = None
  while value is None:
    value = get_plain_input()
    value = is_empty(value, empty_legal)
    value = to_int(value)
  return value

def get_bool_input():
  value = None
  while value is None:
    value = bool_assert(get_plain_input())
  return value

def get_week_day_input(empty_legal = True):
  value = None
  while value is None:
    value = get_plain_input()
    value = is_empty(value, empty_legal)
    value = days_of_week_assert(value)
  return value

def get_days_input(empty_legal = False):
  value = None
  while value is None:
    value = get_plain_input()
    value = is_empty(value, empty_legal)
    value = days_assert(value)
  return value

def write_params(param_path, params):
  with open(param_path, "w") as f:
    json.dump(params, f, indent=4)