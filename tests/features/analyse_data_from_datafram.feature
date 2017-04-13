# Created by Fasusi at 12/04/2017
Feature: Analyse Pandas DataFrame
  Analyse raw data from a Pandas DataFrame


  Scenario: Analyse DataFrame
    Given I extract data from a CSV
    When I analyse raw data in a Pandas DataFrame
    Then It should return a DataFrame with Descriptive Statistics
