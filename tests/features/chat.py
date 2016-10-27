from le ttuce import step, world
from supplychainpy.bot._dash_states import DashStates
from supplychainpy.bot.dash import ChatBot


@step("I chat with bot")
def step_impl(step):
    """
    Args:
        step (lettuce.core.Step):
    """
    dash = DashStates()
    expected = dash.salutations
    bot = ChatBot()
    reponse = bot.chat_machine(message='Hello')
    assert reponse in expected
