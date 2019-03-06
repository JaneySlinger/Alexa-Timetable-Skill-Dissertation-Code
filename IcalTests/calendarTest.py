from icalendar import Calendar, Event, vText
from datetime import datetime, date, timedelta

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

TIMETABLE_DATA = []


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

    # print(campus + ", " + building + ", " + room)

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
    # print(hour_duration + ":" + minute_duration)
    # print("\n")

    TIMETABLE_DATA.append({"module": module_name, "type": event_type, "lecturer": lecturer, "code": module_code,
                           "location_campus": campus, "location_building": building, "location_room": room, "start_time": start_time, "date": date, "time": time, "duration_hours": hour_duration, "duration_minutes": minute_duration})


def printNextLecture():
    # currentTime = datetime(2019, 3, 8, 13, 30)
    currentTime = datetime.now()
    currentTime.replace(tzinfo=None)
    print(currentTime)
    # information to convert to a naive datetime taken from https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end/15307743
    # find all lectures that take place after the current date and then take the first one as it will be the next lecture
    future_lectures = [
        event for event in TIMETABLE_DATA if event['start_time'].replace(tzinfo=None) > currentTime]
    print(future_lectures[0])
    return future_lectures[0]


def printLecturesOnWeek(week):
    '''find the number of lectures on each day in the given week and the start and end times'''
    lectures_on_day = []
    # returns either the list of days with lectures, or an empty list

    # week number is provided in the form "2019-W20" but needs to be converted to 20 as an int
    # year number included as academic year spans calendar years
    week_number = int(week.split("-W")[1])
    year_number = int(week.split("-W")[0])

    # isocalendar function from https://docs.python.org/2/library/datetime.html
    # find the lectures that match the week number
    week_events = [event for event in TIMETABLE_DATA if event['start_time'].isocalendar()[
        1] == week_number and event['start_time'].isocalendar()[0] == year_number]

    # find out how many lectures are on each day
    dates = []
    for lecture in week_events:
        if lecture['date'] not in dates:
            dates.append(lecture['date'])

    for date in dates:
        # loop through the days that have lectures
        num_of_lectures = 0
        temp_day_lectures = []
        for event in week_events:
            # count the number of lectures on that day
            if date == event['date']:
                num_of_lectures += 1
                temp_day_lectures.append(event)

        # find the start time of the first lecture on that day
        if temp_day_lectures:
            day_start = temp_day_lectures[0]['start_time']
            weekday = convertToWeekday(day_start)

            day_start = "{:%H:%M}".format(day_start)
            # find the last lecture and then work out the end time of the lecture
            last_lecture = temp_day_lectures[len(temp_day_lectures) - 1]
            day_end = last_lecture['start_time'] + timedelta(
                minutes=int(last_lecture['duration_minutes']), hours=int(last_lecture['duration_hours']))
            day_end = "{:%H:%M}".format(day_end)
            # store the number of lectures and start and end times of each day
            lectures_on_day.append(
                {"date": date, "weekday": weekday, "num_of_lectures": num_of_lectures, "day_start": day_start, "day_end": day_end})
    print(lectures_on_day)
    return lectures_on_day


def convertToWeekday(date):
    weekday = date.isoweekday()
    if(weekday == 1):
        weekday = "monday"
    elif(weekday == 2):
        weekday = "tuesday"
    elif(weekday == 3):
        weekday = "wednesday"
    elif(weekday == 4):
        weekday = "thursday"
    elif(weekday == 5):
        weekday = "friday"
    elif(weekday == 6):
        weekday = "saturday"
    elif(weekday == 7):
        weekday = "sunday"

    return weekday


printWholeCalendar()
# printSelectModule("Graphics")
# printTodayTimetable()
# print(TIMETABLE_DATA)
# printNextLecture()
printLecturesOnWeek("2019-W10")
