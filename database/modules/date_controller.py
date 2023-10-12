from datetime import datetime, date, timedelta

def date_to_str(date):
    return date.strftime("%Y-%m-%d")

def get_now():
    now = datetime.now()
    return date_to_str(now)

def get_yesterday(current_date):
    return datetime.strptime(current_date, "%Y-%m-%d") - timedelta(1)