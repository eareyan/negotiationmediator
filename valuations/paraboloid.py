from math import pow, sin, pi


def seller_easy(x):
    return -1.0 * pow(x[0] - pi, 2) + 750


def buyer_easy(x):
    return -1.0 * pow(x[1] - pi, 2) + 750


def seller(x):
    return -1.0 * pow(x[0] - pi, 2) + sin(x[0]*x[1]) + 750


def buyer(x):
    return -1.0 * pow(x[1] - pi, 2) + sin(x[0]*x[1]) + 750


def get_paraboloid_lower_bounds():
    return [0.0, 0.0]


def get_paraboloid_upper_bounds():
    return [150.0, 150.0]


def get_paraboloid_ufuns():
    return {0: seller, 1: buyer}
