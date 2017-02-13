# -*- coding: UTF-8 -*-

# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
import tempfile
from behave import given, when, then
from coala_langserver.jsonrpc import TCPReadWriter
from coala_langserver.langserver import LangServer


@given('the LangServer instance')
def step_impl(context):
    context.f = tempfile.TemporaryFile()
    context.langServer = LangServer(conn=TCPReadWriter(context.f, context.f))


@when('I send a initialize request to the server')
def step_impl(context):
    request = {
        'method': 'initialize',
        'params': {
            'rootPath': '/Users/mock-user/mock-dir',
            'capabilities': {},
        },
        'id': 1,
        'jsonrpc': '2.0'
    }
    context.langServer.handle(1, request)


@then('it should return the response with textDocumentSync')
def step_impl(context):
    context.f.seek(0)
    response = context.langServer.read_message(1)
    assert response is not None
    assert response['result']['capabilities']['textDocumentSync'] is 1
    context.f.close()


@when('I send a did_save request about a non-existed file to the server')
def step_impl(context):
    request = {
        'method': 'textDocument/didSave',
        'params': {
            'textDocument': {
                'uri': 'file:///Users/mock-user/non-exist.py'
            }
        },
        'jsonrpc': '2.0'
    }
    context.langServer.handle(None, request)


@then('it should send a publishDiagnostics request')
def step_impl(context):
    context.f.seek(0)
    response = context.langServer.read_message()
    assert response is not None
    assert response['method'] == 'textDocument/publishDiagnostics'
    assert len(response['params']['diagnostics']) is 0
    context.f.close()
