class AwakeError(Exception):
    """
    Base error for awake.
    """

    def __init__(self, msg):
        self.msg = msg

class AwakeNetworkError(AwakeError):
    """
    Network related error in awake.
    """
