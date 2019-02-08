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
    '''extract the data from the component and store/print '''
    # string in form: "MODULE NAME - TYPE"
    # split the string before and after the "-"
    summary = component.get('summary')
    # split function referenced from python documentation
    # https://docs.python.org/3/library/stdtypes.html#str.split
    separated_words = summary.split(" - ", 1)
    module_name = separated_words[0]
    print(module_name)
    event_type = separated_words[1]
    print(event_type)

    # description in form:
    # "Taught by: Lecturer name
    # Blank Line
    # Module Code: COMP/3011/01"
    # cut the /01 off the end as it is the same for all of them and not part of the code
    # then the last time updated but I don't think I need that
    description = component.get('description')
    # splitlines found on python documentation
    # https://docs.python.org/3/library/stdtypes.html#str.splitlines
    lines_of_description = description.splitlines()
    lecturer = lines_of_description[0].split(": ")[1]
    # may want to reverse the order so it reads Dr M Pound rather than Pound M Dr
    # would do this by splitting the string, reordering the resulting words, and joining
    print(lecturer)

    module_code_raw = lines_of_description[2].split(
        ": ")[1]  # still has the /01 on the end
    # split into COMP 3006 and 01 and then ignore the 01 at the end
    partial_code = module_code_raw.split("/")
    module_code = partial_code[0] + partial_code[1]
    print(module_code)

    location = component.get('location')
    print(location)
    # the .dt converts the time to datetime object so that it can be read and processed more easily
    # example of this taken from https://stackoverflow.com/questions/26238835/parse-dates-with-icalendar-and-compare-to-python-datetime
    start_time = component['DTSTART'].dt
    print(start_time)
    end_time = component['DTEND'].dt

    # need to work out the duration
    duration = end_time - start_time
    print(duration)

    print("\n")


# printWholeCalendar()
#printSelectModule("Computer Graphics")
printTodayTimetable()
