Feature: diagnostic module
  diagnostic is a module of language-server.

  Scenario: Test output_to_diagnostics
    Given the output with errors by coala
    When I pass the parameters to output_to_diagnostics
    Then it should return output in vscode format
