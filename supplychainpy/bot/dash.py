# Copyright (c) 2015-2016, Kevin Fasusi
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

import random

from supplychainpy.bot.controller import master_sku_list, database_connection_uri
from textblob import TextBlob
from textblob import Word


class ChatBot():
    SALUTATION_KEYWORDS = ("hi", "hello", "wassup", "sup", "what's up", "ello", "how's tricks?")
    SALUTATION_RESPONSES = ["hi", "hello", "how's tricks?"]
    # NICKNAMES = ("bud", "s") use nicknames when you can ascertain the gender of the user from the user name in config
    # file. Append this name name to responses returning a fact.
    UNKNOWN_UTTERANCE = ["Not sure what you are saying!", "I don't understand!"]
    DEPENDECIES = [
        ('question', ('biggest', 'smallest'), (('WP', 0), ('VBZ', 1), ('DT', 2), ('JJS', 3), ('NN', 4))),
        ('question', ('shortage', 'revenue', 'excess'),
         (('WP', 0), ('VBZ', 1), ('DT', 2), ('NN', 3), ('IN', 4), ('NNP', 5))),
        ('direction', ('explain', 'describe'), (('NNP', 0), ('NNP', 1), ('NNP', 2))),
        ('direction', ('explain', 'describe'), (('NN', 0), ('NNP', 1))),
        ('direction', ('explain', 'describe'), (('VB', 0), ('NNP', 1))),
        ('direction', ('explain', 'describe'), (('CD', 0), ('JJ', 1))),
        ('direction', ('explain', 'describe'), (('NNP', 0), ('NNP', 1)))
    ]
    DIRECTION = ("describe", "explain", "show", "view")

    def __init__(self):
        self._master_sku_list = self._get_msk()

    @property
    def retrieve_master_sku_list(self):
        return self._master_sku_list

    def receive_message(self, message: str) -> list:

        response = self._deconstruct_message(message=message)
        response2 = self.question_check(message)

        return response if response2 is None else response2

    def match_tags(self, message: str):
        pass

    def _deconstruct_message(self, message: str) -> str:
        u_wot_m8 = TextBlob(message)
        greeting = [random.choice(self.SALUTATION_RESPONSES) for word in u_wot_m8.words if
                    word.lower() in self.SALUTATION_KEYWORDS]
        greeting = [random.choice(self.UNKNOWN_UTTERANCE)] if len(greeting) == 0 else greeting
        return greeting

    def unpack_sentence(self, message):
        u_wot_m8 = TextBlob(message)
        print(u_wot_m8.tags)
        for i in u_wot_m8.tags:
            syn = Word(i[0])
            print('word: {}\n lemmatize: {}\n lemma: {}\n synsets: {}\n'.format(i[0], syn.lemmatize, syn.lemma,
                                                                                syn.synsets))

    def question_check(self, message):
        u_wot_m8 = TextBlob(message)
        tags = [i for i in u_wot_m8.tags]
        tag_check = self.deconstruct_message(tags=tags)
        return tag_check

    def deconstruct_message(self, tags, message: str = None) -> list:
        if message is not None:
            u_wot_m8 = TextBlob(message)
        # deconstruct using tree and classifier then select path
        new_tags = tuple([(i[1], index) for index, i in enumerate(tags)])
        for i in self.DEPENDECIES:
            if i[2] == new_tags:
                if i[0] == 'question':
                    return self.understand_question(i, tags)
                elif i[0] == 'direction':
                    return self.understand_direction(tags)
                elif i[0] == 'instruction':
                    pass
                elif i[0] == 'statement':
                    pass
                elif i[0] == 'greeting':
                    return [random.choice(self.SALUTATION_RESPONSES) for word in u_wot_m8.words if
                            word.lower() in self.SALUTATION_KEYWORDS]
                else:
                    return [random.choice(self.UNKNOWN_UTTERANCE)]

    def understand_direction(self, tags):
        # understand the direction
        return self.direction_describe(tags)

    def understand_question(self, dependency, tags):
        # understand what the question is asking
        return self.min_max_check(dependency, tags[3][0])

    def direction_describe(self, tags):
        for i in self._master_sku_list:
            if i[1] == tags[1][0]:
                return ['<a href=\"/sku_detail/{}\">Here you go!</a>'.format(i[0])]

    def min_max_check(self, dependency: list, jjs: str):
        max = dependency[1][0]
        min = dependency[1][1]
        jj_word = Word(jjs)
        max_word = Word(max)
        min_word = Word(min)

        for word in jj_word.synsets:
            for set in min_word.synsets:
                if word == set:
                    return ["Are you asking what the smallest issue is?"]

        return ["Are you asking what the biggest issue is?"]

        # print(max_word.synsets, min_word.synsets, 'jj: {} '.format(jj_word.synsets))

    def construct_response(self):
        pass

    def _get_msk(self):
        msk = master_sku_list(database_connection_uri())
        return msk


if __name__ == '__main__':
    dude = ChatBot()
    print(dude.receive_message('Describe KR202-209?'))
