__author__ = 'Fasusi'

#inuput job/ failure rates, etc
class Machine:
    def __init__(self):
        # user specified features
        self.name = None
        self.maximum_throughput = None
        self.processing_time = None
        self.setup_time = None
        self.down_time = 0
        # generic features

    # remember to build all methods that control machine up-time behaviour
    def add_down_time(self):
        self.down_time += 1

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '{}'.format(self.name)


# TODO-feature singleton with global scope for production Job, holds sequence and cycle time

class MachineBuilder:
    """Abstract builder"""

    def __init__(self):
        self.machine = None

    def make_new_machine(self):
        self.machine = Machine()


class ProductionDirector:
    def __init__(self, machine_builder: MachineBuilder):
        self._machine_builder = machine_builder

    def construct_machine(self, name: str = "", maximum_throughput: int = 0, processing_time: int = 0):
        self._machine_builder.make_new_machine()
        self._machine_builder.machine.name = name
        self._machine_builder.machine.maximum_throughput = maximum_throughput
        self._machine_builder.machine.processing_time = processing_time

    def add_down_time(self):
        self._machine_builder.machine.down_time = self._machine_builder.machine.add_down_time()

    @property
    def machine(self) -> Machine():
        return self._machine_builder.machine


# use to add the most generic features to all machines built, allow the abstract class constructor to build the rest
# based on the client. Create different concrete builders for different types of machine with different generic features
class SimpleMachineBuilder(MachineBuilder):
    """Concrete builder, adds generic features to the machine"""
    pass
