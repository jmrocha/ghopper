import math


class Math:
    @staticmethod
    def geomean(values: list[float]):
        n = len(values)
        prod = math.prod(values)
        return math.pow(prod, 1 / n)
