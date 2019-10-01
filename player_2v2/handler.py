import collections
import Queue as queue

import message_parser
import sp_exceptions
import game_object
from world_model import WorldModel


# should we print messages received from the server?
PRINT_SERVER_MESSAGES = True

# should we print commands sent to the server?
PRINT_SENT_COMMANDS = True

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

    def __init__(self, world_model, teamname):
        self.wm = world_model
        self.teamname = teamname


    def handle_message(self, msg):
        """
        Takes a raw message direct from the server, parses it, and stores its
        data in the world and body model objects given at init.  Returns the
        type of message received.
        """


        f2 = open("resv%s.txt"%self.teamname, "a+")


        # get all the expressions contained in the given message
        parsed = message_parser.parse(msg)

        if PRINT_SERVER_MESSAGES:
            for i in xrange(len(parsed)):
                f2.write(str(parsed[i]) + "!")
            f2.write("\n")
            f2.close()
        # this is the name of the function that should be used to handle
        # this message type.  we pull it from this object dynamically to
        # avoid having a huge if/elif/.../else statement.
        msg_func = "_handle_%s" % parsed[0]

        if hasattr(self, msg_func):
            # call the appropriate function with this message
            handled = getattr(self, msg_func).__call__(parsed)

        # throw an exception if we don't know about the given message type
        else:
            m = "Can't handle message type '%s', function '%s' not found."
            raise sp_exceptions.MessageTypeError(m % (parsed[0], msg_func))
        # return the type of message received
        return [parsed[0], parsed[1], handled]

    def _handle_see(self, msg):
        """
        Parses visual information in a message and turns it into useful data.

        This comes to us as a list of lists.  Each list contains another list as
        its first element, the contents of which describe a particular object.
        The other items of the list are data pertaining to the object.  We parse
        each list into its own game object, then insert those game objects into
        the world model.
        """

        # the simulation cycle of the soccer server
        # TODO: we should probably use this somewhere...
        sim_time = msg[1]

        # store new values before changing those in the world model.  all new
        # values replace those in the world model at the end of parsing.
        new_ball = None
        new_flags = []
        new_goals = []
        new_lines = []
        new_players = []

        # iterate over all the objects given to us in the last see message
        for obj in msg[2:]:
            name = obj[0]
            members = obj[1:]

            # get basic information from the object.  different numbers of
            # parameters (inconveniently) specify different types and
            # arrangements of data received for the object.

            # default values for object data
            distance = None
            direction = None
            dist_change = None
            dir_change = None
            body_dir = None
            neck_dir = None

            # a single item object means only direction
            if len(members) == 1:
                direction = members[0]

            # objects with more items follow a regular pattern
            elif len(members) >= 2:
                distance = members[0]
                direction = members[1]

                # include delta values if present
                if len(members) >= 4:
                    dist_change = members[2]
                    dir_change = members[3]

                # include body/neck values if present
                if len(members) >= 6:
                    body_dir = members[4]
                    neck_dir = members[5]

            # parse flags
            if name[0] == 'f':
                # since the flag's name sometimes contains a number, the parser
                # recognizes it as such and converts it into an int.  it's
                # always the last item when it's a number, so we stringify the
                # last item of the name to convert any numbers back.
                name[-1] = str(name[-1])

                # the flag's id is its name's members following the f as a string
                flag_id = ''.join(name[1:])

                new_flags.append(game_object.Flag(distance, direction, flag_id))

            # parse players
            elif name[0] == 'p':
                # extract any available information from the player object's name
                teamname = None
                uniform_number = None

                if len(name) >= 2:
                    teamname = name[1]
                if len(name) >= 3:
                    uniform_number = name[2]
                if len(name) >= 4:
                    position = name[3]

                # figure out the player's side
                side = None
                if teamname is not None:
                    # if they're on our team, they're on our side
                    if teamname == self.wm.teamname:
                        side = self.wm.side
                    # otherwise, set side to the other team's side
                    else:
                        if self.wm.side == WorldModel.SIDE_L:
                            side = WorldModel.SIDE_R
                        else:
                            side = WorldModel.SIDE_L

                # calculate player's speed
                speed = None
                # TODO: calculate player's speed!

                new_players.append(game_object.Player(distance, direction,
                    dist_change, dir_change, speed, teamname, side,
                    uniform_number, body_dir, neck_dir))

            # parse goals
            elif name[0] == 'g':
                # see if we know which side's goal this is
                goal_id = None
                if len(name) > 1:
                    goal_id = name[1]

                new_goals.append(game_object.Goal(distance, direction, goal_id))

            # parse lines
            elif name[0] == 'l':
                # see if we know which line this is
                line_id = None
                if len(name) > 1:
                    line_id = name[1]

                new_lines.append(game_object.Line(distance, direction, line_id))

            # parse the ball
            elif name[0] == 'b':
                # TODO: handle speed!
                new_ball = game_object.Ball(distance, direction, dist_change,
                        dir_change, None)

            # object very near to but not viewable by the player are 'blank'

            # the out-of-view ball
            elif name[0] == 'B':
                new_ball = game_object.Ball(None, None, None, None, None)

            # an out-of-view flag
            elif name[0] == 'F':
                new_flags.append(game_object.Flag(None, None, None))

            # an out-of-view goal
            elif name[0] == 'G':
                new_goals.append(game_object.Goal(None, None, None))

            # an out-of-view player
            elif name[0] == 'P':
                new_players.append(game_object.Player(None, None, None, None,
                    None, None, None, None, None, None))

            # an unhandled object type
            else:
                raise ObjectTypeError("Unknown object: '" + str(obj) + "'")

        # tell the WorldModel to update any internal variables based on the
        # newly gleaned information.
        self.wm.process_new_info(new_ball, new_flags, new_goals, new_players,
                new_lines)





        """
        To do
        """
        return 1



    def _handle_hear(self, msg):
        """
        Parses audible information and turns it into useful information.
        """

        time_recvd = msg[1] # server cycle when message was heard
        sender = msg[2] # name (or direction) of who sent the message
        message = msg[3] # message string

        # ignore messages sent by self (NOTE: would anybody really want these?)
        if sender == "self":
            return

        # handle messages from the referee, to update game state
        elif sender == "referee":
            # change the name for convenience's sake
            mode = message

            # deal first with messages that shouldn't be passed on to the agent

            # keep track of scores by setting them to the value reported.  this
            # precludes any possibility of getting out of sync with the server.
            if mode.startswith(WorldModel.RefereeMessages.GOAL_L):
                # split off the number, the part after the rightmost '_'
                self.wm.score_l = int(mode.rsplit("_", 1)[1])
                return
            elif mode.startswith(WorldModel.RefereeMessages.GOAL_R):
                self.wm.score_r = int(mode.rsplit("_", 1)[1])
                return

            # ignore these messages, but pass them on to the agent. these don't
            # change state but could still be useful.
            elif (mode == WorldModel.RefereeMessages.FOUL_L or
                  mode == WorldModel.RefereeMessages.FOUL_R or
                  mode == WorldModel.RefereeMessages.GOALIE_CATCH_BALL_L or
                  mode == WorldModel.RefereeMessages.GOALIE_CATCH_BALL_R or
                  mode == WorldModel.RefereeMessages.TIME_UP_WITHOUT_A_TEAM or
                  mode == WorldModel.RefereeMessages.HALF_TIME or
                  mode == WorldModel.RefereeMessages.TIME_EXTENDED):

                # messages are named 3-tuples of (time, sender, message)
                ref_msg = self.Message(time_recvd, sender, message)

                # pass this message on to the player and return
                self.wm.last_message = ref_msg
                return

            # deal with messages that indicate game mode, but that the agent
            # doesn't need to know about specifically.
            else:
                # set the mode to the referee reported mode string
                self.wm.play_mode = mode
                return

        # all other messages are treated equally
        else:
            # update the model's last heard message
            new_msg = MessageHandler.Message(time_recvd, sender, message)
            self.wm.prev_message = new_msg


        """
                To do
                """
        return 1




    def _handle_sense_body(self, msg):
        """
        Deals with the agent's body model information.
        """

        # update the body model information when received. each piece of info is
        # a list with the first item as the name of the data, and the rest as
        # the values.
        for info in msg[2:]:
            name = info[0]
            values = info[1:]

            if name == "view_mode":
                self.wm.view_quality = values[0]
                self.wm.view_width = values[1]
            elif name == "stamina":
                self.wm.stamina = values[0]
                self.wm.effort = values[1]
            elif name == "speed":
                self.wm.speed_amount = values[0]
                self.wm.speed_direction = values[1]
            elif name == "head_angle":
                self.wm.neck_direction = values[0]

            # these update the counts of the basic actions taken
            elif name == "kick":
                self.wm.kick_count = values[0]
            elif name == "dash":
                self.wm.dash_count = values[0]
            elif name == "turn":
                self.wm.turn_count = values[0]
            elif name == "say":
                self.wm.say_count = values[0]
            elif name == "turn_neck":
                self.wm.turn_neck_count = values[0]
            elif name == "catch":
                self.wm.catch_count = values[0]
            elif name == "move":
                self.wm.move_count = values[0]
            elif name == "change_view":
                self.wm.change_view_count = values[0]

            # we leave unknown values out of the equation
            else:
                pass
        """
                To do
                """
        return 1




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
        
        # each list is two items: a value name and its value.  we add them all
        # to the ServerParameters class inside WorldModel programmatically.
        for param in msg[1:]:
            # put all [param, value] pairs into the server settings object
            # by setting the attribute programmatically.
            if len(param) != 2:
                continue
            
            # the parameter and its value
            key = param[0]
            value = param[1]

            # set the attribute if it was accounted for, otherwise alert the user
            if hasattr(self.wm.server_parameters, key):
                setattr(self.wm.server_parameters, key, value)
            else:
                raise AttributeError("Couldn't find a matching parameter in "
                        "ServerParameters class: '%s'" % key)

    def _handle_init(self, msg):
        """
        Deals with initialization messages sent by the server.
        """

        # set the player's uniform number, side, and the play mode as returned
        # by the server directly after connecting.
        side = msg[1]
        uniform_number = msg[2]
        play_mode = msg[3]

        self.wm.side = side
        self.wm.uniform_number = uniform_number
        self.wm.play_mode = play_mode

    def _handle_error(self, msg):
        """
        Deals with error messages by raising them as exceptions.
        """

        m = "Server returned an error: '%s'" % msg[1]
        print msg
        raise sp_exceptions.SoccerServerError(m)


    def _handle_warning(self, msg):
        """
        Deals with warnings issued by the server.
        """

        m = "Server issued a warning: '%s'" % msg[1]
        print sp_exceptions.SoccerServerWarning(m)

class ActionHandler:
    """
    Provides facilities for sending commands to the soccer server.  Contains all
    possible commands that can be sent, as well as everything needed to send
    them.  All basic command methods are aliases for placing that command in the
    internal queue and sending it at the appropriate time.
    """

    class CommandType:
        """
        A static class that defines all basic command types.
        """

        # whether the command can only be sent once per cycle or not
        TYPE_PRIMARY = 0
        TYPE_SECONDARY = 1

        # command types corresponding to valid commands to send to the server
        CATCH = "catch"
        CHANGE_VIEW = "change_view"
        DASH = "dash"
        KICK = "kick"
        MOVE = "move"
        SAY = "say"
        SENSE_BODY = "sense_body"
        TURN = "turn"
        TURN_NECK = "turn_neck"
        TACKLE = "tackle"

        def __init__(self):
            raise NotImplementedError("Can't instantiate a CommandType, access "
                    "its members through ActionHandler instead.")

    # a command for our queue containing an id and command text
    Command = collections.namedtuple("Command", "cmd_type text")

    def __init__(self, server_socket, teamname):
        """
        Save the socket that connects us to the soccer server to allow us to
        send it commands.
        """

        self.sock = server_socket

        # this contains all requested actions for the current and future cycles
        self.q = queue.Queue()
        self.teamname = teamname

    def send_commands(self):
        """
        Sends all the enqueued commands.
        """

        f1 = open("send%s.txt"%self.teamname, "a+")



        # we only send the most recent primary command
        primary_cmd = None

        # dequeue all enqueued commands and send them
        while 1:
            try:
                cmd = self.q.get_nowait()
            except queue.Empty:
                break

            # save the most recent primary command and send it at the very end
            if cmd.cmd_type == ActionHandler.CommandType.TYPE_PRIMARY:
                primary_cmd = cmd
            # send other commands immediately
            else:
                if PRINT_SENT_COMMANDS:
                    f1.write( "sent:"+ cmd.text+ "\n")

                self.sock.send(cmd.text)
                return cmd.txt

            # indicate that we finished processing a command
            self.q.task_done()

        # send the saved primary command, if there was one
        if primary_cmd is not None:
            if PRINT_SENT_COMMANDS:
                f1.write( "sent:"+ primary_cmd.text+ "\n")

            self.sock.send(primary_cmd.text)
            return primary_cmd.text
        f1.close()


    def move(self, x, y):
        """
        Teleport the player to some location on the field.  Only works before
        play begins, ie. pre-game, before starting again at half-time, and
        post-goal.  If an invalid location is specified, player is teleported to
        a random location on their side of the field.
        """

        msg = "(move %.10f %.10f)" % (x, y)

        # create the command object for insertion into the queue
        cmd_type = ActionHandler.CommandType.TYPE_PRIMARY
        cmd = ActionHandler.Command(cmd_type, msg)

        self.q.put(cmd)

    def turn(self, relative_degrees):
        """
        Turns the player's body some number of degrees relative to its current
        angle.
        """

        # disallow unreasonable turning
        assert -180 <= relative_degrees <= 180

        msg = "(turn %.10f)" % relative_degrees

        # create the command object for insertion into the queue
        cmd_type = ActionHandler.CommandType.TYPE_PRIMARY
        cmd = ActionHandler.Command(cmd_type, msg)

        self.q.put(cmd)

    def dash(self, power):
        """
        Accelerate the player in the direction its body currently faces.
        """

        msg = "(dash %.10f)" % power

        # create the command object for insertion into the queue
        cmd_type = ActionHandler.CommandType.TYPE_PRIMARY
        cmd = ActionHandler.Command(cmd_type, msg)

        self.q.put(cmd)

    def kick(self, power, relative_direction):
        """
        Accelerates the ball with the given power in the given direction,
        relative to the current direction of the player's body.
        """

        msg = "(kick %.10f %.10f)" % (power, relative_direction)

        # create the command object for insertion into the queue
        cmd_type = ActionHandler.CommandType.TYPE_PRIMARY
        cmd = ActionHandler.Command(cmd_type, msg)

        self.q.put(cmd)

    def catch(self, relative_direction):
        """
        Attempts to catch the ball and put it in the goalie's hand.  The ball
        remains there until the goalie kicks it away.
        """

        msg = "(catch %.10f)" % relative_direction

        # create the command object for insertion into the queue
        cmd_type = ActionHandler.CommandType.TYPE_PRIMARY
        cmd = ActionHandler.Command(cmd_type, msg)

        self.q.put(cmd)

    def say(self, message):
        """
        Says something to other players on the field.  Messages are restricted
        in length, but that isn't enforced here.
        """

        msg = "(say %s)" % message

        # create the command object for insertion into the queue
        cmd_type = ActionHandler.CommandType.TYPE_SECONDARY
        cmd = ActionHandler.Command(cmd_type, msg)

        self.q.put(cmd)

    def turn_neck(self, relative_direction):
        """
        Rotates the player's neck relative to its previous direction.  Neck
        angle is relative to body angle.
        """

        msg = "(turn_neck %.10f)" % relative_direction

        # create the command object for insertion into the queue
        cmd_type = ActionHandler.CommandType.TYPE_SECONDARY
        cmd = ActionHandler.Command(cmd_type, msg)

        self.q.put(cmd)

    def tackle(self,relative_direction):
        """

        contest the ball
        """
        msg = "(tackle %.10f)" % relative_direction

        # create the command object for insertion into the queue
        cmd_type = ActionHandler.CommandType.TYPE_SECONDARY
        cmd = ActionHandler.Command(cmd_type, msg)

        self.q.put(cmd)