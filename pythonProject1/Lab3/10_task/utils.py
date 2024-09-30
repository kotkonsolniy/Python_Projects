from math import exp, pi


class Norm:
    """
    Norm object represents normal distribution.
    :param mu: mean
    :param std: standard deviation
    """
    def __init__(self, mu: float, std: float):
        self.__mu = mu
        self.__std = std
        self.__step = 1e-3

    def pdf(self, x: float) -> float:
        """
        Get value of probability density function (PDF).
        :param x: value to get PDF

        :returns: PDF
        """
        return self.__pdf(x)

    def __pdf(self, x):
        return exp(-(x - self.__mu)**2 / (2 * self.__std**2)) / self.__std / (2 * pi)**0.5


def normalize_angle(angle: float) -> float:
    """
    Normalizes angle, making it equal to value from [-2*pi; 2*pi].
    :param angle: angle value in radians

    :returns: normalizaed angle in radians
    """
    while angle <= -pi:
        angle += 2 * pi
    while angle > pi:
        angle -= 2 * pi
    return angle


def argmax(a: list) -> int:
    """
    Returns argmax of iterable object
    :param a: iterable object

    :returns: position of maximum
    """
    x = a[0]
    pos = 0
    for i, v in enumerate(a):
        if v > x:
            pos, x = i, v
    return pos
