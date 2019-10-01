import collections
import Queue as queue

import message_parser
import sp_exceptions


# should we print messages received from the server?
PRINT_SERVER_MESSAGES = False

# should we print commands sent to the server?
PRINT_SENT_COMMANDS = False

class MessageHandler:
    """
    Handles all incoming messages from the server.  Parses their data and puts
    it into the given WorldModel.

    All '_handle_*' functions deal with their appropriate message types
    as received from a server.  This allows adding a message handler to be as
    simple as adding a new '_handle_*' function to this object.
    """

    # an inner class used for creating named tuple 'hear' messages
    Message = collections.namedtuple("Message", "time sender message")

    def __init__(self):
        pass


    def handle_message(self, msg):
        """
        Takes a raw message direct from the server, parses it, and stores its
        data in the world and body model objects given at init.  Returns the
        type of message received.
        """

        # get all the expressions contained in the given message
        parsed = message_parser.parse(msg)

        if PRINT_SERVER_MESSAGES:

            print parsed, "\n"

        # this is the name of the function that should be used to handle
        # this message type.  we pull it from this object dynamically to
        # avoid having a huge if/elif/.../else statement.
        msg_func = "_handle_%s" % parsed[0]

        if hasattr(self, msg_func):
            # call the appropriate function with this message
            getattr(self, msg_func).__call__(parsed)

        # throw an exception if we don't know about the given message type
        else:
            m = "Can't handle message type '%s', function '%s' not found."
            raise sp_exceptions.MessageTypeError(m % (parsed[0], msg_func))

        # return the type of message received
        return parsed[0]

    def _handle_see_global(self, msg):



        time_recvd = msg[1]
        ball = msg[4]

        x,y = ball[1], ball[2]




















    def _handle_hear(self, msg):
        """
        Parses audible information and turns it into useful information.
        """
        print msg
        time_recvd = msg[2] # server cycle when message was heard
        sender = msg[1] # name (or direction) of who sent the message
        message = msg[3] # message string

        # handle messages from the referee, to update game state
        if sender == "referee":
            if 'goal_l' in message:
                pass



            elif 'goal_r' in message:
                pass













    def _handle_change_player_type(self, msg):
        """
        Handle player change messages.
        """

    def _handle_player_param(self, msg):
        """
        Deals with player parameter information.
        """

    def _handle_player_type(self, msg):
        """
        Handles player type information.
        """

    def _handle_server_param(self, msg):
        """
        Stores server parameter information.
        """
        return
    def _handle_init(self, msg):
        """
        Deals with initialization messages sent by the server.
        """
        return

    def _handle_error(self, msg):
        """
        Deals with error messages by raising them as exceptions.
        """

        m = "Server returned an error: '%s'" % msg[1]
        raise sp_exceptions.SoccerServerError(m)

    def _handle_warning(self, msg):
        """
        Deals with warnings issued by the server.
        """

        m = "Server issued a warning: '%s'" % msg[1]
        print sp_exceptions.SoccerServerWarning(m)

    def _handle_ok(self,msg):
        return

