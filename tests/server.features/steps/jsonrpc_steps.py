# -*- coding: UTF-8 -*-

# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
import tempfile
import json
from behave import given, when, then
from coala_langserver.jsonrpc import ReadWriter, TCPReadWriter, JSONRPC2Connection


@given('the string')
def step_impl(context):
    context.str = 'test-cases'


@when('I write it to ReadWriter')
def step_impl(context):
    context.f = tempfile.TemporaryFile(mode='w+')
    context.readWriter = ReadWriter(context.f, context.f)
    context.readWriter.write(context.str)


@then('it should read from ReadWriter')
def step_impl(context):
    context.f.seek(0)
    assert context.readWriter.read(len(context.str)) is not ''
    context.f.close()


@then('it should readline from ReadWriter')
def step_impl(context):
    context.f.seek(0)
    assert context.readWriter.readline() is not ''
    context.f.close()


@when('I write it to TCPReadWriter')
def step_impl(context):
    context.f = tempfile.TemporaryFile()
    context.readWriter = TCPReadWriter(context.f, context.f)
    context.readWriter.write(context.str)


@then('it should read from TCPReadWriter')
def step_impl(context):
    context.f.seek(0)
    assert context.readWriter.read(len(context.str)) is not ''
    context.f.close()


@then('it should readline from TCPReadWriter')
def step_impl(context):
    context.f.seek(0)
    assert context.readWriter.readline() is not ''
    context.f.close()


@given('the JSONRPC2Connection instance')
def step_impl(context):
    context.f = tempfile.TemporaryFile()
    context.jsonConn = JSONRPC2Connection(conn=TCPReadWriter(context.f, context.f))


@when('I write a request to the JSONRPC2Connection with id')
def step_impl(context):
    context.jsonConn.send_request('mockMethod', {
        'mock': 'mock'
    })


@then('it should return the request from JSONRPC2Connection with id')
def step_impl(context):
    context.f.seek(0)
    assert context.jsonConn.read_message() is not None
    context.f.close()


@when('I write a notification to the JSONRPC2Connection')
def step_impl(context):
    context.jsonConn.send_notification('mockMethod', {
        'mock': 'mock'
    })


@then('it should return the notification from JSONRPC2Connection')
def step_impl(context):
    context.f.seek(0)
    assert context.jsonConn.read_message() is not None
    context.f.close()


@when('I write a response to the JSONRPC2Connection')
def step_impl(context):
    # BUG: when id = 0
    context.ID = 1
    context.jsonConn.write_response(context.ID, {
        'mock': 'mock'
    })


@then('it should return the response from JSONRPC2Connection')
def step_impl(context):
    context.f.seek(0)
    assert context.jsonConn.read_message(context.ID) is not None
    context.f.close()
