from icalendar import Calendar, Event, vText
from datetime import datetime, date

# opening and reading the values from the ical file using the icalendar module
# https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python

# data I need to get from the event:
# Module Name
# Module code
# LOCATION - already got
# time and date - already got
# lecturer - get from description
# duration?
# type

timetableData = []


def printWholeCalendar():
    '''Prints out the whole calendar with the summary, description, start, and end times'''
    icalFile = open('calendar.ics', 'rb')
    calendar_to_parse = Calendar.from_ical(icalFile.read())
    for component in calendar_to_parse.walk():
        if component.name == "VEVENT":
            extractData(component)
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
    # print(module_name)

    event_type = separated_words[1]
    # print(event_type)

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
    # print(lecturer)

    module_code_raw = lines_of_description[2].split(
        ": ")[1]  # still has the /01 on the end
    # split into COMP 3006 and 01 and then ignore the 01 at the end
    partial_code = module_code_raw.split("/")
    if(len(partial_code) > 1):
        # The Dissertation module does not have a module code in the timetable file.
        module_code = partial_code[0] + partial_code[1]
    else:
        module_code = "NONE"
    # print(module_code)

    # separate and format the location value.
    location = (component.get('location')).split("-")
    campus = location[0]
    building = location[1]
    # may need to remove . and + from some room codes
    room = location[2]

    #print(campus + ", " + building + ", " + room)

    # the .dt converts the time to datetime object so that it can be read and processed more easily
    # example of this taken from https://stackoverflow.com/questions/26238835/parse-dates-with-icalendar-and-compare-to-python-datetime
    start_time = component['DTSTART'].dt
    # Store the date as YYYY-MM-DD so it matches AMAZON.DATE format
    date = "{:%Y-%m-%d}".format(start_time)
    # print(date)

    # Store the time as HH:MM so that it matches the AMAZON.TIME format
    time = "{:%H:%M}".format(start_time)
    # print(time)

    # Calculate the duration and convert to hours and minutes as a string
    end_time = component['DTEND'].dt
    duration = str(end_time - start_time).split(":")
    hour_duration = duration[0]
    minute_duration = duration[1]
    #print(hour_duration + ":" + minute_duration)
    # print("\n")

    timetableData.append({"module": module_name, "type": event_type, "lecturer": lecturer, "code": module_code,
                          "location_campus": campus, "location_building": building, "location_room": room, "date": date, "time": time, "duration_hours": hour_duration, "duration_minutes": minute_duration})


printWholeCalendar()
# printSelectModule("Graphics")
# printTodayTimetable()
print(timetableData)
