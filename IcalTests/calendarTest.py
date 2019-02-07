from icalendar import Calendar, Event
from datetime import datetime, date

# opening and reading the values from the ical file using the icalendar module
# https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python
icalFile = open('calendar.ics', 'rb')
calendar_to_parse = Calendar.from_ical(icalFile.read())
for component in calendar_to_parse.walk():
    if component.name == "VEVENT":
        print(component.get('summary'))
        print(component.get('description'))
        print(component.get('location'))
        # the .dt converts the time to datetime object so that it can be read and processed more easily
        # example of this taken from https://stackoverflow.com/questions/26238835/parse-dates-with-icalendar-and-compare-to-python-datetime
        print(component['DTSTART'].dt)
        print(component['DTEND'].dt)
        print(component['DTSTAMP'].dt)
icalFile.close()
