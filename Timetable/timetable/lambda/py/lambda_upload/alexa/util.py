# -*- coding: utf-8 -*-

import requests
from datetime import datetime, date, timedelta
from icalendar import Calendar, Event, vText
from ask_sdk_model import IntentRequest
from typing import Union, Dict, List
import logging

TIMETABLE_DATA = []

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def process_ical_file():
    '''read the calendar file'''
    icalFile = open('calendar.ics', 'rb')
    calendar_to_parse = Calendar.from_ical(icalFile.read())
    for component in calendar_to_parse.walk():
        if component.name == "VEVENT":
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
    event_type = separated_words[1]

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

    module_code_raw = lines_of_description[2].split(
        ": ")[1]  # still has the /01 on the end
    # split into COMP 3006 and 01 and then ignore the 01 at the end
    partial_code = module_code_raw.split("/")
    if(len(partial_code) > 1):
        # The Dissertation module does not have a module code in the timetable file.
        module_code = partial_code[0] + partial_code[1]
    else:
        module_code = "NONE"

    # separate and format the location value.
    location = (component.get('location')).split("-")
    campus = location[0]
    building = location[1]
    # may need to remove . and + from some room codes
    room = location[2]

    # the .dt converts the time to datetime object so that it can be read and processed more easily
    # example of this taken from https://stackoverflow.com/questions/26238835/parse-dates-with-icalendar-and-compare-to-python-datetime
    start_time = component['DTSTART'].dt
    # Store the date as YYYY-MM-DD so it matches AMAZON.DATE format
    date = "{:%Y-%m-%d}".format(start_time)

    # Store the time as HH:MM so that it matches the AMAZON.TIME format
    time = "{:%H:%M}".format(start_time)

    # Calculate the duration and convert to hours and minutes as a string
    end_time = component['DTEND'].dt
    duration = str(end_time - start_time).split(":")
    hour_duration = duration[0]
    minute_duration = duration[1]

    TIMETABLE_DATA.append({"module": module_name, "type": event_type, "lecturer": lecturer, "code": module_code,
                           "location_campus": campus, "location_building": building, "location_room": room, "start_time": start_time, "date": date, "time": time, "duration_hours": hour_duration, "duration_minutes": minute_duration})


def get_restaurants_by_meal(city_data, meal_type):
    """Return a restaurant list based on meal type."""
    # type: (Dict, str) -> List
    return [r for r in city_data["restaurants"] if meal_type in r["meals"]]


def get_restaurants_by_name(city_data, name):
    """Return a restaurant based on name."""
    # type: (Dict, str) -> Dict
    for r in city_data["restaurants"]:
        if r["name"] == name:
            return r
    return {}


def get_attractions_by_distance(city_data, distance):
    """Return a attractions list based on distance."""
    # type: (Dict, str) -> List
    return [a for a in city_data["attractions"]
            if int(a["distance"]) <= int(distance)]


def build_url(city_data, api_info):
    """Return a `request` compatible URL from api properties."""
    # type: (Dict, Dict) -> str
    return "{}:{}{}".format(
        api_info["host"], str(api_info["port"]), api_info["path"].format(
            city=city_data["city"], state=city_data["state"]))


def http_get(url, path_params=None):
    """Return a response JSON for a GET call from `request`."""
    # type: (str, Dict) -> Dict
    response = requests.get(url=url, params=path_params)

    if response.status_code < 200 or response.status_code >= 300:
        response.raise_for_status()
    return response.json()


def get_weather(city_data, api_info):
    """Return weather information for a city by calling API."""
    # type: (Dict, Dict) -> str, str, str
    url = build_url(city_data, api_info)

    response = http_get(url)
    channel = response["query"]["results"]["channel"]

    local_time = channel["lastBuildDate"][17:25]
    current_temp = channel["item"]["condition"]["temp"]
    current_condition = channel["item"]["condition"]["text"]

    return local_time, current_temp, current_condition


def get_resolved_value(request, slot_name):
    """Resolve the slot name from the request."""
    # type: (IntentRequest, str) -> Union[str, None]
    try:
        return request.intent.slots[slot_name].value
    except (AttributeError, ValueError, KeyError, IndexError):
        return None


def searchByDate(date):
    '''search for events taking place on a certain date'''
    # returns a list of all the events matching the date
    # takes date, a string in the format "YYYY-MM-DD", and the timetable data

    # search for the date in the list of events
    # returns unsorted list, may need to sort by time of day
    return [event for event in TIMETABLE_DATA if event['date'] == date]


def findNextLecture():
    '''Finds and returns the event that is next to happen'''
    # currentTime = datetime(2019, 3, 8, 13, 30)  #provided for testing purposes
    # get the current time
    currentTime = datetime.now()
    currentTime.replace(tzinfo=None)
    # information to convert to a naive datetime taken from https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end/15307743
    # find all lectures that take place after the current date and then take the first one as it will be the next lecture
    future_lectures = [
        event for event in TIMETABLE_DATA if event['start_time'].replace(tzinfo=None) > currentTime]
    return future_lectures[0]


def findLecturesOnWeek(week):
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
    logger.info(week_events)
    logger.info("inside the findLecturesOnWeek function")
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
    return lectures_on_day


def timeUntilLecture(lecture):
    '''calculate the time until the given lecture from the current time'''
    # this will not account for daylight savings time??
    currentTime = datetime.now()
    currentTime.replace(tzinfo=None)
    lecture_time = lecture["start_time"].replace(
        tzinfo=None)

    if(lecture_time > currentTime):
        time_until_lecture = lecture_time - currentTime
        # print(time_until_lecture)
        time_string = str(time_until_lecture)
        if("days" in time_string):
            split_days = time_string.split(",")
            days = split_days[0]
            time_string = split_days[1]
            time = time_string.split(".")[0]
            time = time.split(":")[0] + " hours and " + \
                time.split(":")[1] + "minutes"
            time_until_lecture = days + time
        else:
            # there are no days in the time
            time_until_lecture = time_string.split(".")[0]
            time_until_lecture = time_until_lecture.split(
                ":")[0] + " hours and " + time_until_lecture.split(":")[1] + "minutes"

        # print(time_until_lecture)
        # print(type(time_until_lecture))
        return time_until_lecture
    else:
        # if the event was in the past return -1
        # print("-1")
        return -1


def convertToWeekday(date):
    # if(date == date.today())
    # needs checking for the today one
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
