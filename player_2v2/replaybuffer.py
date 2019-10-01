import numpy as np


class ReplayBuffer(object):
    def __init__(self, max_size=1e6):
        self.storage = [[],[],[],[],[]]
        self.max_size = max_size
        self.ptr = 0


    def add(self, data, type):
        if "see" in type:

            if len(self.storage[0]) == self.max_size:
                self.storage[0][int(self.ptr)] = data
                self.ptr = (self.ptr + 1) % self.max_size
            else:
                self.storage[0].append(data)
                print(1)

        if "sense_body" in type:
            if len(self.storage[1]) == self.max_size:
                self.storage[1][int(self.ptr)] = data
                self.ptr = (self.ptr + 1) % self.max_size
            else:
                self.storage[1].append(data)

        if "hear" in type:

            if len(self.storage[2]) == self.max_size:
                self.storage[2][int(self.ptr)] = data
                self.ptr = (self.ptr + 1) % self.max_size
            else:
                self.storage[2].append(data)

        if "action" in type:
            if len(self.storage[3]) == self.max_size:
                self.storage[3][int(self.ptr)] = data
                self.ptr = (self.ptr + 1) % self.max_size
            else:
                self.storage[3].append(data)
        if "reward" in type:
            if len(self.storage[4]) == self.max_size:
                self.storage[4][int(self.ptr)] = data
                self.ptr = (self.ptr + 1) % self.max_size
            else:
                self.storage[4].append(data)
        else:
            'Unidentified message type'

    """
    need to modify the sample function
    """

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









