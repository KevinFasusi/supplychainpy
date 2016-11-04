from behave import *
from supplychainpy.bot._dash_states import DashStates
from supplychainpy.bot.dash import ChatBot

@when("I chat with bot")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    dash = DashStates()
    expected = dash.salutations
    bot = ChatBot()
    reponse = bot.chat_machine(message='Hello')
    pass

@given("I have a greeting")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    pass


@then("It should respond")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    pass


