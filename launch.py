import shelve
import numpy as np
import os
import appscript
import multiprocessing as mp

if __name__ == "__main__":
    """
    Activate the server, coach and agents 
    
    """
    def game_begin(dir, cmd):
        os.chdir(dir)
        os.system(cmd)

    gt = mp.Process(target=game_begin, args=('/Users/liwenzhang/Downloads/project/server/src', './rcssserver server::auto_mode=on server::half_time=20000 server::coach_w_referee=on'))
    gt.start()

    gt2 = mp.Process(target=game_begin, args=('/Users/liwenzhang/Downloads/project/player_2v2', 'python2 agent.py 300'))
    gt2.start()

    gt3 = mp.Process(target=game_begin, args=(
    '/Users/liwenzhang/Downloads/project/server/src', './rcssserver server::auto_mode=on server::half_time=20000'))

    gt.start()








