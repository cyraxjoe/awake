class AwakeError(Exception):
    """
    Base error for awake.
    """

class AwakeNetworkError(AwakeError):
    """
    Network related error in awake.
    """
    def __init__(self, *args, **kwargs):
        if 'original_error' in kwargs:
            self.original_error = kwargs.pop('original_error')
        super(AwakeNetworkError, self).__init__(*args, **kwargs)
