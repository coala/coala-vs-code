Feature: langserver module
  langserver is the main program of language-server.

  Scenario: Test serve_initialize with rootPath
    Given the LangServer instance
    When I send a initialize request with rootPath to the server
    Then it should return the response with textDocumentSync

  Scenario: Test serve_initialize with rootUri
    Given the LangServer instance
    When I send a initialize request with rootUri to the server
    Then it should return the response with textDocumentSync

  Scenario: Test send_diagnostics
    Given the LangServer instance
    When I invoke send_diagnostics message
    Then I should receive a publishDiagnostics type response

  Scenario: Test negative m_text_document__did_save
    Given the LangServer instance
    When I send a did_save request about a non-existed file to the server
    Then I should receive a publishDiagnostics type response

  Scenario: Test positive m_text_document__did_save
    Given the LangServer instance
    When I send a did_save request about a existing file to the server
    Then I should receive a publishDiagnostics type response

  Scenario: Test when coafile is missing
    Given the LangServer instance
    When I send a did_save request on a file with no coafile to server
    Then I should receive a publishDiagnostics type response

  Scenario: Test didChange
    Given the LangServer instance
    When I send a did_change request about a file to the server
    Then it should ignore the request

  Scenario: Test langserver shutdown
    Given the LangServer instance
    When I send a shutdown request to the server
    Then it should shutdown

  Scenario: Test language server in stdio mode
    Given I send a initialize request via stdio stream
    When the server is started in stdio mode
    Then it should return the response with textDocumentSync via stdio

  Scenario: Test language server in tcp mode
    Given the server started in TCP mode
    When I send a initialize request via TCP stream
    Then it should return the response with textDocumentSync via TCP
