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

import random
import uuid

from supplychainpy._helpers._codes import Currency
from supplychainpy._helpers._db_connection import database_connection_uri
from supplychainpy._helpers._decorators import strip_punctuation
from supplychainpy.bi._recommendations import ResponseSingleton
from supplychainpy.bot._controller import master_sku_list, excess_controller, shortage_controller, revenue_controller, \
    inventory_turns_controller, average_orders_controller, currency_symbol_controller, classification_controller, \
    safety_stock_controller, reorder_level_controller
from supplychainpy.bot._helpers import get_master_sku_list, _unpack_pos, _find_pronoun, filter_pos, filter_pos_type

from textblob import TextBlob
from textblob import Word


class DashStates:
    _MIN = ('least', 'lowest', 'smallest', 'fewest')
    _MAX = ('biggest', 'most', 'highest', 'largest')
    _END_STATE = 'response'
    _EMPTY = 'EMPTY'
    _TRANSITION_STATES = {
        'PRONOUN_STATE': 'pronoun',
        'GREETING_STATE': 'greeting',
        'DECONSTRUCTION_STATE': 'deconstruction',
        'RANDOM_STATE': 'random_utterance',
        'RESPONSE_STATE': 'response'
    }
    _NOUN_SINGULAR = [
        "{}!",
        "Again {}.It's probably time for a coffee!",
        "{} may be hard, don't let the details get you down.",
        "{} we will be running the show."
    ]

    KEYWORDS = ('average', 'retail', 'economic')

    ANALYSIS_KEYWORDS = ("safety stock", "reorder level","excess", "shortage", "revenue", "inventory turns", "average order", "classification")

    SALUTATION_KEYWORDS = ("hi", "hello", "wassup", "sup", "what's up", "ello", "how's tricks?")

    SALUTATION_RESPONSES = ["hi", "hello", "how's tricks?"]

    UNKNOWN_UTTERANCE = ["Not sure what you are saying!", "I don't understand!"]

    _SEMANTIC_DICTIONARY = [
        ('question', ('biggest', 'smallest'), (('WP', 0), ('VBZ', 1), ('DT', 2), ('JJS', 3), ('NN', 4))),
        ('question', ('biggest', 'smallest'), (('WDT', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5))),
        ('question', ('biggest', 'smallest'), (('WDT', 0), ('NNP', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NNS', 5))),
        ('question', ('shortage', 'revenue', 'excess', 'classification'), (('WP', 0), ('VBZ', 1), ('DT', 2), ('NN', 3), ('IN', 4), ('NNP', 5))),
        ('question', ('equal', 'is'), (('WP', 0), ('VBZ', 1), ('DT', 2), ('NN', 3), ('IN', 4), ('NNP', 5))),
        ('question', ('biggest', 'smallest'), (('WDT', 0), ('NNP', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5))),
        ('question', ('most', 'fewest'), (('NNP', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5), ('NNS', 6))),
        ('question', ('biggest', 'smallest'), (('NNP', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5), ('NN', 6))),
        ('question', ('biggest', 'smallest'), (('NNP', 0), ('NNP', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5), ('NN', 6))),

        ('question', ('biggest', 'smallest'), (('WDT', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5), ('NN', 6))),
        ('question', ('biggest', 'smallest'), (('NNP', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('JJ', 5), ('NNS', 6))),
        ('question', ('biggest', 'smallest'), (('NNP', 0), ('NNP', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('JJ', 5), ('NN', 6))),
        ('question', ('biggest', 'smallest'), (('NNP', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('JJ', 5), ('NN', 6))),
        ('question', ('biggest', 'smallest'), (('WDT', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('JJ', 5), ('NN', 6))),
        ('question', ('biggest', 'smallest'), (('NNP', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('JJ', 5), ('NNS', 6))),
        ('question', ('most', 'fewest'), (('NNP', 0), ('NNP', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5), ('NNS', 6))),
        ('question', ('most', 'fewest'), (('NNP', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('JJS', 4), ('NN', 5), ('NNS', 6))),
        ('question', ('most', 'fewest'), (('NNP', 0), ('NNP', 1), ('VBZ', 2), ('DT', 3), ('RBS', 4), ('JJ', 5), ('NNS', 6))),
        ('question', ('most', 'fewest'), (('NNP', 0), ('NN', 1), ('VBZ', 2), ('DT', 3), ('RBS', 4), ('JJ', 5), ('NNS', 6))),
        ('question', ('average'), (('WP', 0), ('VBZ', 1), ('DT', 2), ('JJ', 3), ('NN', 4), ('IN', 5), ('NNP', 6))),
        ('direction', ('explain', 'describe'), (('NNP', 0), ('NNP', 1), ('NNP', 2))),
        ('direction', ('explain', 'describe'), (('NNP', 0), ('NN', 1), ('NNP', 2))),
        ('direction', ('explain', 'describe'), (('NNP', 0), ('NNP', 1), ('NNP', 2))),
        ('direction', ('explain', 'describe'), (('NNP', 0), ('NN', 1), ('NN', 2))),
        ('direction', ('explain', 'describe'), (('NNP', 0), ('NNP', 1), ('NNP', 2))),
        ('direction', ('explain', 'describe'), (('NN', 0), ('NN', 1), ('NNP', 2))),
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

    SELF_REFERENCING = [
        "I'm busy keeping the data clean.",
        "I want to help you work smart!",
        "I see widgets in my sleep.",
        "Ready to optimise, optimise, optimise.",
        "I think there is work to be done."
    ]

    NONE_RESPONSES = [
        ["It's probably time for a coffee!"],
        ["It's probably time for some tea!"],
        ["Don't let the details get you down"],
        ["Keep fighting the good fight"],

    ]

    RANDOM_STATEMENTS = [
        "I see SKUs in my sleep",
    ]
    _communication_id = ''
    _currency_symbol = ''
    _currency_code = ''

    def __init__(self):
        self._master_sku_list = get_master_sku_list()
        self.compiled_response = ResponseSingleton()

    @property
    def salutations(self):
        return self.SALUTATION_RESPONSES

    @property
    def currency_symbol(self):
        return self._currency_symbol

    @property
    def currency(self):
        return currency_symbol_controller(database_connection_uri(retrieve='retrieve'))

    @property
    def communication_id(self):
        return self._communication_id

    @communication_id.setter
    def communication_id(self, comms_id):
        self._communication_id = comms_id

    def load_currency_symbol(self):
        self._currency_code = self.currency
        cur = Currency(self._currency_code)
        self._currency_symbol = cur.retrieve_symbol()

    @strip_punctuation
    def _check_for_greeting(self, sentence: str):
        """ Checks whether message includes greeting and responds in kind.

        Args:
            sentence:   Sentence from message entered by user.

        Returns:

        """
        greeting = [random.choice(self.SALUTATION_RESPONSES) for word in sentence.split(' ') if
                    word.lower() in self.SALUTATION_KEYWORDS]
        if len(greeting) == 0:
            greeting = None
            return greeting
        return greeting

    def _check_for_bot_reference(self, pronoun, noun, adjective, verb):
        """

        Args:
            pronoun:
            noun:
            adjective:
            verb:

        Returns:

        """
        if pronoun:
            if pronoun[0] == 'You':
                if noun and adjective is False:
                    response = random.choice(self._NOUN_SINGULAR).format()
                elif noun and verb:
                    response = random.choice(self.NOUN_PLURAL).format(
                        noun[0].pluralize())
                else:
                    response = random.choice(self.SELF_REFERENCING)

                return response
        else:
            return None

    def direction_describe(self, tags):
        """

        Args:
            tags:

        Returns:

        """
        for i in self._master_sku_list:
            if i[1] == tags[1][0]:
                return ['<a href=\"/sku_detail/{}\">Here you go!</a>'.format(i[0])]

    def _understand_direction(self, tags):
        """

        Args:
            tags:

        Returns:

        """
        # understand the direction
        return self.direction_describe(tags)

    def _understand_question(self, dependency, tags, sentence):
        """

        Args:
            dependency:
            tags:
            sentence:

        Returns:

        """
        # understand what the question is asking
        for tag in tags:
            if tag[1].lower() == 'jjs' or tag[1].lower() == 'rbs':
                return self.check_min_max_semantic(dependency, tag[0], sentence)
        for tag in tags:
            if tag[1].lower() == 'nn':
                return self.check_keyword_sku_combo(dependency, tag[0], sentence)

    def check_keyword_sku_combo(self, dependency, nn: str, sentence):

        len_tags = len(sentence.tags)
        new_tags = sentence.tags
        antepenultimate_word = new_tags[len_tags - 3]
        end_word = new_tags[len_tags - 1]
        skus = [sku[1] for sku in  self._master_sku_list]
        if sentence.tags[len_tags - 1][1] in ('NNP') and end_word[0] in skus:
            for word in self.ANALYSIS_KEYWORDS:
                if word == 'classification':
                    result = classification_controller(database_connection_uri(retrieve='retrieve'),sku_id=end_word[0])
                    response = [
                        'SKU {} has the classification {}'.format(str(end_word[0]), result)]
                    return response

    def check_min_max_semantic(self, dependency, jjs: str, sentence):
        """

        Args:
            dependency:
            jjs:
            sentence:

        Returns:

        """
        # probably beter to change this to a tuple of keywords, removes the call to wordnet etc
        max = dependency[1][0]
        min_w = dependency[1][1]
        jj_word = Word(jjs)
        max_word = Word(max)
        min_word = Word(min_w)
        len_tags = len(sentence.tags)
        new_tags = sentence.tags
        penultimate_word = new_tags[len_tags - 2]
        end_word = new_tags[len_tags - 1]

        for word in jj_word.synsets:
            for set in min_word.synsets:
                if word == set:
                    for keyword in self.ANALYSIS_KEYWORDS:
                        if keyword == end_word[0].lower() and keyword == 'excess':
                            result = excess_controller(database_connection_uri(retrieve='retrieve'),
                                                       direction='smallest')
                            response = [
                                'SKU {} has the smallest excess value at {}{:,.2f}'.format(str(result[1]),
                                                                                           self.currency_symbol,
                                                                                           result[0][1])]
                            return response

                        elif keyword == end_word[0].lower() and keyword in ('shortage', 'shortages'):
                            result = shortage_controller(database_connection_uri(retrieve='retrieve'),
                                                         direction='smallest')
                            response = [
                                'SKU {} has the smallest shortage value at {}{:,.2f}'.format(str(result[1]),
                                                                                             self.currency_symbol,
                                                                                             result[0][1])]
                            return response

                        elif keyword == end_word[0].lower() and keyword == 'revenue':
                            result = revenue_controller(database_connection_uri(retrieve='retrieve'),
                                                        direction='smallest')
                            response = [
                                'SKU {} has the lowest revenue value at {}{:,.2f}'.format(str(result[1]),
                                                                                          self.currency_symbol,
                                                                                          result[0][1])]
                            return response
                        elif keyword == '{} {}'.format(penultimate_word[0].lower(),
                                                       end_word[0].lower()) and keyword == 'inventory turns':
                            result = inventory_turns_controller(database_connection_uri(retrieve='retrieve'),
                                                                direction='smallest')
                            response = [
                                'SKU {} has the fewest inventory turns at {}'.format(str(result[1]), result[0][1])]
                            return response
                        elif keyword == '{} {}'.format(penultimate_word[0].lower(),
                                                       end_word[0].lower()) and keyword in ('average order', 'average orders'):
                            result = average_orders_controller(database_connection_uri(retrieve='retrieve'),
                                                               direction='smallest')
                            response = [
                                'SKU {} has the lowest average order at {} units.'.format(str(result[1]),
                                                                                          result[0][1])]
                            return response

                        elif keyword == '{} {}'.format(penultimate_word[0].lower(),
                                                    end_word[0].lower()) and keyword == 'safety stock':
                            result = safety_stock_controller(database_connection_uri(retrieve='retrieve'),
                                                               direction='smallest')
                            response = ['SKU {} has the lowest safety stock at {} units.'.format(str(result[1]),
                                                                                                   result[0])]
                            return response

                        elif keyword == '{} {}'.format(penultimate_word[0].lower(),
                                                    end_word[0].lower()) and keyword == 'reorder level':
                            result = reorder_level_controller(database_connection_uri(retrieve='retrieve'),
                                                               direction='smallest')
                            response = ['SKU {} has the lowest reorder level at {} units.'.format(str(result[1]),
                                                                                                   result[0])]
                            return response

        # print(sentence.tags[len_tags - 1][1])
        if sentence.tags[len_tags - 1][1] in ('NN') or max.lower() in self._MAX:
            for word in self.ANALYSIS_KEYWORDS:
                if word == end_word[0] and word == 'excess':
                    # max excess filters excess rank for lowest rank indicating biggest excess
                    result = excess_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
                    return [
                        'SKU {} has the largest excess value at {}{:,.2f}'.format(str(result[1]), self.currency_symbol,
                                                                                  result[0][1])]
                elif word == end_word[0].lower() and word == 'shortage':
                    result = shortage_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
                    return ['SKU {} has the largest shortage value at {}{:,.2f}'.format(str(result[1]),
                                                                                        self.currency_symbol,
                                                                                        result[0][1])]
                elif word == end_word[0].lower() and word == 'revenue':
                    result = revenue_controller(database_connection_uri(retrieve='retrieve'), direction='biggest')
                    return [
                        'SKU {} has the highest revenue value at {}{:,.2f}'.format(str(result[1]), self.currency_symbol,
                                                                                   result[0][1])]
                elif word == '{} {}'.format(penultimate_word[0].lower(),
                                            end_word[0].lower()) and word == 'inventory turns':
                    result = inventory_turns_controller(database_connection_uri(retrieve='retrieve'),
                                                        direction='biggest')
                    response = ['SKU {} has the highest inventory turn rate at {}'.format(str(result[1]), result[0][1])]
                    return response
                elif word == '{} {}'.format(penultimate_word[0].lower(),
                                            end_word[0].lower()) and word in ('average order', 'average orders'):
                    result = average_orders_controller(database_connection_uri(retrieve='retrieve'),
                                                       direction='biggest')
                    response = ['SKU {} has the largest average order at {} units.'.format(str(result[1]), result[0][1])]
                    return response
                elif word == '{} {}'.format(penultimate_word[0].lower(),
                                                end_word[0].lower()) and word =='safety stock':
                    result = safety_stock_controller(database_connection_uri(retrieve='retrieve'),
                                                       direction='biggest')
                    response = [
                        'SKU {} has the largest safety stock at {} units.'.format(str(result[1]), result[0])]
                    return response
                elif word == '{} {}'.format(penultimate_word[0].lower(),
                                                end_word[0].lower()) and word == 'reorder level':
                    result = reorder_level_controller(database_connection_uri(retrieve='retrieve'),
                                                     direction='biggest')
                    response = [
                        'SKU {} has the largest reorder level at {} units.'.format(str(result[1]), result[0])]
                    return response


                    # print(max_word.synsets, min_word.synsets, 'jj: {} '.format(jj_word.synsets))

    def _deconstruct_message(self, sentence) -> list:
        """

        Args:
            sentence:

        Returns:

        """
        # deconstruct using tree and classifier then select path
        new_tags = tuple([(i[1], index) for index, i in enumerate(sentence.tags)])
        for i in self._SEMANTIC_DICTIONARY:
            if i[2] == new_tags:
                if i[0] == 'question':
                    return self._understand_question(i, sentence.tags, sentence)
                elif i[0] == 'direction':
                    return self._understand_direction(sentence.tags)
                elif i[0] == 'instruction':
                    pass
                elif i[0] == 'statement':
                    pass
                    # print(i, sentence.tags, sentence)
                else:
                    return None

    def _append_response(self, message):
        msg_flag = ''
        msg = []
        if self.communication_id:
            msg_flag = self.compiled_response.shared_response.get(str(self.communication_id), self._EMPTY)
        else:
            msg_flag = self._EMPTY
            self.communication_id = uuid.uuid1()
        if self._EMPTY != msg_flag:
            msg.append(msg_flag)
            for m in message:
                msg.append(m)

            self.compiled_response.shared_response.update(**{'{}'.format(self.communication_id): msg})
        else:
            self.compiled_response.shared_response.update(**{'{}'.format(self.communication_id): message})

    def _check_deconstruction_required(self, message: dict) -> bool:
        sentence_count = len([i for i in message.keys()])
        # precompiled_response = [response for response in self.compiled_response.shared_response.values()]
        if sentence_count != 0:
            return True
        else:
            return False

    def unpack_pos(self, msg):
        pronoun = None
        noun = None
        adjective = None
        verb = None
        pronoun = _find_pronoun(filter_pos(sentence=msg, pos='PRP'))
        noun = filter_pos_type(sentence=msg, pos_type='noun')
        adjective = filter_pos_type(sentence=msg, pos_type='adjective')
        verb = filter_pos_type(sentence=msg, pos_type='verb')
        # print("pronoun: {}, noun: {}, adjective: {}, verb {},".format(pronoun, noun, adjective, verb))
        return {'pronoun': pronoun, 'noun': noun, 'adjective': adjective, 'verb': verb}

    def initialise_chat(self, message):
        u_wot_m8 = TextBlob(message)
        self.load_currency_symbol()
        unpacked_sentences = {}
        new_state = ''
        for sentence in u_wot_m8.sentences:
            unpacked_sentence_pos = _unpack_pos(message=sentence)
            unpacked_sentences.update({sentence: unpacked_sentence_pos})
            new_state = self._TRANSITION_STATES.get('PRONOUN_STATE', self._END_STATE)
        return new_state, unpacked_sentences

    def pronoun(self, message: dict):
        msg = {}
        for x in message.values():
            msg.update(**x)
        response = self._check_for_bot_reference(**msg)
        if response:
            new_state = self._TRANSITION_STATES.get('DECONSTRUCTION_STATE', self._END_STATE)
            self._append_response(message=response)
        else:
            new_state = self._TRANSITION_STATES.get('GREETING_STATE', self._END_STATE)
        return new_state, message

    def greeting(self, message: dict):
        msg = []
        for x in message.keys():
            msg.append(x)
        response = ''
        del_key = ''
        for sentence in msg:
            response = self._check_for_greeting(*msg)
            if response:
                del_key = sentence
                break
        new_state = self._TRANSITION_STATES.get('DECONSTRUCTION_STATE', self._END_STATE)
        if response:
            self._append_response(message=response)
            del message[del_key]
        return new_state, message

    def deconstruction(self, message: dict):
        msg = []
        response = []
        new_state = new_state = self._TRANSITION_STATES.get('RANDOM_STATE', self._END_STATE)
        for x in message.keys():
            msg.append(x)
        if self._check_deconstruction_required(message=message):
            reply = []
            for sentence in message.keys():
                response = self._deconstruct_message(sentence)
                if response:
                    reply.append(response)
                    new_state = self._TRANSITION_STATES.get('RESPONSE_STATE', self._END_STATE)
            if reply:
                self._append_response(message=reply)
            else:
                new_state = new_state = self._TRANSITION_STATES.get('RANDOM_STATE', self._END_STATE)
        return new_state, message

    def random_utterance(self, message: dict):
        response = ''
        for sentence in message.keys():
            print(sentence)
            unpacked_sentence_pos = self.unpack_pos(sentence)
            if not unpacked_sentence_pos['pronoun']:
                response = random.choice(self.NONE_RESPONSES)
            elif unpacked_sentence_pos['pronoun'] == 'I' and not unpacked_sentence_pos['verb'][0]:
                response = random.choice(self.RANDOM_STATEMENTS)
        self._append_response(message=response)
        new_state = self._TRANSITION_STATES.get('RESPONSE_STATE', self._END_STATE)
        return new_state, message
