from collections.abc import Iterable
import random

INVALID_RANGE_MESSAGE = (
    "Expected a range in one of the forms: "
    "'<number>' or '1,2,...,n' or '[start, stop]' or "
    "'[start,stop],step' or "
    "'[start,stop],random,n'"
)


class Range(Iterable):
    def has_next(self):
        return len(self.range_list) > 0

    def next(self) -> int:
        return self.range_list.pop()

    def reset(self):
        self.range_list = self._original_list

    def __init__(self, range_str: str):
        # range_str examples:
        #  - '1' -> single number
        #  - '1,2,3' -> sequence
        #  - '[1,10]' -> interval
        #  - '[1,10],2' -> interval with step
        #  - '[1,10],random,3' -> three random lengths between [1, 10]
        self.range_str = range_str
        self.range_list = []
        self._original_list = []
        try:
            self.range_list = self.get_range_list()
            self._original_list = self.range_list.copy()
        except Exception:
            raise AttributeError(INVALID_RANGE_MESSAGE)

    def get_range_list(self):
        if self.is_range_a_single_number():
            return self.get_list_from_single_number()
        elif self.is_range_a_sequence():
            return self.get_list_from_sequence()
        elif self.is_range_a_random_sequence():
            return self.get_list_from_random_sequence()
        else:
            return self.get_list_from_interval()

    def is_range_a_single_number(self):
        try:
            self.try_casting_range_to_int()
        except ValueError:
            return False
        return True

    def try_casting_range_to_int(self):
        int(self.range_str)

    def get_list_from_single_number(self):
        number = int(self.range_str)
        return [number]

    def is_range_a_random_sequence(self):
        try:
            return "random" == self.range_str.split(",")[2]
        except IndexError:
            return False

    def is_range_a_sequence(self):
        try:
            self.try_casting_range_to_int_list()
        except ValueError:
            return False
        return True

    def try_casting_range_to_int_list(self):
        # if range is a list: '1,2,3'
        first_element = self.range_str.split(",")[0]
        int(first_element)

    def get_list_from_sequence(self):
        sequence = self.range_str.split(",")
        sequence = list(sequence)
        return [int(x) for x in sequence]

    def get_list_from_random_sequence(self):
        l = []
        n = int(self.range_str.split(",")[3])
        u, v = self._get_bounds(self.range_str.split("random")[0])
        return random.sample(range(u, v), n)

    def get_list_from_interval(self):
        r = self.get_range_from_str()
        return list(r)

    def get_range_from_str(self):
        if self.range_has_step():
            return self.get_range_with_step()
        else:
            return self.get_range()

    def range_has_step(self):
        range_str = self.range_str.split(",")
        return len(range_str) == 3

    def get_range_with_step(self):
        range_str = self.range_str.split(",")
        # range_str: [1, 2], 1
        r = self.get_range()
        start = r.start
        stop = r.stop
        step = range_str[2]
        step = int(step)
        return range(start, stop, step)

    def get_range(self):
        range_str = self.range_str.split(",")
        # range_str: [1, 2]
        start = range_str[0].strip()[1:]
        stop = range_str[1].strip()[:-1]
        start = int(start)
        stop = int(stop)
        return range(start, stop + 1)

    def _get_bounds(self, range_str):
        range_str = range_str.split(",")
        # range_str: [1, 2]
        start = range_str[0].strip()[1:]
        stop = range_str[1].strip()[:-1]
        start = int(start)
        stop = int(stop)
        return start, stop

    def __iter__(self):
        return iter(self.range_list)

    def __len__(self):
        return len(self.range_list)

    def __repr__(self):
        return f"<Range {self.range_list}>"
