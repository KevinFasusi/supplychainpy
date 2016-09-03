from textblob import TextBlob


class ChatBot():
    def __init__(self):
        pass

    def receive_message(self, message:str)->list:
        response =['Hi i am Dash!']
        return response

    @staticmethod
    def deconstruct_message(message:str):
        u_wot_m8 = TextBlob(message)