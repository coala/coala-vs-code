Feature: coalashim module
  coalashim is a module of language-server, it interacts with coala core.

  Scenario: Test run_coala_with_specific_file
    Given the current directory and path of qualified.py
    When I pass the qualified.py to run_coala_with_specific_file
    Then it should return output in json format
    And with no error in the output

  Scenario: Test run_coala_with_specific_file
    Given the current directory and path of unqualified.py
    When I pass the unqualified.py to run_coala_with_specific_file
    Then it should return output in json format
    And with autopep8 errors in the output
