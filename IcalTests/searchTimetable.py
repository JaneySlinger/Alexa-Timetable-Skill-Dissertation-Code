
import datetime
from calendarData import timetableData

# data is stored as a list of dictionaries, as seen below
# timetableData = [
#    {
#        'module': 'Collaboration and Communication Technologies',
#        'type': 'Lecture ',
#        'lecturer': 'Koleva BN Dr ',
#        'code': 'COMP3010',
#        'location': vText('b'JC - DEARING - C35 + ''),
#        'date': '2018-10-01'
#        'time': '13:00',
#        'duration': datetime.timedelta(seconds=3600)
#    },
#    {
#        'module': 'Mobile Device Programming',
#        'type': 'Lecture ',
#        'lecturer': 'Chen X Dr, Flintham M D Dr ',
#        'code': 'COMP3018',
#        'location': vText('b'JC - BSSOUTH - A25 +\\, JC - BSSOUTH - A25 + ''),
#        'date': '2018-10-01',
#        'time': '14:00',
#        'duration': datetime.timedelta(seconds=3600)
#    }
# ]


def searchByDate(date):
    '''search for events taking place on a certain date'''
    # returns a list of all the events matching the date
    # takes date, a string in the format "YYYY-MM-DD"

    # do i need to convert it? Doesn't it come from the alexa in that format
    # convert the dateToCompare to the format YYYY-MM-DD
    #dateToCompare = "{:%Y-%m-%d}".format(date)

    # search for the date in the list of events
    return [event for event in timetableData if event['date'] == dateToCompare]


print(searchByDate('2019-02-28'))
