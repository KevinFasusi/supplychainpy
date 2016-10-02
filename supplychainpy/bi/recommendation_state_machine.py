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


class SkuMachine(RecommendationStateMachine):
    def __init__(self):
        super(SkuMachine, self).__init__()

    def run(self, sku_id):
        new_state = ''
        try:
            handler = self.handlers[self.start_state]
        except:
            raise OSError("call .set_start() first before .run()")
        if not self.end_states:
            raise OSError("must have at least one end_state")

        while True:
            (new_state, sku_id) = handler(sku_id)
            if new_state.upper() in self.end_states:
                break
            else:
                handler = self.handlers[new_state.upper()]
        return new_state, sku_id


class ProfileMachine(RecommendationStateMachine):
    def __init__(self):
        super(ProfileMachine, self).__init__()

    def run(self):
        new_state = ''
        try:
            handler = self.handlers[self.start_state]
        except:
            raise OSError("call .set_start() first before .run()")
        if not self.end_states:
            raise OSError("must have at least one end_state")

        while True:
            new_state = handler()
            if new_state.upper() in self.end_states:
                break
            else:
                handler = self.handlers[new_state.upper()]
        return new_state
