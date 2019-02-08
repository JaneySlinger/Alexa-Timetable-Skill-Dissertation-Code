from icalendar import Calendar, Event, vText
from datetime import datetime, date

# opening and reading the values from the ical file using the icalendar module
# https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python

# data I need to get from the event:
# Module Name
# LOCATION - already got
# time and date - already got
# lecturer - get from description
# duration?
# type


def printWholeCalendar():
    '''Prints out the whole calendar with the summary, description, start, and end times'''
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
    icalFile.close()


def printSelectModule(module):
    '''Print out the lectures for a certain module based on summary'''
    icalFile = open('calendar.ics', 'rb')
    calendar_to_parse = Calendar.from_ical(icalFile.read())
    for component in calendar_to_parse.walk():
        if component.name == "VEVENT":
            thing_to_decode = component.get('summary')
            if thing_to_decode.find(module) != -1:
                # if the module name is part of the summary then print the information
                extractData(component)
    icalFile.close()


def printTodayTimetable():
    '''Print the lectures for the current day'''
    icalFile = open('calendar.ics', 'rb')
    calendar_to_parse = Calendar.from_ical(icalFile.read())
    for component in calendar_to_parse.walk():
        if component.name == "VEVENT":
            if component['DTSTART'].dt.date() == datetime.today().date():
                # if the lecture start date is today then print the information
                extractData(component)

    icalFile.close()


def extractData(component):
    print(component.get('summary'))
    print(component.get('description'))
    print(component.get('location'))
    # the .dt converts the time to datetime object so that it can be read and processed more easily
    # example of this taken from https://stackoverflow.com/questions/26238835/parse-dates-with-icalendar-and-compare-to-python-datetime
    print(component['DTSTART'].dt)
    print(component['DTEND'].dt)
    print("\n")


# printWholeCalendar()
#printSelectModule("Computer Graphics")
printTodayTimetable()