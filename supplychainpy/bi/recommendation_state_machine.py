class ResponseBorg:
    """ Borg class making  class attributes global """
    _shared_response = {}  # global attribute dictionary remember to use single under score not double

    def __init__(self):
        self.__dict__ = self._shared_response


class ResponseSingleton(ResponseBorg):
    def __init__(self, **kwargs):
        # borg class instantiated at same time as the singleton updates the
        # shared_state dictionary by adding a new key-value pair
        ResponseBorg.__init__(self)
        self._shared_response.update(kwargs)

    def __str__(self):
        # returns the attribute for printing
        return str(self._shared_response)


class RecommendationStateMachine:
    def __init__(self):
        self.handlers = {}
        self.start_state = None
        self.end_states = []
        self.response = ResponseSingleton()

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.end_states.append(name)

    def set_start(self, name):
        self.start_state = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.start_state]
        except:
            raise OSError("must call .set_start() before .run()")
        if not self.end_states:
            raise OSError("at least one state must be an end_state")

        while True:
            (new_state, cargo) = handler(cargo)
            if new_state.upper() in self.end_states:
                #print("reached ", new_state)
                break
            else:
                handler = self.handlers[new_state.upper()]
