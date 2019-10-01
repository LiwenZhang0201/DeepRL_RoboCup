
import shelve
import numpy as np


def action_translate(action):
    for i in action.keys():
        a = action[i].replace('(', '').split(')')
        vec = np.zeros(8)
        for j in a:
            if 'turn' in j:
                vec[0] = 1
                temp = j.split()
                vec[4] = temp[1]
            elif 'dash' in j:
                vec[1] = 1
                temp = j.split()
                vec[5] = temp[1]
                vec[6] = temp[2]
            elif 'kick' in j:
                vec[2] = 1
                temp = j.split()
                vec[7] = temp[1]
                vec[8] = temp[2]
            elif 'tackle' in j:
                vec[3] = 1
                temp = j.split()
                vec[9] = temp[1]
            elif 'turn_neck' in j:
                temp = j.split()
                vec[10] = temp[1]

        action[i] = vec
    return

"""
Convert the strings in the action file into vector for training.
The vector of action is organized as [turn, dash, kick, tackle, turn_param, dash_angle, dash_power, kick_angle, 
kick_power, tackle_param, turn_neck_param]
"""


def replay_organize(state, reward, action):
    for i in state.keys():
        """
        整理成一个方向的
        
        """


    return replaybuffer


class replaybuffer():

    def __init__(self):
        self.replaybuffer1 = []
        self.replaybuffer2 = []




    def organize(self):
        s1 = shelve.open('statel')
        r1 = shelve.open('rewardl')
        a1 = shelve.open('actionl')
        s2 = shelve.open('stater')
        r2 = shelve.open('rewardr')
        a2 = shelve.open('actionr')
        action_translate(a1)
        action_translate(a2)
        self.replaybuffer1 = replay_organize(s1,r1,a1)
        self.replaybuffer2 = replay_organize(s2,r2,a2)
        s1.close()
        r1.close()
        a1.close()
        s2.close()
        r2.close()
        a2.close()

    def sample(self, batch_size):

        ind = np.random.randint(0, len(self.storage), size=batch_size)
        x, y, u, r, d = [], [], [], [], []

        for i in ind:
            X, Y, U, R, D = self.storage[i]
            x.append(np.array(X, copy=False))
            y.append(np.array(Y, copy=False))
            u.append(np.array(U, copy=False))
            r.append(np.array(R, copy=False))
            d.append(np.array(D, copy=False))

        return np.array(x), np.array(y), np.array(u), np.array(r).reshape(-1, 1), np.array(d).reshape(-1, 1)


    def clear(self):
        s1 = shelve.open('statel')
        r1 = shelve.open('rewardl')
        a1 = shelve.open('actionl')
        s2 = shelve.open('stater')
        r2 = shelve.open('rewardr')
        a2 = shelve.open('actionr')

        s1.clear()
        r1.clear()
        a1.clear()
        s2.clear()
        r2.clear()
        a2.clear()

        s1.close()
        r1.close()
        a1.close()
        s2.close()
        r2.close()
        a2.close()




