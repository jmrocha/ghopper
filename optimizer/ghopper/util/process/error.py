class ProcessError(Exception):
    pass


class CommandNotFoundError(ProcessError):
    pass


class CommandError(ProcessError):
    pass


class CommandTimeoutError(ProcessError):
    pass
