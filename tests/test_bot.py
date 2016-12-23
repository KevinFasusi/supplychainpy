from unittest import TestCase

from supplychainpy.bot.dash import ChatBot


class TestBot(TestCase):

    def setUp(self):
        self.__dude = ChatBot()
        self.__SALUTATION_RESPONSES = ["hi", "hello", "how's tricks?"]


    def test_chatbot(self):
        greeting = self.__dude.chat_machine("hello")[0][0]
        self.assertIn(greeting, self.__SALUTATION_RESPONSES)
        self.assertIn('KR202-244', *self.__dude.chat_machine("Which SKU has the highest reorder level?")[0])
        self.assertEqual('<a href="/sku_detail/36">Here you go!</a>', *self.__dude.chat_machine("show KR202-244")[0])
        self.assertIn('SKU KR202-244', *self.__dude.chat_machine("what is the biggest shortage?")[0])
        self.assertIn('KR202-223',*self.__dude.chat_machine("what is the biggest excess?")[0])
