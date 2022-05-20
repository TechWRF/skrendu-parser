from params_builder_utils import is_empty, to_date, to_int, bool_assert, \
  days_of_week_assert, days_assert, get_plain_input, get_date_input, \
  get_int_input, get_bool_input, get_week_day_input, get_days_input
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_duration(with_return, start):
  duration = None
  if with_return:
    print("Set duration of your trip with return date or number of days.\nDo you know trip duration in days? y/n")
    enter_duration = get_bool_input()

  if with_return and enter_duration:
    print("Enter trip duration in days.")
    duration = get_int_input()
    print(f"Return date: {str(start + timedelta(days=duration))}")

  elif with_return and enter_duration is False:
    print("Enter return date")
    duration = (get_date_input() - start).days
    print(f"Trip duration: {duration} days")
  return duration

def get_start_dates(dates_in_range):
  start_dates = None
  print("Check prices for every day? y/n")
  every_day = get_bool_input()
  if every_day:
    start_dates = dates_in_range
  
  if every_day is False:
    print("Check prices for specific day of week? y/n")
    day_of_week = get_bool_input()

  if every_day is False and day_of_week:
    print("Enter days of week as comma separated list.\nExample for Saturday and Sunday: 5,6")
    days = get_week_day_input()
    start_dates = [date for date in dates_in_range if date.weekday() in days]

  elif every_day is False and day_of_week is False:
    print("Enter days of month as comma separated list. Example: 10,16,24")
    days = get_days_input()
    start_dates = [date for date in dates_in_range if date.day in days]
  return start_dates

def questionnaire():  
  print("Answer questions to build input parameter JSON.\nEnter text without qoutes.\nDate format: 'YYYY-MM-DD'\n")

  print("Departure city? Enter 3 letter airport code")
  departure_city = input().upper()

  print("Arrival city?")
  arrival_city = input().upper()

  print("Departure date? Just [ENTER] for today.")
  start = get_date_input(True)
  if len(str(start)) == 0:
    start = datetime.now().date()
    print(start)

  print("Flight with return? y/n")
  with_return = get_bool_input()

  duration = get_duration(with_return, start)

  print("Enter number of months for lookup. 0 for single flight.")
  date_range_end = start + relativedelta(months=+get_int_input())
  n_days = (date_range_end - start).days

  first_day = start
  dates_in_range = [first_day]
  for i in range(n_days):
    next_day = first_day + timedelta(days=1)
    dates_in_range.append(next_day)
    first_day = next_day
  
  start_dates = get_start_dates(dates_in_range)
  if with_return:
    end_dates = [date + timedelta(days=duration) for date in start_dates]
  else:
    end_dates = [None] * len(start_dates)

  params = []
  for id, (s, e) in enumerate(zip(start_dates, end_dates)):
    params.append({
      "departure_city": departure_city,
      "arrival_city": arrival_city,
      "departure_date": str(s),
      "comeback_date": str(e),
      "query_id": id
    })

  return params