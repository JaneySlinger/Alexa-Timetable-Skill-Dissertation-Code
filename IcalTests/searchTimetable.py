
from alexa import data

# data is stored as a list of dictionaries, as seen below
# timetableData = [
#    {
#        'module': 'Collaboration and Communication Technologies',
#        'type': 'Lecture ',
#        'lecturer': 'Koleva BN Dr ',
#        'code': 'COMP3010',
#        'location_campus': 'JC',
#        'location_building': 'DEARING',
#        'location_room': 'C35+',
#        'date': '2018-10-01',
#        'time': '13:00',
#        'duration_hours': '1',
#        'duration_minutes': '00'
#    },
#    {
#        'module': 'Mobile Device Programming',
#        'type': 'Lecture ',
#        'lecturer': 'Chen X Dr, Flintham M D Dr ',
#        'code': 'COMP3018',
#        'location_campus': 'JC',
#        'location_building': 'BSSOUTH',
#        'location_room': 'A25+,JC',
#        'date': '2018-10-01',
#        'time': '14:00',
#        'duration_hours': '1',
#        'duration_minutes': '00'
#    }
# ]


def searchByDate(date):
    '''search for events taking place on a certain date'''
    # returns a list of all the events matching the date
    # takes date, a string in the format "YYYY-MM-DD"

    # search for the date in the list of events
    # returns unsorted list, may need to sort by time of day
    return [event for event in TIMETABLE_DATA if event['date'] == date]


print(searchByDate('2019-02-28'))
print(searchByDate('2019-03-01'))
