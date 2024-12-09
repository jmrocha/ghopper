class MockDatetime:
    @classmethod
    def return_now(cls, value):
        cls._now = value

    @classmethod
    def now(cls):
        return cls._now
