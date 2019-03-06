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
import datetime

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

week_slot_key = "DATE"
week_slot = "week"

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
        # set up TIMETABLE_DATA
        util.process_ical_file()

        # logger.info(_("This is an untranslated message"))

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
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.ABOUT))
        return handler_input.response_builder.response


class BeforeLectureIntentHandler(AbstractRequestHandler):
    """Handler for before lecture intent which returns the location of the next scheduled event."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BeforeLectureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In BeforeLectureIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        lecture = util.findNextLecture()
        module = lecture['code']
        room = lecture['location_room']
        building = lecture['location_building']
        date = lecture['date']

        speech = ("Your next lecture is {} in room {} in the {} building.").format(
            module, room, building, date)

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class DetailedIndividualDayIntentHandler(AbstractRequestHandler):
    """Handler for DetailedIndividualDayIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DetailedIndividualDayIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In DetailedIndividualDayIntentHandler")

        # the example shortened some of the lines of code by assigning a variable to store the result of some commonly used functions. Maybe use this but may just leave it as the functions as could be easier to read.
        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        # access the slot value for the day to be searched
        slots = handler_input.request_envelope.request.intent.slots
        if day_slot in slots:
            # check if the value in the slot was valid.
            if slots[day_slot].value != None:
                logger.info("Inside the day_slot section")

                day_to_search = slots[day_slot].value

               # save the value of the slot to return later. Might just be able to output it.
                handler_input.attributes_manager.session_attributes[day_slot_key] = day_to_search

        # find the event on that day
                events = util.searchByDate(day_to_search)

        # define how you want alexa to respond.
                if not events:
                    # if there are no lectures on that day
                    speech = ("You have no events on {}").format(day_to_search)
                else:
                    speech = ("On {} you have ").format(day_to_search)
                    for i in range(len(events) - 1):
                        speech += ("a {} hour {} {} at {}, ").format(
                            events[i]["duration_hours"], events[i]["module"], events[i]["type"], events[i]["time"])
                    # speech = ("{} you have a {} hour {} {} at {}").format(day_to_search,events[0]["duration_hours"], events[0]["module"], events[0]["type"], events[0]["time"])
                    last_item_index = len(events) - 1
                    speech += ("and a {} hour {} {} at {}").format(events[last_item_index]["duration_hours"],
                                                                   events[last_item_index]["module"],
                                                                   events[last_item_index]["type"],
                                                                   events[last_item_index]["time"])
            else:
                speech = "I'm not sure what day you asked about. Please try again."
            reprompt = ("You can ask about your timetable today by saying, "
                        "whats on my timetable today")
        else:
            # the slot was empty
            logger.info("In the else section")
            speech = "I'm not sure what day you asked about. Please try again."
            reprompt = ("I'm not sure what day you asked about. "
                        "You can ask about your timetable today by saying, "
                        "whats on my timetable today")

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class WeekOverviewIntentHandler(AbstractRequestHandler):
    """Handler for WeekOverviewIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("WeekOverviewIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In WeekOverviewIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        # test what the slot value is
        slots = handler_input.request_envelope.request.intent.slots
        if week_slot in slots:
            # check if the value in the slot was valid.
            if slots[week_slot].value != None:
                logger.info("Inside the week_slot section")

                week_to_search = slots[week_slot].value
                logger.info(type(week_to_search))
                logger.info(week_to_search)

               # save the value of the slot to return later. Probably don't need it
                handler_input.attributes_manager.session_attributes[week_slot_key] = week_to_search

        restaurant = random.choice(util.get_restaurants_by_meal(
            data.CITY_DATA, "lunch"))
        session_attr["restaurant"] = restaurant["name"]
        speech = ("Lunch time! Here is a good spot. {}. Would you "
                  "like to hear more?").format(restaurant["name"])

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class NextLectureIntentHandler(AbstractRequestHandler):
    """Handler for NextLectureIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("NextLectureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NextLectureIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        restaurant = random.choice(util.get_restaurants_by_meal(
            data.CITY_DATA, "dinner"))
        session_attr["restaurant"] = restaurant["name"]
        speech = ("Enjoy dinner at, {}. Would you "
                  "like to hear more?").format(restaurant["name"])

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class YesMoreInfoIntentHandler(AbstractRequestHandler):
    """Handler for yes to get more info intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.YesIntent")(handler_input)
                and "restaurant" in session_attr)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In YesMoreInfoIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes
        _ = attribute_manager.request_attributes["_"]

        # the restaurant name was stored as a session attribute in the earlier function
        restaurant_name = session_attr["restaurant"]
        restaurant_details = util.get_restaurants_by_name(
            data.CITY_DATA, restaurant_name)

        speech = ("{} is located at {}, the phone number is {}, and the "
                  "description is, {}. I have sent these details to the "
                  "Alexa App on your phone.  Enjoy your meal! "
                  "<say-as interpret-as='interjection'>bon appetit</say-as>"
                  .format(restaurant_details["name"],
                          restaurant_details["address"],
                          restaurant_details["phone"],
                          restaurant_details["description"]))
        card_info = "{}\n{}\n{}, {}, {}\nphone: {}\n".format(
            restaurant_details["name"], restaurant_details["address"],
            data.CITY_DATA["city"], data.CITY_DATA["state"],
            data.CITY_DATA["postcode"], restaurant_details["phone"])

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(
                title=_(data.SKILL_NAME),
                content=card_info)).set_should_end_session(True)
        return handler_input.response_builder.response


class NoMoreInfoIntentHandler(AbstractRequestHandler):
    """Handler for no to get no more info intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.NoIntent")(handler_input) and
                "restaurant" in session_attr)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NoMoreInfoIntentHandler")

        speech = ("Ok.  Enjoy your meal! "
                  "<say-as interpret-as='interjection'>bon appetit</say-as>")
        handler_input.response_builder.speak(speech).set_should_end_session(
            True)
        return handler_input.response_builder.response


class FirstLectureIntentHandler(AbstractRequestHandler):
    """Handler for FirstLectureIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("FirstLectureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FirstLectureIntentHandler")
        distance = util.get_resolved_value(
            handler_input.request_envelope.request, "distance")
        if distance is None:
            distance = 200

        attraction = random.choice(util.get_attractions_by_distance(
            data.CITY_DATA, distance))
        speech = "Try {}, which is {}. {}. Have fun!!".format(
            attraction["name"],
            "right downtown" if attraction["distance"] == "0"
            else "{} miles away".format(attraction["distance"]),
            attraction["description"])

        handler_input.response_builder.speak(speech).set_should_end_session(
            True)
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
sb.add_request_handler(DetailedIndividualDayIntentHandler())
sb.add_request_handler(WeekOverviewIntentHandler())
sb.add_request_handler(NextLectureIntentHandler())
sb.add_request_handler(YesMoreInfoIntentHandler())
sb.add_request_handler(NoMoreInfoIntentHandler())
sb.add_request_handler(FirstLectureIntentHandler())
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
