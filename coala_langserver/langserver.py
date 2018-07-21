import sys
import argparse
import socketserver

from pyls.jsonrpc.endpoint import Endpoint
from pyls.jsonrpc.dispatchers import MethodDispatcher
from pyls.jsonrpc.streams import JsonRpcStreamReader
from pyls.jsonrpc.streams import JsonRpcStreamWriter
from coala_utils.decorators import enforce_signature
from .log import log
from .coalashim import run_coala_with_specific_file
from .uri import path_from_uri
from .diagnostic import output_to_diagnostics


class _StreamHandlerWrapper(socketserver.StreamRequestHandler, object):
    """
    A wrapper class that is used to construct a custom handler class.
    """

    delegate = None

    def setup(self):
        super(_StreamHandlerWrapper, self).setup()
        self.delegate = self.DELEGATE_CLASS(self.rfile, self.wfile)

    def handle(self):
        self.delegate.start()


class LangServer(MethodDispatcher):
    """
    Language server for coala base on JSON RPC.
    """

    def __init__(self, rx, tx):
        self.root_path = None
        self._jsonrpc_stream_reader = JsonRpcStreamReader(rx)
        self._jsonrpc_stream_writer = JsonRpcStreamWriter(tx)
        self._endpoint = Endpoint(self, self._jsonrpc_stream_writer.write)
        self._dispatchers = []
        self._shutdown = False

    def start(self):
        self._jsonrpc_stream_reader.listen(self._endpoint.consume)

    def m_initialize(self, **params):
        """
        Serve for the initialization request.
        """
        # Notice that the root_path could be None.
        if 'rootUri' in params:
            self.root_path = path_from_uri(params['rootUri'])
        elif 'rootPath' in params:
            self.root_path = path_from_uri(params['rootPath'])
        return {
            'capabilities': {
                'textDocumentSync': 1
            }
        }

    def m_text_document__did_save(self, **params):
        """
        Serve for did_change request.
        """
        uri = params['textDocument']['uri']
        path = path_from_uri(uri)
        diagnostics = output_to_diagnostics(
            run_coala_with_specific_file(self.root_path, path))
        self.send_diagnostics(path, diagnostics)

    def m_shutdown(self, **_kwargs):
        self._shutdown = True

    # TODO: Support did_change and did_change_watched_files.
    # def serve_change(self, request):
    #     '""Serve for the request of documentation changed.""'
    #     params = request['params']
    #     uri = params['textDocument']['uri']
    #     path = path_from_uri(uri)
    #     diagnostics = output_to_diagnostics(
    #         run_coala_with_specific_file(self.root_path, path))
    #     self.send_diagnostics(path, diagnostics)
    #     return None
    #
    # def serve_did_change_watched_files(self, request):
    #     '""Serve for thr workspace/didChangeWatchedFiles request.""'
    #     changes = request['changes']
    #     for fileEvent in changes:
    #         uri = fileEvent['uri']
    #         path = path_from_uri(uri)
    #         diagnostics = output_to_diagnostics(
    #             run_coala_with_specific_file(self.root_path, path))
    #         self.send_diagnostics(path, diagnostics)

    def send_diagnostics(self, path, diagnostics):
        _diagnostics = []
        if diagnostics is not None:
            _diagnostics = diagnostics
        params = {
            'uri': 'file://{0}'.format(path),
            'diagnostics': _diagnostics,
        }
        self._endpoint.notify('textDocument/publishDiagnostics', params=params)


@enforce_signature
def start_tcp_lang_server(handler_class: LangServer, bind_addr, port):
    # Construct a custom wrapper class around the user's handler_class
    wrapper_class = type(
        handler_class.__name__ + 'Handler',
        (_StreamHandlerWrapper,),
        {'DELEGATE_CLASS': handler_class},
    )

    try:
        server = socketserver.TCPServer((bind_addr, port), wrapper_class)
    except Exception as e:
        log('Fatal Exception: {}'.format(e))
        sys.exit(1)

    log('Serving {} on ({}, {})'.format(
        handler_class.__name__, bind_addr, port))
    try:
        server.serve_forever()
    finally:
        log('Shutting down')
        server.server_close()


@enforce_signature
def start_io_lang_server(handler_class: LangServer, rstream, wstream):
    log('Starting {} IO language server'.format(handler_class.__name__))
    server = handler_class(rstream, wstream)
    server.start()


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--mode', default='stdio',
                        help='communication (stdio|tcp)')
    parser.add_argument('--addr', default=2087,
                        help='server listen (tcp)', type=int)

    args = parser.parse_args()

    if args.mode == 'stdio':
        start_io_lang_server(LangServer, sys.stdin.buffer, sys.stdout.buffer)
    elif args.mode == 'tcp':
        host, addr = '0.0.0.0', args.addr
        start_tcp_lang_server(LangServer, host, addr)


if __name__ == '__main__':
    main()
