import random
import re

from supplychainpy._helpers._db_connection import database_connection_uri
from supplychainpy._helpers._decorators import strip_punctuation
from supplychainpy.bot._controller import master_sku_list
from textblob import TextBlob
from textblob import Word


def get_master_sku_list():
    msk = master_sku_list(database_connection_uri(retrieve='retrieve'))
    return msk





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


def _unpack_pos( message):
    pronoun = _find_pronoun(filter_pos(sentence=message, pos='PRP'))
    noun = filter_pos_type(sentence=message, pos_type='noun')
    adjective = filter_pos_type(sentence=message, pos_type='adjective')
    verb = filter_pos_type(sentence=message, pos_type='verb')

    # print("pronoun: {}, noun: {}, adjective: {}, verb {},".format(pronoun, noun, adjective, verb))
    return {'pronoun': pronoun, 'noun': noun, 'adjective': adjective, 'verb': verb}


def _find_pronoun(pos: tuple) -> str:
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


def unpack_sentence(message):
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


