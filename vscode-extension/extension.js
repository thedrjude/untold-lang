const vscode = require("vscode");
const path   = require("path");
const cp     = require("child_process");
const fs     = require("fs");

let outputChannel;

function getOutputChannel() {
  if (!outputChannel) {
    outputChannel = vscode.window.createOutputChannel("Untold Lang");
  }
  return outputChannel;
}

function findCliPath(workspaceRoot) {
  // Try config setting first
  const config  = vscode.workspace.getConfiguration("untold");
  const cfgPath = config.get("cliPath");
  if (cfgPath && fs.existsSync(cfgPath)) return cfgPath;

  // Auto-detect: walk up from workspace looking for cli/main.py
  const candidates = [
    path.join(workspaceRoot, "cli", "main.py"),
    path.join(workspaceRoot, "..", "cli", "main.py"),
    path.join(workspaceRoot, "..", "..", "cli", "main.py"),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

function getPython() {
  const config = vscode.workspace.getConfiguration("untold");
  return config.get("pythonPath") || "python3";
}

function runUntoldFile(filePath, command = "run") {
  const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri?.fsPath;
  if (!workspaceRoot) {
    vscode.window.showErrorMessage("Untold Lang: No workspace folder open.");
    return;
  }

  const cliPath = findCliPath(workspaceRoot);
  if (!cliPath) {
    vscode.window.showErrorMessage(
      "Untold Lang: Could not find cli/main.py. Set 'untold.cliPath' in settings."
    );
    return;
  }

  const python  = getPython();
  const channel = getOutputChannel();
  channel.clear();
  channel.show(true);

  const timestamp = new Date().toLocaleTimeString();
  channel.appendLine(`─────────────────────────────────────────`);
  channel.appendLine(`  Untold Lang — ${command.toUpperCase()} — ${timestamp}`);
  channel.appendLine(`  File: ${path.basename(filePath)}`);
  channel.appendLine(`─────────────────────────────────────────`);

  const cmd  = `${python} "${cliPath}" ${command} "${filePath}"`;
  const proc = cp.spawn(python, [cliPath, command, filePath], {
    cwd: path.dirname(cliPath),
  });

  proc.stdout.on("data", (data) => {
    channel.append(data.toString());
  });

  proc.stderr.on("data", (data) => {
    channel.append(data.toString());
  });

  proc.on("close", (code) => {
    channel.appendLine(`─────────────────────────────────────────`);
    if (code === 0) {
      channel.appendLine(`  Done (exit 0)`);
    } else {
      channel.appendLine(`  Exited with code ${code}`);
    }
    channel.appendLine(`─────────────────────────────────────────`);
  });

  proc.on("error", (err) => {
    channel.appendLine(`[Untold] Failed to start process: ${err.message}`);
    vscode.window.showErrorMessage(
      `Untold Lang: Could not run Python. Is '${python}' installed?`
    );
  });
}

function activate(context) {
  // Run file command
  const runCmd = vscode.commands.registerCommand("untold.runFile", () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage("Untold Lang: No active file.");
      return;
    }
    // Save before running
    editor.document.save().then(() => {
      runUntoldFile(editor.document.uri.fsPath, "run");
    });
  });

  // Check syntax command
  const checkCmd = vscode.commands.registerCommand("untold.checkFile", () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage("Untold Lang: No active file.");
      return;
    }
    editor.document.save().then(() => {
      runUntoldFile(editor.document.uri.fsPath, "check");
    });
  });

  context.subscriptions.push(runCmd, checkCmd);

  // Status bar item
  const statusBar = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left, 100
  );
  statusBar.text     = "$(play) Run .ut";
  statusBar.command  = "untold.runFile";
  statusBar.tooltip  = "Run this Untold Lang file (Ctrl+Shift+R)";
  statusBar.color    = "#9FE1CB";

  // Show status bar only for .ut files
  const updateStatusBar = () => {
    const editor = vscode.window.activeTextEditor;
    if (editor && editor.document.fileName.endsWith(".ut")) {
      statusBar.show();
    } else {
      statusBar.hide();
    }
  };

  vscode.window.onDidChangeActiveTextEditor(updateStatusBar);
  updateStatusBar();
  context.subscriptions.push(statusBar);
}

function deactivate() {
  if (outputChannel) outputChannel.dispose();
}

module.exports = { activate, deactivate };