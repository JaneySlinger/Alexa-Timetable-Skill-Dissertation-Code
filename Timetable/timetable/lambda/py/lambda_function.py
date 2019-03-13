# -*- coding: utf-8 -*-

# City Guide: A sample Alexa Skill Lambda function
# This function shows how you can manage data in objects and arrays,
# choose a random recommendation,
# call an external API and speak the result,
# handle YES/NO intents with session attributes,
# and return text data on a card.

import logging
import random
import gettext
from datetime import datetime, timedelta

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type

from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

from alexa import data, util


day_slot_key = "DATE"
day_slot = "day"

first_slot_key = "DATE"
first_slot = "first_day"

lecture_location_key = "LOCATION"

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Request Handler classes


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]
        if not util.TIMETABLE_DATA:
            # set up TIMETABLE_DATA
            logger.info("Setting up timetable data")
            util.process_ical_file()

        speech = _(data.WELCOME)
        speech += " " + _(data.HELP)
        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(_(
            data.GENERIC_REPROMPT))
        return handler_input.response_builder.response


class AboutIntentHandler(AbstractRequestHandler):
    """Handler for about intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AboutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AboutIntentHandler")
        if not util.TIMETABLE_DATA:
            # set up TIMETABLE_DATA
            logger.info("Setting up timetable data")
            util.process_ical_file()

        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(
            _(data.ABOUT)).ask(_(data.GENERIC_REPROMPT))
        return handler_input.response_builder.response


class BeforeLectureIntentHandler(AbstractRequestHandler):
    """Handler for before lecture intent which returns the location of the next scheduled event."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BeforeLectureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In BeforeLectureIntentHandler")
        if not util.TIMETABLE_DATA:
            # set up TIMETABLE_DATA
            logger.info("Setting up timetable data")
            util.process_ical_file()

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        lecture = util.findNextLecture()
        if not lecture:
            # if there aren't any more lectures on the timetable
            speech = ("There are no more lectures on your timetable.")
        else:
            # save the lecture to be used in the YesMoreInfoIntentHandler
            handler_input.attributes_manager.session_attributes[lecture_location_key] = lecture

            module = lecture['code']
            room = lecture['location_room']
            building = lecture['location_building']
            building = util.convertBuildingCode(
                lecture["location_campus"], building)
            date = lecture['date']

            speech = ("Your next lecture is {} in room {} in {}. Would you like more information about where that is?").format(
                module, room, building)

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class WeekOverviewOrDetailedDayIntentHandler(AbstractRequestHandler):
    """Handler for WeekOverviewOrDetailedDayIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("WeekOverviewOrDetailedDayIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In WeekOverviewOrDetailedDayIntentHandler")
        if not util.TIMETABLE_DATA:
            # set up TIMETABLE_DATA
            logger.info("Setting up timetable data")
            util.process_ical_file()

        # the example shortened some of the lines of code by assigning a variable to store the result of some commonly used functions. Maybe use this but may just leave it as the functions as could be easier to read.
        #attribute_manager = handler_input.attributes_manager
        #session_attr = attribute_manager.session_attributes

        # access the slot value for the day to be searched
        slots = handler_input.request_envelope.request.intent.slots
        if day_slot in slots:
            # check if the value in the slot was valid.
            if slots[day_slot].value != None:
                logger.info("Inside the day_slot section")
                logger.info(slots[day_slot].value)
                value_to_search = slots[day_slot].value

               # save the value of the slot to return later. Might just be able to output it.
                #handler_input.attributes_manager.session_attributes[day_slot_key] = value_to_search

                if("W" in value_to_search):
                    # then the slot is a week value
                    # find the event on that day
                    week_events = util.findLecturesOnWeek(value_to_search)
                    if not week_events:
                        # if there are no lectures that week
                        speech = ("You have no events {}").format(
                            value_to_search)
                    else:
                        length = len(week_events)
                        speech = ("You have ")
                        for i in range(length):
                            if(length > 1 and i == length - 1):
                                # if there is more than one day with events
                                speech += "and "
                            speech += ("{}").format(
                                week_events[i]["num_of_lectures"])
                            if(week_events[i]["num_of_lectures"] == 1):
                                # if there is only one lecture on that day then lecture does not need to be plural
                                speech += " lecture "
                            else:
                                speech += " lectures "

                            speech += ("on {} between {} and {}, ").format(
                                week_events[i]["weekday"], week_events[i]["day_start"], week_events[i]["day_end"])
                else:
                    # the slot is a date value for an individual day
                    events = util.searchByDate(value_to_search)

                    if not events:
                        # if there are no lectures on that day
                        speech = ("You have no events on {}").format(
                            value_to_search)
                    else:
                        length = len(events)
                        speech = ("On {} you have ").format(value_to_search)
                        for i in range(length):
                            if(length > 1 and i == length - 1):
                                speech += ("and ")
                            speech += ("a {} hour {} {} at {}, ").format(
                                events[i]["duration_hours"], events[i]["module"], events[i]["type"], events[i]["time"])
            else:
                speech = "I'm not sure what day or week you asked about. Please try again."
            reprompt = ("You can ask about your timetable today by saying, "
                        "whats on my timetable today")
        else:
            # the slot was empty
            logger.info("In the else section")
            speech = "I'm not sure what day or week you asked about. Please try again."
            reprompt = ("I'm not sure what day or week you asked about. "
                        "You can ask about your timetable this week by saying, "
                        "whats on my timetable this week")

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class NextLectureIntentHandler(AbstractRequestHandler):
    """Handler for NextLectureIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("NextLectureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NextLectureIntentHandler")
        if not util.TIMETABLE_DATA:
            # set up TIMETABLE_DATA
            logger.info("Setting up timetable data")
            util.process_ical_file()

        # get the value of the next lecture to happen
        next_lecture = util.findNextLecture()

        if not next_lecture:
            # if there are no lectures in the future
            speech = ("There are no more lectures on your timetable.")
        else:
            time_until_lecture = util.timeUntilLecture(next_lecture)
            speech = ("Your next lecture is {} at {}. That is in {}.").format(
                next_lecture["module"], next_lecture["time"], time_until_lecture)

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class YesMoreInfoIntentHandler(AbstractRequestHandler):
    """Handler for yes to get more info intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.YesIntent")(handler_input)
                and lecture_location_key in session_attr)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In YesMoreInfoIntentHandler")
        if not util.TIMETABLE_DATA:
            # set up TIMETABLE_DATA
            logger.info("Setting up timetable data")
            util.process_ical_file()

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes
        _ = attribute_manager.request_attributes["_"]

        # the lecture was stored as a session attribute in the earlier function
        lecture = session_attr[lecture_location_key]
        building = util.convertBuildingCode(
            lecture["location_campus"], lecture["location_building"])
        campus = util.convertCampusCode(lecture["location_campus"])

        speech = ("{} is on {} campus. Your lecture is in room {}. "
                  "I have sent these details to the "
                  "Alexa App on your phone."
                  .format(building,
                          campus,
                          lecture["location_room"]))
        card_info = "Room: {}\nBuilding: {}\nCampus: {}\n".format(
            lecture["location_room"], building,
            campus)

        handler_input.response_builder.speak(speech).ask(speech).set_card(
            SimpleCard(
                title=_(data.SKILL_NAME),
                content=card_info))
        return handler_input.response_builder.response


class NoMoreInfoIntentHandler(AbstractRequestHandler):
    """Handler for no to get no more info intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.NoIntent")(handler_input) and
                lecture_location_key in session_attr)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NoMoreInfoIntentHandler")
        if not util.TIMETABLE_DATA:
            # set up TIMETABLE_DATA
            logger.info("Setting up timetable data")
            util.process_ical_file()

        speech = ("Ok.")
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class FirstLectureIntentHandler(AbstractRequestHandler):
    """Handler for FirstLectureIntent."""
    # take a slot of a date (usually today or tomorrow)
    # return the time of the first lecture and the time until that lecture

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FirstLectureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FirstLectureIntentHandler")
        if not util.TIMETABLE_DATA:
            # set up TIMETABLE_DATA
            logger.info("Setting up timetable data")
            util.process_ical_file()
        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        # access the slot value to be searched
        slots = handler_input.request_envelope.request.intent.slots
        if first_slot in slots:
            # check if the value in the slot is valid
            if slots[first_slot].value != None:
                logger.info("Inside the first_slot section")
                day_to_search = slots[first_slot].value

                # get the first lecture of the day
                events_on_day = util.searchByDate(day_to_search)

                if not events_on_day:
                    speech = ("You don't have any lectures {}").format(
                        day_to_search)
                else:
                    speech = ("Your first lecture {} is {} at {}. ").format(
                        day_to_search, events_on_day[0]["module"], events_on_day[0]["time"])
                    # Calculate how long it is until the lecture starts
                    time_until_lecture = util.timeUntilLecture(
                        events_on_day[0])
                    if(time_until_lecture != -1):
                        # if the lecture is not in the past
                        speech += ("That is in {}.").format(time_until_lecture)
                    else:
                        speech += ("That is in the past.")

            else:
                speech = "I'm not sure what day you asked about. Please try again."
            reprompt = ("You can ask about your first lecture today by saying, "
                        "whats my first lecture today")
        else:
            # the slot was empty
            logger.info("In the else section")
            speech = "I'm not sure what day you asked about. Please try again."
            reprompt = ("I'm not sure what day you asked about. "
                        "You can ask about your first lecture today or tomorrow by saying, "
                        "whats my first lecture today?")

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        if not util.TIMETABLE_DATA:
            # set up TIMETABLE_DATA
            logger.info("Setting up timetable data")
            util.process_ical_file()
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.HELP)).ask(_(data.HELP))
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop intents."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.STOP)).set_should_end_session(True)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent or Yes/No without
    restaurant info intent.

     2018-May-01: AMAZON.FallackIntent is only currently available in
     en-US locale. This handler will not be triggered except in that
     locale, so it can be safely deployed for any locale."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.FallbackIntent")(handler_input) or
                ("restaurant" not in session_attr and (
                    is_intent_name("AMAZON.YesIntent")(handler_input) or
                    is_intent_name("AMAZON.NoIntent")(handler_input))
                 ))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.FALLBACK).format(data.SKILL_NAME)).ask(_(
                data.FALLBACK).format(data.SKILL_NAME))

        return handler_input.response_builder.response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.

    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        logger.info("Original request was {}".format(
            handler_input.request_envelope.request))

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'base', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes[
            "_"] = i18n.gettext


# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AboutIntentHandler())
sb.add_request_handler(BeforeLectureIntentHandler())
sb.add_request_handler(WeekOverviewOrDetailedDayIntentHandler())
sb.add_request_handler(NextLectureIntentHandler())
sb.add_request_handler(FirstLectureIntentHandler())
sb.add_request_handler(YesMoreInfoIntentHandler())
sb.add_request_handler(NoMoreInfoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add locale interceptor to the skill.
sb.add_global_request_interceptor(LocalizationInterceptor())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
