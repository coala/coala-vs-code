Feature: log module
  log is a module of language-server.

  Scenario: Test log
    Given There is a string
    When I pass the string to log
    Then it should return normally
