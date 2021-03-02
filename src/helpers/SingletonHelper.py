class Singleton(type):
    """
    Metaclass that can be used to make a singleton out of any class. Check the Dispatcher for an example.
    """

    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance
