import logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logging.setLevel(logging.INFO)
my_move = ""
alexa_move = ""


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Welcome to CodeMonkey Chess. White goes first, please make a move"
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("White goes first",
                                                                              speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "You can tell me a move to move a piece like move c4 to b4\
         or  rook from c4 to b4. You can also ask me to repeat my last move by saying repeat\
         Say  reset board to create a new game."


        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(SimpleCard("ChessMonkey", speech_text))
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) \
               or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Move cancelled, please say another move"
        my_move = ""
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("ChessMonkey", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # this is where we reset the board
        speech_text = "Game ended. Board reset"
        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("ChessMonkey", speech_text))
        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class MoveIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("MoveIntent")(handler_input)

    def handle(self, handler_input):
        global my_move
        slots = handler_input.request_envelope.request.intent.slots
        if "Position" in slots:
            my_move = slots["Position"].value
            my_move.strip(" ")
        speech_text = "Moved",my_move,". I am moving", alexa_move

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("ChessMonkey",
                                                                              speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class ResetBoardIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ResetBoardIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Resetting board"
        my_move = 'game reset'

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("ChessMonkey",
                                                                              speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response



def get_move_alexa(move_text):
    global my_move
    return my_move

def give_move_alexa(move_text):
    global alexa_move
    alexa_move = move_text


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MoveIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()