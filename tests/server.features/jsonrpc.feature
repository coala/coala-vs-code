Feature: jsonrpc module
  jsonrpc is a module of language-server.

  Scenario: Test JsonRpcStreamWriter and JsonRpcStreamReader
    Given the message
    When I write it to JsonRpcStreamWriter
    Then it should read from JsonRpcStreamReader

  Scenario: Test notification and disptacher
    Given a notification type rpc request
    When I send rpc request using JsonRpcStreamWriter
    Then it should invoke the notification consumer with args

  Scenario: Test rpc request and response
    Given a request type rpc request
    When I send rpc request using JsonRpcStreamWriter
    Then it should invoke consumer and return response

  # TODO: block until we have generantee the unique request.
#  Scenario: Test send_request
#    Given the JSONRPC2Connection instance
#    When I write a request to the JSONRPC2Connection with id
#    Then it should return the request from JSONRPC2Connection with id
