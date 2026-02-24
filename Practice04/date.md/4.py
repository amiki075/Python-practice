from datetime import datetime

# Example dates
date1 = datetime(2026, 2, 20, 12, 0, 0)  # Feb 20, 2026, 12:00:00
date2 = datetime(2026, 2, 24, 12, 0, 0)  # Feb 24, 2026, 12:00:00

difference = date2 - date1
seconds = difference.total_seconds()

print(f"Date 1: {date1}")
print(f"Date 2: {date2}")
print(f"Difference in seconds: {seconds}")