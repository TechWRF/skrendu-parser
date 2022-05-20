import os
import json
from datetime import datetime

def create_dirs(data_dir, params_dir, results_dir):
  for _dir in [data_dir, params_dir, results_dir]:
    if os.path.isdir(_dir) is False:
      os.mkdir(_dir)
    
def create_log(data_path):
  if os.path.isfile(data_path) is False:
    with open(data_path, "w") as f:
      f.write("result_time,departure_city,arrival_city,departure_date,comeback_date,price,url")

def write_log(data_path, data, result_dict):
  with open(data_path, "a") as f:
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

def load_params(params_path):
  with open(params_path) as f:
    return json.load(f)