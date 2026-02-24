from datetime import date, timedelta

today = date.today()
five_days_ago = today - timedelta(days=5)

print("Today:", today)
print("Five days ago:", five_days_ago)