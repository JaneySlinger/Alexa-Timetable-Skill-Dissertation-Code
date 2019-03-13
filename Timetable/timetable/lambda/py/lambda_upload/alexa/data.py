# -*- coding: utf-8 -*-

# Resolving gettext as _ for module loading.
from gettext import gettext as _

SKILL_NAME = "Nottingham Timetable"

WELCOME = ("Welcome to Nottingham Timetable!")
HELP = ("You can say, what do i have today, what do i have this week, what is my next lecture, what time do lectures start tomorrow, or where is my lecture.")
ABOUT = ("You can ask about your University of Nottingham timetable, such as what do i have today, what do i have this week, or where is my lecture.")
STOP = ("Okay, see you next time!")
FALLBACK = ("The {} can't help you with that. It can help you find out about your lectures today if you say what do i have today, or an overview of your week if you say tell me about my lectures this week. What can i help you with?")
GENERIC_REPROMPT = ("What can I help you with?")

BUILDING_CODES = {
    "UP-CLIVEG": "Sir Clive Granger Building",
    "UP-HALLWARD": "Hallward Library",
    "UP-HEMSLEY":	"University Staff Club",
    "UP-HIGH":	"Highfield House",
    "UP-HUGHST":	"Hugh Stewart House",
    "UP-LASS":	"Law and Social Sciences Building",
    "UP-PORT":	"Portland Building",
    "UP-TRNT":	"Trent Building",
    "UP-ARCH-SRB":	"Sustainable Research Building",
    "UP-ARTCEN":	"Arts Centre Lecture Theatre",
    "UP-BOOTS":	"Boots Science Building",
    "UP-COATESRD":	"Coates Road Auditorium",
    "UP-CHEM":	"Chemistry Building",
    "UP-COAT":	"Coates Building",
    "UP-ESLC":	"Engineering and Science Learning Centre",
    "UP-GEOGREEN":	"George Green Library",
    "UP-KEIGHTON AUD":	"Keighton Auditorium",
    "UP-LIFESCI":	"Life Sciences Building",
    "UP-MATH":	"Mathematical Sciences Building",
    "UP-PHARM":	"Pharmacy Building",
    "UP-PHYS":	"Physics Building",
    "UP-POPE":	"Pope Building",
    "UP-PRB":	"Pavement Research Building",
    "UP-PSYC":	"Psychology Building",
    "UP-TOWER":	"Tower Block",
    "UP-WOLF":	"Wolfson Building",
    "UP-HUMS":	"Humanities Building",
    "UP-LENG":	"Lenton Grove",
    "UP-WILL":	"Willoughby Hall",
    "NMS-MEDSCH":	"Nottingham Medical School",
    "QMC-STHBLK":	"South Block",
    "JC-AEROSPACE-TEC":	"Aerospace Technology Centre",
    "JC-AMEN":	"Amenities Building",
    "JC-BSNORTH":	"Business School North",
    "JC-BSSOUTH":	"Business School South",
    "JC-DEARING":	"Dearing Building",
    "JC-ENERGY-TEC":	"Energy Technologies Building",
    "JC-EXCHGE":	"The Exchange Building",
    "JC-DEARING": "The Dearing Building",
    "JC-COMPSCI": "Computer Science",
    "JC-NGB":	"Nottingham Geospatial Building",
    "JC-SI-YUAN-CENTRE":	"The Si Yuan Centre of Contemporary Chinese Studies",
    "JC-YANG-Fujia":	"YANG Fujia Building",
    "CITY-CLINSCI":	"Clinical Sciences Building",
    "SB-GATE":	"Gateway Building",
    "SB-LECTBLK":	"Lecture Room Block",
    "SB-MAINBLDG":	"Main Building",
    "SB-PLANTSCI":	"Plant Sciences Building",
    "SB-VETSCH":	"Veterinary Sciences Building",
    "SB-FOODSCI": "Food Sciences Building",
    "DERBY-DMS":	"Derby Medical School",
    "DERBY-DSN":	"Derby School of Nursing",
    "KMC-KM":	"Kings Meadow Campus"
}

MY_API = {
    "host": "https://query.yahooapis.com",
    "port": 443,
    "path": "/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22{city}%2C%20{state}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys",
}
