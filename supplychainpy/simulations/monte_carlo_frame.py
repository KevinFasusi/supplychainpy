class MainFrame:
    """ Borg class making shared frame global """
    _shared_frame = {}

    def __init__(self):
        self.__dict__ = self._shared_frame


class BuildFrame(MainFrame):
    """ Shares the shared frame attribute with all instances to be used when using multi-threading for  """


    def __init__(self, **kwargs):
        # borg class (MainFrame) instantiated at same time as the singleton updates the
        MainFrame.__init__(self)
        self._shared_frame.update(kwargs)


    def __str__(self):
        # returns the attribute for printing
        return str(self._shared_frame)
