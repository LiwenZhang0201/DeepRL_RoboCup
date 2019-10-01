
class GameObject:
    """
    Root class for all percievable objects in the world model.
    """

    def __init__(self, distance, direction):
        """
        All objects have a distance and direction to the player, at a minimum.
        """

        self.distance = distance
        self.direction = direction

class Line(GameObject):
    """
    Represents a line on the soccer field.
    """

    def __init__(self, distance, direction, line_id):
        self.line_id = line_id
        
        GameObject.__init__(self, distance, direction)

class Goal(GameObject):
    """
    Represents a goal object on the field.
    """

    def __init__(self, distance, direction, goal_id):
        self.goal_id = goal_id

        GameObject.__init__(self, distance, direction)

class Flag(GameObject):
    """
    A flag on the field.  Can be used by the agent to determine its position.
    """

    # a dictionary mapping all flag_ids to their on-field (x, y) coordinates
    # TODO: these are educated guesses based on Figure 4.2 in the documentation.
    #       where would one find the actual coordinates, besides in the server
    #       code?
    FLAG_COORDS = {
        # perimiter flags
        "tl50": (-50, 39),
        "tl40": (-40, 39),
        "tl30": (-30, 39),
        "tl20": (-20, 39),
        "tl10": (-10, 39),
        "t0": (0, 39),
        "tr10": (10, 39),
        "tr20": (20, 39),
        "tr30": (30, 39),
        "tr40": (40, 39),
        "tr50": (50, 39),

        "rt30": (57.5, 30),
        "rt20": (57.5, 20),
        "rt10": (57.5, 10),
        "r0": (57.5, 0),
        "rb10": (57.5, -10),
        "rb20": (57.5, -20),
        "rb30": (57.5, -30),

        "bl50": (-50, -39),
        "bl40": (-40, -39),
        "bl30": (-30, -39),
        "bl20": (-20, -39),
        "bl10": (-10, -39),
        "b0": (0, -39),
        "br10": (10, -39),
        "br20": (20, -39),
        "br30": (30, -39),
        "br40": (40, -39),
        "br50": (50, -39),

        "lt30": (-57.5, 30),
        "lt20": (-57.5, 20),
        "lt10": (-57.5, 10),
        "l0": (-57.5, 0),
        "lb10": (-57.5, -10),
        "lb20": (-57.5, -20),
        "lb30": (-57.5, -30),

        "glt": (-52.5, 9.16),
        "gl": (-52.5, 0),
        "glb": (-52.5, -9.16),

        "grt": (52.5, 9.16),
        "gr": (52.5, 0),
        "grb": (52.5, -9.16),

        # penalty flags
        "plt": (-36, 20.16),
        "plc": (-36, 0),
        "plb": (-36, -20.16),

        "prt": (36, 20.16),
        "prc": (36, 0),
        "prb": (36, -20.16),

        # field boundary flags (on boundary lines)
        "lt": (-52.5, 34),
        "ct": (0, 34),
        "rt": (52.5, 34),

        "lb": (-52.5, -34),
        "cb": (0, -34),
        "rb": (52.5, -34),

        # center flag
        "c": (0, 0)
    }

    def __init__(self, distance, direction, flag_id):
        """
        Adds a flag id for this field object.  Every flag has a unique id.
        """

        self.flag_id = flag_id

        GameObject.__init__(self, distance, direction)

class MobileObject(GameObject):
    """
    Represents objects that can move.
    """

    def __init__(self, distance, direction, dist_change, dir_change, speed):
        """
        Adds variables for distance and direction deltas.
        """

        self.dist_change = dist_change
        self.dir_change = dir_change
        self.speed = speed

        GameObject.__init__(self, distance, direction)

class Ball(MobileObject):
    """
    A spcial instance of a mobile object representing the soccer ball.
    """

    def __init__(self, distance, direction, dist_change, dir_change, speed):
        
        MobileObject.__init__(self, distance, direction, dist_change,
                dir_change, speed)

class Player(MobileObject):
    """
    Represents a friendly or enemy player in the game.
    """

    def __init__(self, distance, direction, dist_change, dir_change, speed,
            team, side, uniform_number, body_direction, neck_direction):
        """
        Adds player-specific information to a mobile object.
        """

        self.team = team
        self.side = side
        self.uniform_number = uniform_number
        self.body_direction = body_direction
        self.neck_direction = neck_direction

        MobileObject.__init__(self, distance, direction, dist_change,
                dir_change, speed)

