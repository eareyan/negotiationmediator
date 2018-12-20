"""
An abstract individual surrogate.
"""
import numpy as np


class BaseSurrogate:
    num_issues = None
    X = None
    y = None
    u = None
    current_surrogate = None
    poly_features = None

    def __init__(self, num_issues, X, u):
        self.num_issues = num_issues
        self.X = X
        self.y = [u(x) for x in self.X]
        self.u = u

    def update_surrogate(self):
        pass

    def query(self, x):
        pass

    def add_observation(self, x):
        # TODO: check if we already have the observation before adding it. But note that this check becomes less important
        # TODO: in higher dimension as it is very unlikely we will query exactly the same point more than once.
        self.X = np.append(self.X, x).reshape(len(self.X) + 1, self.num_issues)
        self.y = np.append(self.y, self.u(x[0]))

    def get_current_surrogate(self):
        return self.current_surrogate

    def get_X(self):
        return self.X

    def get_y(self):
        return self.y

    def evaluate_u(self, x):
        return self.u(x)
