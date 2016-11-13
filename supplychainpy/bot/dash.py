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

from copy import deepcopy
from typing import List

from supplychainpy.bot._dash_engine import DashMachine
from supplychainpy.bot._dash_states import DashStates
from supplychainpy.bot._helpers import unpack_sentence


class ChatBot:
    """ Chat Bot for supplychainpy Reporting."""

    @staticmethod
    def chat_machine(message: str) -> List[str]:
        """ Interact with chat bot my sending a message and waiting for a response.
        Args:
            message (str):    The message for the chat bot.

        Returns:
            list:   The response from the chat bot.

        Examples:
        >>> chat_bot = ChatBot()
        >>> response = chat_bot.chat_machine(message='hello')
        """
        response = DashMachine()
        states = DashStates()
        response.add_state("start", states.initialise_chat)
        response.add_state("pronoun", states.pronoun)
        response.add_state("greeting", states.greeting)
        response.add_state("deconstruction", states.deconstruction)
        response.add_state("random_utterance", states.random_utterance)
        response.add_state("response", response, end_state=1)
        response.set_start("start")
        response.run(message=message)
        resp = deepcopy(list(states.compiled_response.shared_response.values()))
        states.compiled_response.shared_response.clear()
        return resp[0]


if __name__ == '__main__':
    dude = ChatBot()
    print(dude.chat_machine("Which SKU has the highest reorder level?"))
    #print(unpack_sentence("Which SKU has the smallest reorder level?"))