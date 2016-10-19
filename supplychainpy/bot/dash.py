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

import os
import random
import re

from supplychainpy._helpers._db_connection import database_connection_uri
from supplychainpy.bot.controller import (master_sku_list, excess_controller, shortage_controller, revenue_controller)
from supplychainpy._helpers._decorators import preprocess_text, strip_punctuation, pickle_response
from textblob import TextBlob
from textblob import Word


class ChatBot:
    """ Chat Bot for supplychainpy Reporting."""

    APP_DIR = os.path.dirname(__file__, )
    REL_PATH = 'dash.pickle'
    REL_PATH_CONFIG = 'config.pickle'
    ABS_FILE_PATH = os.path.abspath(os.path.join(APP_DIR, '..', REL_PATH))
    ABS_FILE_PATH_CONFIG = os.path.abspath(os.path.join(APP_DIR, '..', REL_PATH_CONFIG))

    KEYWORDS = ('average', 'retail', 'economic')

    ANALYSIS_KEYWORDS = ("excess", "shortage", "revenue",)

    SALUTATION_KEYWORDS = ("hi", "hello", "wassup", "sup", "what's up", "ello", "how's tricks?")

    SALUTATION_RESPONSES = ["hi", "hello", "how's tricks?"]

    UNKNOWN_UTTERANCE = ["Not sure what you are saying!", "I don't understand!"]

    SEMANTIC_DICTIONARY = [
        ('question', ('biggest', 'smallest'), (('WP', 0), ('VBZ', 1), ('DT', 2), ('JJS', 3), ('NN', 4))),
        ('question', ('biggest', 'smallest'), (('WDT', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5))),
        ('question', ('shortage', 'revenue', 'excess'),
         (('WP', 0), ('VBZ', 1), ('DT', 2), ('NN', 3), ('IN', 4), ('NNP', 5))),
        ('question', ('biggest', 'smallest'), (('WDT', 0), ('NNP', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5))),
        ('question', ('average'), (('WP', 0), ('VBZ', 1), ('DT', 2), ('JJ', 3), ('NN', 4), ('IN', 5), ('NNP', 6))),
        ('direction', ('explain', 'describe'), (('NNP', 0), ('NNP', 1), ('NNP', 2))),
        ('direction', ('explain', 'describe'), (('NN', 0), ('NNP', 1))),
        ('direction', ('explain', 'describe'), (('VB', 0), ('NNP', 1))),
        ('direction', ('explain', 'describe'), (('CD', 0), ('JJ', 1))),
        ('direction', ('explain', 'describe'), (('NNP', 0), ('NNP', 1))),
        ('statement', ('today', 'yesterday', 'tomorrow'), (('MD', 0), ('PRP', 1), ('VB', 2), ('NN', 3))),
        ('question', ('biggest', 'smallest'), (('JJS', 0), ('NN', 1))),

    ]

    DIRECTION = ("describe", "explain", "show", "view")

    NOUN_PLURAL = [
        "There are {} in any organisation. ",
        "Let's keep focus and improve the {}.",
        "yesterdays successes can become {} problems. Keep fighting the good fight."
    ]

    NOUN_SINGULAR = [
        "{}!",
        "Again {}.It's probably time for a coffee!",
        "{} may be hard, don't let the details get you down.",
        "{} we will be running the show."
    ]

    SELF_REFERENCING = [
        "I'm busy keeping the data clean.",
        "I want to help you work smart!",
        "I see widgets in my sleep.",
        "Ready to optimise, optimise, optimise.",
        "I think there is work to be done."
    ]

    NONE_RESPONSES = [
        "It's probably time for a coffee!",
        "It's probably time for some tea!",
        "Don't let the details get you down",
        "Keep fighting the good fight",

    ]

    RANDOM_STATEMENTS = [
        "I see SKUs in my sleep",
    ]

    def __init__(self):
        self._master_sku_list = self._get_msk()

    @property
    def retrieve_master_sku_list(self) -> list:
        """ Retrieves the entire master sku list for use by the bot

        Returns:
            list: List of SKU Ids from master_sku_table.

        """
        return self._master_sku_list

    def chat(self, message: str) -> list:

        response = self.construct_response(message)

        return response

    @preprocess_text
    def clean_up(self, message):

        return message

    @pickle_response
    def construct_response(self, message: str):
        """ Constructs response for dash by examining the input. The input is checked by several rules before relying on
        very general semantic maps."

        Args:
            message:    User input from the chatbot client.

        Returns:
            list:       List of responses, based on each sentence supplied from the client.

        """
        message = self.clean_up(message)
        u_wot_m8 = TextBlob(message)
        reply = []
        for sentence in u_wot_m8.sentences:
            unpacked_sentence_pos = self.unpack_pos(sentence)
            response = self.check_for_bot_reference(**unpacked_sentence_pos)
            if not response:
                response = self.check_for_greeting(sentence)
            if not response:
                response = self.deconstruct_message(sentence)
            if not response:
                if not unpacked_sentence_pos['pronoun']:
                    response = random.choice(self.NONE_RESPONSES)
                elif unpacked_sentence_pos['pronoun'] == 'I' and not unpacked_sentence_pos['verb']:
                    response = random.choice(self.RANDOM_STATEMENTS)
                else:
                    response = self.deconstructed_response(**unpacked_sentence_pos)
            if not response:
                response = self.unknown_utterance(True)
            reply.append(response)
        return reply

    def deconstructed_response(self, pronoun, noun, verb, adjective):
        """ Inspects the syntax and

        Args:
            pronoun:
            noun:
            verb:
            adjective:

        Returns:

        """
        response = []
        if pronoun:
            response.append(pronoun)
        if verb:
            response.append(self._response_pattern_verb(verb, pronoun))
        if noun and adjective:
            response.append(adjective[0])
        if len(response) <= 1:
            return None
        return [" ".join(response)]

    def _response_pattern_verb(self, verb, pronoun):
        """

        Args:
            verb:
            pronoun:

        Returns:

        """
        response = []
        verb_word = verb[0]
        verb_lemma = Word(verb_word)
        if verb_lemma.lemma in ('be', 'am', 'is'):
            if pronoun.lower() == 'you':
                response.append("are indeed")
            else:
                response.append(verb_word)
        if len(response) == 0:
            response = ''
        return response

    @staticmethod
    def starts_with_vowel(word):
        """

        Args:
            word:

        Returns:

        """
        return True if word[0] in 'aeiou' else False

    def match_tags(self, message: str):
        pass

    @strip_punctuation
    def check_for_greeting(self, sentence: str):
        """

        Args:
            sentence:

        Returns:

        """
        greeting = [random.choice(self.SALUTATION_RESPONSES) for word in sentence.split(' ') if
                    word.lower() in self.SALUTATION_KEYWORDS]
        if len(greeting) == 0:
            greeting = None
            return greeting
        return greeting[0]

    def unknown_utterance(self, unknown_utterance: bool = False):
        """

        Args:
            unknown_utterance:

        Returns:

        """
        que = None
        if unknown_utterance:
            que = [random.choice(self.UNKNOWN_UTTERANCE)]
        return que

    def unpack_sentence(self, message):
        """

        Args:
            message:

        Returns:

        """
        u_wot_m8 = TextBlob(message)
        print(u_wot_m8.tags)
        for i in u_wot_m8.tags:
            syn = Word(i[0])
            print('word: {}\n lemmatize: {}\n lemma: {}\n synsets: {}\n'.format(i[0], syn.lemmatize, syn.lemma,
                                                                                syn.synsets))

    def question_check(self, message):
        """

        Args:
            message:

        Returns:

        """
        u_wot_m8 = TextBlob(message)
        tag_check = self.deconstruct_message(sentence=u_wot_m8)
        return tag_check

    def deconstruct_message(self, sentence) -> list:
        """

        Args:
            sentence:

        Returns:

        """
        # deconstruct using tree and classifier then select path
        new_tags = tuple([(i[1], index) for index, i in enumerate(sentence.tags)])
        for i in self.SEMANTIC_DICTIONARY:
            if i[2] == new_tags:
                if i[0] == 'question':
                    return self.understand_question(i, sentence.tags, sentence)
                elif i[0] == 'direction':
                    return self.understand_direction(sentence.tags)
                elif i[0] == 'instruction':
                    pass
                elif i[0] == 'statement':
                    print(i, sentence.tags, sentence)
                else:
                    return None

    def understand_direction(self, tags):
        """

        Args:
            tags:

        Returns:

        """
        # understand the direction
        return self.direction_describe(tags)

    def understand_question(self, dependency, tags, sentence):
        """

        Args:
            dependency:
            tags:
            sentence:

        Returns:

        """
        # understand what the question is asking
        for tag in tags:
            # print(tag[1])
            if tag[1].lower() == 'jjs':
                return self.check_min_max_semantic(dependency, tag[0], sentence)

    def direction_describe(self, tags):
        """

        Args:
            tags:

        Returns:

        """
        for i in self._master_sku_list:
            if i[1] == tags[1][0]:
                return ['<a href=\"/sku_detail/{}\">Here you go!</a>'.format(i[0])]

    def check_min_max_semantic(self, dependency, jjs: str, sentence):
        """

        Args:
            dependency:
            jjs:
            sentence:

        Returns:

        """
        max = dependency[1][0]
        min = dependency[1][1]

        jj_word = Word(jjs)
        max_word = Word(max)
        min_word = Word(min)
        len_tags = len(sentence.tags)
        new_tags = sentence.tags
        end_word = new_tags[len_tags - 1]

        for word in jj_word.synsets:
            for set in min_word.synsets:
                if word == set:
                    for keyword in self.ANALYSIS_KEYWORDS:
                        if keyword == end_word[0].lower() and keyword == 'excess':
                            result = excess_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
                            return [
                                "SKU {} has the smallest excess value at ${}".format(str(result[1]), result[0][1])]
                        elif keyword == end_word[0].lower() and keyword == 'shortage':
                            result = shortage_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
                            return [
                                "SKU {} has the smallest shortage value at ${}".format(str(result[1]), result[0][1])]
                        elif keyword == end_word[0].lower() and keyword == 'revenue':
                            result = revenue_controller(database_connection_uri(retrieve='retrieve'), direction='smallest')
                            return [
                                "SKU {} has the lowest revenue value at ${}".format(str(result[1]), result[0][1])]

        # print(sentence.tags[len_tags - 1][1])
        if sentence.tags[len_tags - 1][1] == 'NN':
            for word in self.ANALYSIS_KEYWORDS:
                if word == end_word[0] and word == 'excess':
                    # max excess filters excess rank for lowest rank indicating biggest excess
                    result = excess_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
                    return ["SKU {} has the largest excess value at ${}".format(str(result[1]), result[0][1])]
                elif word == end_word[0].lower() and word == 'shortage':
                    result = shortage_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
                    return [
                        "SKU {} has the largest shortage value at ${}".format(str(result[1]), result[0][1])]
                elif word == end_word[0].lower() and word == 'revenue':
                    result = revenue_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
                    return [
                        "SKU {} has the highest revenue value at ${}".format(str(result[1]), result[0][1])]

                    # print(max_word.synsets, min_word.synsets, 'jj: {} '.format(jj_word.synsets))

    def _get_msk(self):
        ""

        msk = master_sku_list(database_connection_uri(retrieve='retrieve'))
        return msk

    def unpack_pos(self, msg):
        pronoun = None
        noun = None
        adjective = None
        verb = None
        pronoun = self.find_pronoun(self.filter_pos(sentence=msg, pos='PRP'))
        noun = self.filter_pos_type(sentence=msg, pos_type='noun')
        adjective = self.filter_pos_type(sentence=msg, pos_type='adjective')
        verb = self.filter_pos_type(sentence=msg, pos_type='verb')

        # print("pronoun: {}, noun: {}, adjective: {}, verb {},".format(pronoun, noun, adjective, verb))
        return {'pronoun': pronoun, 'noun': noun, 'adjective': adjective, 'verb': verb}

    @staticmethod
    def filter_pos(sentence, pos):
        """

        Args:
            sentence:
            pos:

        Returns:

        """
        tags = [i for i in sentence.tags]
        for tag in tags:
            if tag[1] == pos:
                return tag

    @staticmethod
    def filter_pos_type(sentence, pos_type):
        """

        Args:
            sentence:
            pos_type:

        Returns:

        """
        pos_regex = ''
        if pos_type == 'verb':
            pos_regex = re.compile('[V][B]\w?\w?')
        if pos_type == 'adjective':
            pos_regex = re.compile('[J][J]\w?\w?')
        if pos_type == 'noun':
            pos_regex = re.compile('[N][N]\w?\w?')

        tags = [i for i in sentence.tags]
        for tag in tags:
            if pos_regex.match(tag[1]):
                return tag

    @staticmethod
    def find_pronoun(pos: tuple) -> str:
        """

        Args:
            pos:

        Returns:

        """
        if pos is not None:
            pronoun = 'I' if pos[0] == 'PRP' and pos[1].lower() == 'you' else 'You'
            return pronoun
        else:
            return None

    def check_for_bot_reference(self, pronoun, noun, adjective, verb):
        """

        Args:
            pronoun:
            noun:
            adjective:
            verb:

        Returns:

        """
        if pronoun == 'You':
            if noun and adjective is False:
                response = random.choice(self.NOUN_SINGULAR).format(
                    noun[0])
            elif noun and verb:
                response = random.choice(self.NOUN_PLURAL).format(
                    noun[0].pluralize())
            else:
                response = random.choice(self.SELF_REFERENCING)

            return response


if __name__ == '__main__':
    dude = ChatBot()
    # print(dude.unpack_sentence("I like chocolate"))
    print(dude.chat("which sku generates the highest revenue"))
