# -*- coding: utf-8 -*-

import requests
from datetime import datetime, date, timedelta
from icalendar import Calendar, Event, vText
from ask_sdk_model import IntentRequest
from typing import Union, Dict, List

TIMETABLE_DATA = []


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

    # sort the list by the time of the lecture
    #TIMETABLE_DATA = sorted(unsorted_timetable, key=lambda k: k['start_time'])


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
    # get the current time
    #currentTime = datetime.now()
    currentTime = datetime(2019, 3, 7, 12)
    currentTime.replace(tzinfo=None)
    i = 0
    while TIMETABLE_DATA[i]['start_time'].replace(tzinfo=None) < currentTime:
        i += 1

    next_lecture = TIMETABLE_DATA[i + 1]
    return next_lecture
