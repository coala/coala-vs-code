Feature: uri module
  uri is a module of language-server.

  Scenario: Test path_from_uri
    Given There is a string with "file://"
    When I pass the string with the prefix to path_from_uri
    Then it should return a string without "file://"

  Scenario: Test path_from_uri
    Given There is a string without "file://"
    When I pass the string without the prefix to path_from_uri
    Then it should return a string without "file://"

  Scenario: Test dir_from_uri
    Given There is a string without "file://"
    When I pass the string to dir_from_uri
    Then it should return the directory of the path
