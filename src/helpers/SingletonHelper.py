class Singleton(type):
    """
    Metaclass that can be used to make a singleton out of any class. Check the Dispatcher for an example.
    """

    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]
