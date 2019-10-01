#!/usr/bin/env python

import threading
import time
import random
import numpy as np

import sock
import sp_exceptions
import handler


class Agent:
    def __init__(self):
        # whether we're connected to a server yet or not
        self.__connected = False

        # set all variables and important objects to appropriate values for
        # pre-connect state.

        # the socket used to communicate with the server
        self.__sock = None

        # models and the message handler for parsing and storing information
        self.wm = None
        self.msg_handler = None

        # parse thread and control variable
        self.__parsing = False
        self.__msg_thread = None

        self.__thinking = False # think thread and control variable
        self.__think_thread = None

        # whether we should run the think method
        self.__should_think_on_data = False

        # whether we should send commands
        self.__send_commands = False

        self.teamname = None
        self.sim_time = 0
        self.action_handler = None
        self.mode = None



    def connect(self, host, port, mode, teamname = None, version='15.5.0'):
        """
        Gives us a connection to the server as one player on a team.  This
        immediately connects the agent to the server and starts receiving and
        parsing the information it sends.
        """

        # determine the mode of coach is online or off-line
        self.mode = mode
        self.teamname = None

        # if already connected, raise an error since user may have wanted to
        # connect again to a different server.
        if self.__connected:
            msg = "Cannot connect while already connected, disconnect first."
            raise sp_exceptions.AgentConnectionStateError(msg)

        # the pipe through which all of our communication takes place
        self.__sock = sock.Socket(host, port)

        # our models of the world and our body

        # set the team name of the world model to the given name

        # handles all messages received from the server
        self.msg_handler = handler.MessageHandler()


        # set up our threaded message receiving system
        self.__parsing = True  # tell thread that we're currently running
        self.__msg_thread = threading.Thread(target=self.__message_loop,
                                             name="message_loop")
        self.__msg_thread.daemon = True  # dies when parent thread dies

        # start processing received messages. this will catch the initial server
        # response and all subsequent communication.
        self.__msg_thread.start()

        # send the init message and allow the message handler to handle further
        # responses.




        init_address = self.__sock.address
        if self.mode == 'off':

            init_msg = "(init (version %s))"
            self.__sock.send(init_msg % (version))
        elif self.mode == 'on':
            init_msg = "(init %s (version %s))"
            self.__sock.send(init_msg % (teamname, version))


        # wait until the socket receives a response from the server and gets its
        # assigned port.
        while self.__sock.address == init_address:
            time.sleep(0.0001)



        # set connected state.  done last to prevent state inconsistency if
        # something goes wrong beforehand.
        self.__connected = True


        self.__sock.send('(eye on)')
        self.__sock.send('(ear on)')


    def send_cmd(self,input):
        self.__sock.send(input)

    def disconnect(self):
        """
        Tell the loop threads to stop and signal the server that we're
        disconnecting, then join the loop threads and destroy all our inner
        methods.

        Since the message loop thread can conceiveably block indefinitely while
        waiting for the server to respond, we only allow it (and the think loop
        for good measure) a short time to finish before simply giving up.

        Once an agent has been disconnected, it is 'dead' and cannot be used
        again.  All of its methods get replaced by a method that raises an
        exception every time it is called.
        """

        # don't do anything if not connected
        if not self.__connected:
            return

        # tell the loops to terminate
        self.__parsing = False
        self.__thinking = False

        # tell the server that we're quitting
        self.__sock.send("(bye)")

        # tell our threads to join, but only wait breifly for them to do so.
        # don't join them if they haven't been started (this can happen if
        # disconnect is called very quickly after connect).
        if self.__msg_thread.is_alive():
            self.__msg_thread.join(0.01)

        if self.__think_thread.is_alive():
            self.__think_thread.join(0.01)

        # reset all standard variables in this object.  self.__connected gets
        # reset here, along with all other non-user defined internal variables.
        Agent.__init__(self)

    def __message_loop(self):
        """
        Handles messages received from the server.

        This SHOULD NOT be called externally, since it's used as a threaded loop
        internally by this object.  Calling it externally is a BAD THING!
        """

        # loop until we're told to stop
        while self.__parsing:
            # receive message data from the server and pass it along to the
            # world model as-is.  the world model parses it and stores it within
            # itself for perusal at our leisure.
            raw_msg = self.__sock.recv()
            msg_type = self.msg_handler.handle_message(raw_msg)[0]





    def setup_environment(self):
        """
        Called before the think loop starts, this allows the user to store any
        variables/objects they'll want access to across subsequent calls to the
        think method.
        """

        self.in_kick_off_formation = False



if __name__ == "__main__":
    import sys
    import multiprocessing as mp


    # enforce corrent number of arguments, print help otherwise



    a = Agent()
    a.connect("localhost", 6001, sys.argv[1], sys.argv[2])

    #argv[1] should give the mode of the coach and argv[2] should give the team name which is valid only when mode is 'on'.

    print "Spawned 1 agents."
    print
    print "Playing soccer..."


    action = raw_input("What is the next action? ")
    a.send_cmd(action)


    # wait until killed to terminate agent processes
    try:
        while 1:

            action = raw_input("What is the next action? ")
            a.send_cmd(action)
            time.sleep(0.05)


    except KeyboardInterrupt:


        print "Killing agent threads..."

        # terminate all agent processes
        count = 0
        for at in agentthreads:
            print "  Terminating agent %d..." % count
            at.terminate()
            count += 1
        print "Killed %d agent threads." % (count - 1)

        print
        print "Exiting."
        sys.exit()


