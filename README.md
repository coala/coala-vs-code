# coala-vs-code

A visual studio code plugin working via [Language Server Protocol (LSP)](https://github.com/Microsoft/language-server-protocol/blob/master/protocol.md).Python versions 3.x is supported.

**Note: this language server is currently in the early stages of active development and only supports to be run in debug mode now.**

## Getting started

You'll need python version 3.5 or greater.

1. `pip3 install -r requirements.txt`
1. `python3 langserver-python.py --mode=tcp --addr=2087`

To try it in [Visual Studio Code](https://code.visualstudio.com), open ./vscode-client in VS Code and turn to debug view, launch the extension.

## Feature preview

![](./docs/images/demo.gif)

## Reference

* [python-langserver](https://github.com/sourcegraph/python-langserver)
