import os
import sys
cwd = os.getcwd()
sys.path.append(os.path.join(cwd, "parser"))
sys.path.append(os.path.join(cwd, "utils"))

from skrendu import Skrendu
from params_builder import questionnaire
from skrendu_utils import create_dirs, create_log, write_log, load_params
from params_builder_utils import write_params
import argparse

def read_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', type=str, help='name for input param json and output csv', required=True)
  parser.add_argument('-b', type=int, help='number of parallel requests', required=True)
  parser.add_argument('-n', action='store_true', default=False, help='specify to overwrite old params json')
  args = parser.parse_args()

  data_dir = os.path.join(os.getcwd(), "data")
  params_dir = os.path.join(data_dir, "params")
  results_dir = os.path.join(data_dir, "results")
  return data_dir, params_dir, results_dir, os.path.join(params_dir, f"{args.f}.json"), os.path.join(results_dir, f"{args.f}.csv"), args.n, args.b

def parse(result_dict, data):
  queries = []
  for params in data:
    queries.append(
      Skrendu(
        params["departure_city"],
        params["arrival_city"],
        params["departure_date"],
        params["comeback_date"],
        params["query_id"],
        result_dict
      )
    )

  [p.start() for p in queries]
  [p.join() for p in queries]

if __name__ == "__main__":
  data_dir, params_dir, results_dir, params_path, data_path, new_params, batch_size = read_args()
  create_dirs(data_dir, params_dir, results_dir)
  create_log(data_path)

  if os.path.isfile(params_path):
    params_exist = True
  else:
    params_exist = False

  if params_exist and new_params or params_exist is False:
    params = questionnaire()
    write_params(params_path, params)

  result_dict = {}
  data = load_params(params_path)
  n_queries = len(data)
  for i in range(n_queries // batch_size + 1):
    start = i * batch_size
    end = min([n_queries, (i + 1) * batch_size])
    parse(result_dict, data[start: end])

  write_log(data_path, data, result_dict)