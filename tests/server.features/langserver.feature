Feature: langserver module
  langserver is the main program of language-server.

  Scenario: Test serve_initialize
    Given the LangServer instance
    When I send a initialize request to the server
    Then it should return the response with textDocumentSync

  # TODO: Add positive test case.
  Scenario: Test serve_did_save
    Given the LangServer instance
    When I send a did_save request about a non-existed file to the server
    Then it should send a publishDiagnostics request
