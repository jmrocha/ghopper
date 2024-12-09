class Llvm12Error(Exception):
    pass


class ClangError(Llvm12Error):
    pass


class ClangNotFoundError(ClangError):
    pass


class OptError(Llvm12Error):
    pass


class OptNotFoundError(OptError):
    pass


class LlcError(Llvm12Error):
    pass


class LlcNotFoundError(LlcError):
    pass
