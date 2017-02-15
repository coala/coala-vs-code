# coala-vs-code

[![Build Status](https://travis-ci.org/coala/coala-vs-code.svg?branch=master)](https://travis-ci.org/coala/coala-vs-code)
[![codecov](https://codecov.io/gh/coala/coala-vs-code/branch/master/graph/badge.svg)](https://codecov.io/gh/coala/coala-vs-code)

A visual studio code plugin working via [Language Server Protocol (LSP)](https://github.com/Microsoft/language-server-protocol/blob/master/protocol.md).Python versions 3.x is supported.

## Feature preview

![](./docs/images/demo.gif)

## Setting up your dev environment, coding, and debugging

You'll need python version 3.5 or greater, run `pip3 install -r requirements.txt` to install the requirements, and run `python3 langserver-python.py --mode=tcp --addr=2087` to start a local languager server listening at port 2087.

Then you should update the `./vscode-client/src/extension.ts` to make client in TCP mode.

```diff
export function activate(context: ExtensionContext) {
-   context.subscriptions.push(startLangServer
-   (require("path").resolve(__dirname, '../coala-langserver.sh'), ["python"]));
+   context.subscriptions.push(startLangServerTCP(2087, ["python"]));
    console.log("coala language server is running.");
}
```

To try it in [Visual Studio Code](https://code.visualstudio.com), open ./vscode-client in VS Code and turn to debug view, launch the extension.

## Known bugs

* [Language server restarts when `didSave` requests come](https://github.com/coala/coala-vs-code/issues/7)

## Reference

* [python-langserver](https://github.com/sourcegraph/python-langserver)
