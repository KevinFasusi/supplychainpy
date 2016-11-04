Feature: Chat with Bot
  Chat with Bot and receive a response.

  Scenario: Greet bot
    Given I have a greeting
    When I chat with bot
    Then It should respond
