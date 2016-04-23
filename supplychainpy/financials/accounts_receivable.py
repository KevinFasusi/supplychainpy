class Costing:
    def __init__(self):
        self.name ="base"

    def print_me(self):
        return print(self.name)


class FIFO(Costing):
    def __init__(self):
        super().__init__()

    def print_me(self):
        return print("FIFO")


class LIFO(Costing):
    def __init__(self):
        super().__init__()


class MovingAverage(Costing):
    def __init__(self):
        super().__init__()
        pass
