'use strict';

import * as net from 'net';
import { resolve, } from 'path';

import {
    Disposable,
    ExtensionContext,
    workspace,
    WorkspaceConfiguration,
} from 'vscode';
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
        'c',
        'coffeescript',
        'cpp',
        'csharp',
        'css',
        'dockerfile',
        'git-commit',
        'go',
        'html',
        'jade',
        'java',
        'javascript',
        'json',
        'latex',
        'less',
        'lua',
        'markdown',
        'objective-c',
        'objective-cpp',
        'perl',
        'php',
        'python',
        'r',
        'ruby',
        'scss',
        'shellscript',
        'sql',
        'swift',
        'tex',
        'typescript',
        'xml',
        'yaml',
    ],
};

function getSettings(): { [id: string]: number; } {
    const config: WorkspaceConfiguration = workspace.getConfiguration(
                                            'coalals');

    return {
        maxWorkers: Number(config.get('maxWorkers')),
        tcpPort: Number(config.get('tcpPort')),
    };
}

function startLangServer(
    command: string,
    documentSelector: string | string[],
    maxWorkers: number
): Disposable {
    const serverOptions: ServerOptions = {
        args: [
            '--max-workers',
            String(maxWorkers),
        ],
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
    };
    return new LanguageClient(
        `tcp lang server (port ${addr})`,
        serverOptions,
        clientOptions
    ).start();
}

export function activate(context: ExtensionContext) {
    const debug: boolean = false;
    const {
        tcpPort,
        maxWorkers,
    } = getSettings();

    if (!debug) {
        context.subscriptions.push(
            startLangServer(
                coalals.command.usage,
                coalals.langs,
                maxWorkers
            )
        );
    } else {
        // For Debug
        context.subscriptions.push(
            startLangServerTCP(tcpPort, coalals.langs));
    }

    console.log('coala language server is running.');
}
