# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
