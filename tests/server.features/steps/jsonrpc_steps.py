# -*- coding: UTF-8 -*-

# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
import tempfile
import json
from behave import given, when, then
from pyls.jsonrpc import streams
from pyls.jsonrpc import endpoint
from pyls.jsonrpc import dispatchers


def issimilar(dicta, dictb):
    """
    Return bool indicating if dicta is deeply similar to dictb.
    """
    # slow but safe for deeper evaluation
    return json.dumps(dicta) == json.dumps(dictb)


@given('the message')
def step_impl(context):
    context.message = {
        'simple': 'test',
    }


@when('I write it to JsonRpcStreamWriter')
def step_impl(context):
    context.f = tempfile.TemporaryFile(mode='w+b')
    context.writer = streams.JsonRpcStreamWriter(context.f)
    context.writer.write(context.message)


@then('it should read from JsonRpcStreamReader')
def step_impl(context):
    context.f.seek(0)
    context._passed = False

    def consumer(message):
        assert issimilar(context.message, message)
        context._passed = True
        context.writer.close()

    reader = streams.JsonRpcStreamReader(context.f)
    reader.listen(consumer)
    reader.close()

    if not context._passed:
        assert False


@given('a notification type rpc request')
def step_impl(context):
    context.request = {
        'jsonrpc': '2.0',
        'method': 'math/add',
        'params': {
            'a': 1,
            'b': 2,
        },
    }


@when('I send rpc request using JsonRpcStreamWriter')
def step_impl(context):
    context.f = tempfile.TemporaryFile()
    context.writer = streams.JsonRpcStreamWriter(context.f)
    context.writer.write(context.request)


@then('it should invoke the notification consumer with args')
def step_impl(context):
    context.f.seek(0)
    context._passed = False

    class Example(dispatchers.MethodDispatcher):

        def m_math__add(self, a, b):
            context.writer.close()
            context._passed = True

    epoint = endpoint.Endpoint(Example(), None)
    reader = streams.JsonRpcStreamReader(context.f)
    reader.listen(epoint.consume)
    reader.close()

    if not context._passed:
        assert False


@given('a request type rpc request')
def step_impl(context):
    context.request = {
        'jsonrpc': '2.0',
        'id': 2148,
        'method': 'math/add',
        'params': {
            'a': 1,
            'b': 2,
        },
    }


@then('it should invoke consumer and return response')
def step_impl(context):
    context.f.seek(0)
    context._passed = False

    class Example(dispatchers.MethodDispatcher):

        def m_math__add(self, a, b):
            return a + b

    def consumer(message):
        assert message['result'] == sum(context.request['params'].values())
        context.writer.close()
        context._passed = True

    epoint = endpoint.Endpoint(Example(), consumer)
    reader = streams.JsonRpcStreamReader(context.f)
    reader.listen(epoint.consume)
    reader.close()

    if not context._passed:
        assert False
