# coala-vs-code

[![Build Status](https://travis-ci.org/coala/coala-vs-code.svg?branch=master)](https://travis-ci.org/coala/coala-vs-code)
[![codecov](https://codecov.io/gh/coala/coala-vs-code/branch/master/graph/badge.svg)](https://codecov.io/gh/coala/coala-vs-code)

A visual studio code plugin for the coala-ls working via [Language Server Protocol (LSP)](https://github.com/Microsoft/language-server-protocol/blob/master/protocol.md).Python versions 3.x is supported.

## Setting up your dev environment, coding, and debugging

You'll need python version 3.5 or greater. Install coala-ls from <http://github.com/coala/coala-ls>.

To try it in [Visual Studio Code](https://code.visualstudio.com), open ./vscode-client in VS Code and turn to debug view, launch the extension.

## Known bugs

- [Language server restarts when `didSave` requests come](https://github.com/coala/coala-vs-code/issues/7)

## Reference

- [python-langserver](https://github.com/sourcegraph/python-langserver)
