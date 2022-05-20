import os
import json
from datetime import datetime

def create_log(log_path):
  if os.path.isfile(log_path) is False:
    with open(log_path, "w") as f:
      f.write("result_time,departure_city,arrival_city,departure_date,comeback_date,price,url")

def write_log(log_path, data, result_dict):
  with open(log_path, "a") as f:
    for i, params in enumerate(data):
      f.write(
        (f'\n{datetime.now().date()},'
        f'{params["departure_city"]},'
        f'{params["arrival_city"]},'
        f'{params["departure_date"]},'
        f'{params["comeback_date"]},'
        f'{result_dict[params["query_id"]]},'
        f'{result_dict["%s_url" % params["query_id"]]}')
      )

def load_params(param_path):
  with open(param_path) as f:
    return json.load(f)