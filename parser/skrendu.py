import subprocess
import re
from threading import Thread

class Skrendu(Thread):
  def __init__(self, departure_city, arrival_city, departure_date, comeback_date, query_id, result_dict):
    Thread.__init__(self)
    self.chromium_cmd = "chromium --headless --disable-gpu --dump-dom --virtual-time-budget=60000 --run-all-compositor-stages-before-draw".split()
    self.pattern = re.compile('value current">€ (\d+)')

    self.departure_city = departure_city
    self.arrival_city = arrival_city
    self.departure_date = departure_date
    self.comeback_date = comeback_date

    self.result_dict = result_dict
    self.query_id = query_id

  def get_price(self):
    if self.comeback_date != "None":
      comeback_date_str = f"comeback_date:{self.comeback_date}"
    else:
      comeback_date_str = ""

    url = ("https://skrendu.lt/lt/flights/"
    f"departure_city:{self.departure_city}/"
    f"arrival_city:{self.arrival_city}/"
    f"departure_date:{self.departure_date}/"
    f"{comeback_date_str}")

    print(url)

    out = subprocess.check_output(self.chromium_cmd + [url]).decode('utf-8')
    result = self.pattern.search(out)
    result = result.group(1)
    print(result)
    return result, url

  def run(self):
    price, url = [None] * 2
    c = 0
    while price is None and c < 10:
      try:
        price, url = self.get_price()
      except:
        c += 1
    self.result_dict[self.query_id] = price
    self.result_dict[f"{self.query_id}_url"] = url