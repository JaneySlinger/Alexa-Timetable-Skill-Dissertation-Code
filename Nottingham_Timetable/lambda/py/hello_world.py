# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to the Nottingham Timetable skill, you can ask what lectures you have today!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Welcome to Nottingham Timetable", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class TimeOfLectureIntentHandler(AbstractRequestHandler):
    """Handler for TimeOfLectureIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("TimeOfLectureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Your lecture is at 12pm"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Your lecture is at 12pm", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class DayLecturesIntentHandler(AbstractRequestHandler):
    """Handler for DayLecturesIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DayLecturesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Today you have Fundamentals of Information Visualisation at 11am and Software Engineering Management at 4pm"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("FIV: 11am, SEM: 4pm", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class ModuleLecturesIntent(AbstractRequestHandler):
    """Handler for ModuleLecturesIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ModuleLecturesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Computer Security has a lecture on Thursday at 1pm, a lab on Friday at 9am, and a lecture on Friday at 2pm."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("SEC: Thu 1pm, Fri 9am, Fri 2pm", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class LectureLocationIntent(AbstractRequestHandler):
    """Handler for LectureLocationIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LectureLocationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "The Computer Security lab on Friday is in COMPSCI A32 on Jubilee Campus."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Computer Security, Friday, COMPSCI A32, Jubilee", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class LecturerIntent(AbstractRequestHandler):
    """Handler for LecturerIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LecturerIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Computer Security is taught by Dr M. Pound."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Computer Security is taught by Dr M. Pound", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class NextLectureIntent(AbstractRequestHandler):
    """Handler for NextLectureIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("NextLectureIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Your next lecture is Computer Security in COMPSCI A32 at 9am."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Computer Security in COMPSCI A32 at 9am", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can ask what lectures you have today!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Sample text", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Sample Text", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Nottingham Timetable skill can't help you with that.  "
            "You can ask when a lecture for one of your modules is scheduled!!")
        reprompt = "You can ask about your lectures!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TimeOfLectureIntentHandler())
sb.add_request_handler(DayLecturesIntentHandler())
sb.add_request_handler(ModuleLecturesIntent())
sb.add_request_handler(LectureLocationIntent())
sb.add_request_handler(LecturerIntent())
sb.add_request_handler(NextLectureIntent())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
