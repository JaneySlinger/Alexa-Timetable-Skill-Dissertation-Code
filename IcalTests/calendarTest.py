from icalevents.icalevents import events
from icalevents.icalparser import parse_events
# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
from pathlib import Path
import random
import pathlib


file_path = pathlib.Path(
    r'C:\Users\Janey\Documents\DissertationCode\dissertationcode\IcalTests\calendar.ics')

#es = events(None, file_path, None, None, None, False)
#events = parse_events(es, None, None)

# for a in events:
#    print("a")

# just checking that the program runs.
print("Hello World!")
for i in range(10):
    print(random.randint(1, 25))
