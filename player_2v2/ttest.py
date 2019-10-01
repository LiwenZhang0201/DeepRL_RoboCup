import numpy as np
from replaybuffer import ReplayBuffer






dict = {"tl50": np.array([-50, 39]),
        "tl40": np.array([-40, 39]),
        "tl30": np.array([-30, 39]),
        "tl20": np.array([-20, 39]),
        "tl10": np.array([-10, 39]),
        "t0": np.array([0, 39]),
        "tr10": np.array([10, 39]),
        "tr20": np.array([20, 39]),
        "tr30": np.array([30, 39]),
        "tr40": np.array([40, 39]),
        "tr50": np.array([50, 39]),

        "rt30": np.array([57.5, 30]),
        "rt20": np.array([57.5, 20]),
        "rt10": np.array([57.5, 10]),
        "r0": np.array([57.5, 0]),
        "rb10": np.array([57.5, -10]),
        "rb20": np.array([57.5, -20]),
        "rb30": np.array([57.5, -30]),

        "bl50": np.array([-50, -39]),
        "bl40": np.array([-40, -39]),
        "bl30": np.array([-30, -39]),
        "bl20": np.array([-20, -39]),
        "bl10": np.array([-10, -39]),
        "b0": np.array([0, -39]),
        "br10": np.array([10, -39]),
        "br20": np.array([20, -39]),
        "br30": np.array([30, -39]),
        "br40": np.array([40, -39]),
        "br50": np.array([50, -39]),

        "lt30": np.array([-57.5, 30]),
        "lt20": np.array([-57.5, 20]),
        "lt10": np.array([-57.5, 10]),
        "l0": np.array([-57.5, 0]),
        "lb10": np.array([-57.5, -10]),
        "lb20": np.array([-57.5, -20]),
        "lb30": np.array([-57.5, -30]),

        "glt": np.array([-52.5, 9.16]),
        "gl": np.array([-52.5, 0]),
        "glb": np.array([-52.5, -9.16]),

        "grt": np.array([52.5, 9.16]),
        "gr": np.array([52.5, 0]),
        "grb": np.array([52.5, -9.16]),

        # penalty flags
        "plt": np.array([-36, 20.16]),
        "plc": np.array([-36, 0]),
        "plb": np.array([-36, -20.16]),

        "prt": np.array([36, 20.16]),
        "prc": np.array([36, 0]),
        "prb": np.array([36, -20.16]),

        # field boundary flags (on boundary lines)
        "lt": np.array([-52.5, 34]),
        "ct": np.array([0, 34]),
        "rt": np.array([52.5, 34]),

        "lb": np.array([-52.5, -34]),
        "cb": np.array([0, -34]),
        "rb": np.array([52.5, -34]),

        # center flag
        "c": np.array([0, 0])}





a = 'a'
f = open("resv %s.txt"%a, "a+")





