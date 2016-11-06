Feature: Chat with Bot
  Chat with Bot and receive a response.

  Scenario: Greet bot
    Given I initiate chat with bot with a greeting
    When I say hello to the bot
    Then It should respond
