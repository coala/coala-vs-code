Feature: jsonrpc module
  jsonrpc is a module of language-server.

  Scenario: Test ReadWriter
    Given the string
    When I write it to ReadWriter
    Then it should read from ReadWriter

  Scenario: Test ReadWriter
    Given the string
    When I write it to ReadWriter
    Then it should readline from ReadWriter

  Scenario: Test TCPReadWriter
    Given the string
    When I write it to TCPReadWriter
    Then it should read from TCPReadWriter

  Scenario: Test TCPReadWriter
    Given the string
    When I write it to TCPReadWriter
    Then it should readline from TCPReadWriter

  Scenario: Test send_notification and read_message
    Given the JSONRPC2Connection instance
    When I write a notification to the JSONRPC2Connection
    Then it should return the notification from JSONRPC2Connection

  Scenario: Test write_response
    Given the JSONRPC2Connection instance
    When I write a response to the JSONRPC2Connection
    Then it should return the response from JSONRPC2Connection

  # TODO: block until we have generantee the unique request.
#  Scenario: Test send_request
#    Given the JSONRPC2Connection instance
#    When I write a request to the JSONRPC2Connection with id
#    Then it should return the request from JSONRPC2Connection with id
