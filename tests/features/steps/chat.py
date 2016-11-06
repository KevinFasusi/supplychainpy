from behave import given, when, then
from supplychainpy.bot._dash_states import DashStates
from supplychainpy.bot.dash import ChatBot


@given("I initiate chat with bot with a greeting")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    bot = ChatBot()
    assert isinstance(bot, ChatBot)


@when("I say hello to the bot")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """


    bot = ChatBot()
    context.response = bot.chat_machine(message='Hello')
    assert context.response


@then("It should respond")
def step_impl(context):
    """
    Args:
        context (behave.runner.Context):
    """
    dash = DashStates()
    assert context.response[0][0] in dash.salutations


