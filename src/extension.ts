'use strict';

import * as net from 'net';
import { resolve, } from 'path';

import { Disposable, ExtensionContext, workspace } from 'vscode';
import {
    CloseAction,
    ErrorAction,
    ErrorHandler,
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    SettingMonitor,
    TransportKind,
} from 'vscode-languageclient';

const coalals = {
    command: {
        usage: resolve(__dirname, '../coala-langserver.sh'),
    },

    langs: [
        'html',
        'python',
    ],
};

function startLangServer(
    command: string,
    documentSelector: string | string[]
): Disposable {
    const serverOptions: ServerOptions = {
        command: command,
    };
    const clientOptions: LanguageClientOptions = {
        documentSelector: documentSelector,
    };
    return new LanguageClient(
        'coala langserver', serverOptions, clientOptions).start();
}

function startLangServerTCP(
    addr: number,
    documentSelector: string | string[]
): Disposable {
    const serverOptions: ServerOptions = () => {
        return new Promise((resolve, reject) => {
            const client = new net.Socket();
            client.connect(
                addr,
                '127.0.0.1',
                () => {
                    resolve({
                        reader: client,
                        writer: client,
                    });
                }
            );
        });
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: documentSelector,
        synchronize: {
            // Notify the server about file changes to '.clientrc
            // files contain in the workspace
            fileEvents: workspace.createFileSystemWatcher('**/.py'),
        },
    };
    return new LanguageClient(
        `tcp lang server (port ${addr})`,
        serverOptions,
        clientOptions
    ).start();
}

export function activate(context: ExtensionContext) {
    context.subscriptions.push(
        startLangServer(
            coalals.command.usage,
            coalals.langs
        )
    );
    // For Debug
    // context.subscriptions.push(startLangServerTCP(2087, coalals.langs));
    console.log('coala language server is running.');
}
