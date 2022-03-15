class RestoreDataHandler:
    def __init__(self, type, *args, **kwargs):
        self.type = type
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "<%s(key='%s', args='%s', kwargs='%s')>" % (self.__class__.__name__, self.type, self.args, self.kwargs)

