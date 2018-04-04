# -*- coding: UTF-8 -*-

# @mark.steps
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
import io
import os
import sys
import time
import socket
import tempfile
from threading import Thread

from behave import given, when, then
from unittest import mock

from pyls.jsonrpc import streams
from coala_langserver.langserver import LangServer, start_io_lang_server, main


@given('the LangServer instance')
def step_impl(context):
    context.f = tempfile.TemporaryFile()
    context.langServer = LangServer(context.f, context.f)


@when('I send a initialize request with rootPath to the server')
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
    context.langServer._endpoint.consume(request)


@when('I send a initialize request with rootUri to the server')
def step_impl(context):
    request = {
        'method': 'initialize',
        'params': {
            'rootUri': '/Users/mock-user/mock-dir',
            'capabilities': {},
        },
        'id': 1,
        'jsonrpc': '2.0',
    }
    context.langServer._endpoint.consume(request)


@then('it should return the response with textDocumentSync')
def step_impl(context):
    context.f.seek(0)
    context._passed = False

    def consumer(response):
        assert response is not None
        assert response['result']['capabilities']['textDocumentSync'] == 1
        context.f.close()
        context._passed = True

    reader = streams.JsonRpcStreamReader(context.f)
    reader.listen(consumer)
    reader.close()

    if not context._passed:
        assert False


@when('I invoke send_diagnostics message')
def step_impl(context):
    context.langServer.send_diagnostics('/sample', [])
    context._diagCount = 0


@when('I send a did_save request about a non-existed file to the server')
def step_impl(context):
    request = {
        'method': 'textDocument/didSave',
        'params': {
            'textDocument': {
                'uri': 'file:///Users/mock-user/non-exist.py'
            }
        },
        'jsonrpc': '2.0',
    }
    context.langServer._endpoint.consume(request)
    context._diagCount = 0


@when('I send a did_save request about a existing file to the server')
def step_impl(context):
    thisfile = os.path.realpath(__file__)
    thisdir = os.path.dirname(thisfile)
    parturi = os.path.join(thisdir, '../../resources', 'unqualified.py')
    absparturi = os.path.abspath(parturi)

    request = {
        'method': 'textDocument/didSave',
        'params': {
            'textDocument': {
                'uri': 'file://{}'.format(absparturi),
            },
        },
        'jsonrpc': '2.0',
    }
    context.langServer._endpoint.consume(request)
    context._diagCount = 4


@when('I send a did_save request on a file with no coafile to server')
def step_impl(context):
    somefile = tempfile.NamedTemporaryFile(delete=False)
    somefilename = somefile.name
    somefile.close()

    request = {
        'method': 'textDocument/didSave',
        'params': {
            'textDocument': {
                'uri': 'file://{}'.format(somefilename),
            },
        },
        'jsonrpc': '2.0'
    }
    context.langServer._endpoint.consume(request)
    context._diagCount = 0


@then('it should send a publishDiagnostics request')
def step_impl(context):
    context.f.seek(0)
    context._passed = False

    def consumer(response):
        assert response is not None
        assert response['method'] == 'textDocument/publishDiagnostics'
        assert len(response['params']['diagnostics']) is context._diagCount

        context.f.close()
        context._passed = True

    reader = streams.JsonRpcStreamReader(context.f)
    reader.listen(consumer)
    reader.close()

    if not context._passed:
        assert False


@when('I send a did_change request about a file to the server')
def step_impl(context):
    thisfile = os.path.realpath(__file__)
    thisdir = os.path.dirname(thisfile)
    parturi = os.path.join(thisdir, '../../resources', 'unqualified.py')

    request = {
        'method': 'textDocument/didChange',
        'params': {
            'textDocument': {
                'uri': 'file://{}'.format(parturi),
            },
            'contentChanges': [
                {
                    'text': 'def test():\n  a = 1\n',
                },
            ],
        },
        'jsonrpc': '2.0',
    }
    context.langServer._endpoint.consume(request)


@then('it should ignore the request')
def step_impl(context):
    length = context.f.seek(0, os.SEEK_END)
    assert length == 0
    context.f.close()


@when('I send a shutdown request to the server')
def step_impl(context):
    request = {
        'method': 'shutdown',
        'params': None,
        'id': 1,
        'jsonrpc': '2.0',
    }
    context.langServer._endpoint.consume(request)


@then('it should shutdown')
def step_impl(context):
    context.f.seek(0)
    context._passed = False

    def consumer(response):
        assert response is not None
        assert response['result'] is None

        context.f.close()
        context._passed = True

    reader = streams.JsonRpcStreamReader(context.f)
    reader.listen(consumer)
    reader.close()

    assert context._passed
    assert context.langServer._shutdown


def gen_alt_log(context, mode='tcp'):
    if mode == 'tcp':
        check = 'Serving LangServer on (0.0.0.0, 20801)\n'
    elif mode == 'stdio':
        check = 'Starting LangServer IO language server\n'
    else:
        assert False

    def alt_log(*args, **kargs):
        result = io.StringIO()
        print(*args, file=result, **kargs)

        value = result.getvalue()
        if value == check:
            context._server_alive = True

    return alt_log


@given('the server started in TCP mode')
def step_impl(context):
    context._server_alive = False
    host, port = ('0.0.0.0', 20801)

    with mock.patch('coala_langserver.langserver.log') as mock_log:
        mock_log.side_effect = gen_alt_log(context)

        sys.argv = ['', '--mode', 'tcp', '--addr', str(port)]
        context.thread = Thread(target=main)
        context.thread.daemon = True
        context.thread.start()

        for _ in range(20):
            if context._server_alive:
                break
            else:
                time.sleep(1)
        else:
            assert False

        context.sock = socket.create_connection(
            address=(host, port), timeout=10)
        context.f = context.sock.makefile('rwb')

        context.reader = streams.JsonRpcStreamReader(context.f)
        context.writer = streams.JsonRpcStreamWriter(context.f)


@when('I send a initialize request via TCP stream')
def step_impl(context):
    request = {
        'method': 'initialize',
        'params': {
            'rootUri': '/Users/mock-user/mock-dir',
            'capabilities': {},
        },
        'id': 1,
        'jsonrpc': '2.0',
    }
    context.writer.write(request)


@then('it should return the response with textDocumentSync via TCP')
def step_impl(context):
    context._passed = False

    def consumer(response):
        assert response is not None
        assert response['result']['capabilities']['textDocumentSync'] == 1
        context.f.close()
        context._passed = True

    context.reader.listen(consumer)
    context.reader.close()
    context.sock.close()

    if not context._passed:
        assert False


@given('I send a initialize request via stdio stream')
def step_impl(context):
    context.f = tempfile.TemporaryFile()
    context.writer = streams.JsonRpcStreamWriter(context.f)

    request = {
        'method': 'initialize',
        'params': {
            'rootUri': '/Users/mock-user/mock-dir',
            'capabilities': {},
        },
        'id': 1,
        'jsonrpc': '2.0',
    }
    context.writer.write(request)
    context.f.seek(0)


@when('the server is started in stdio mode')
def step_impl(context):
    context._server_alive = False
    context.o = tempfile.TemporaryFile()

    with mock.patch('coala_langserver.langserver.log') as mock_log:
        mock_log.side_effect = gen_alt_log(context, 'stdio')

        context.thread = Thread(target=start_io_lang_server, args=(
            LangServer, context.f, context.o))
        context.thread.daemon = True
        context.thread.start()

        for _ in range(10):
            if context._server_alive:
                break
            else:
                time.sleep(1)
        else:
            assert False


@then('it should return the response with textDocumentSync via stdio')
def step_impl(context):
    context._passed = False

    def consumer(response):
        assert response is not None
        assert response['result']['capabilities']['textDocumentSync'] == 1
        context.f.close()
        context._passed = True

    last = -9999
    while context.o.tell() != last:
        last = context.o.tell()
        time.sleep(1)

    context.o.seek(0)
    context.reader = streams.JsonRpcStreamReader(context.o)
    context.reader.listen(consumer)
    context.reader.close()

    if not context._passed:
        assert False
