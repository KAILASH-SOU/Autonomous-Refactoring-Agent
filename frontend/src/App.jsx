import React, { useState } from 'react';
import DiffViewer from './components/DiffViewer';
import TerminalLog from './components/TerminalLog';
import ActionPanel from './components/ActionPanel';
import { useWebSocket } from './hooks/useWebSocket';

const App = () => {
  const { logs, diff, isConnected, sendMessage } = useWebSocket('ws://localhost:8000/ws');
  
  const [repoUrl, setRepoUrl] = useState('');
  
  const handleStart = () => {
    if (!repoUrl) return;
    sendMessage({ type: 'start', payload: { repoUrl } });
  };
  
  const handleApprove = () => {
    sendMessage({ type: 'approve' });
  };

  return (
    <div className="flex flex-col h-screen max-w-[1600px] mx-auto p-4 gap-4">
      <header className="flex justify-between items-center pb-4 border-b border-gray-800">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Autonomous Agentic Refactoring
        </h1>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
          <span className="text-sm text-gray-400">{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 flex-grow overflow-hidden">
        <div className="lg:col-span-2 flex flex-col gap-4 overflow-hidden rounded-xl border border-gray-800 bg-gray-900 shadow-xl">
          <div className="p-3 border-b border-gray-800 bg-gray-950 flex justify-between items-center">
            <span className="text-sm font-medium text-gray-300">Code Diff Viewer</span>
            <span className="text-xs text-gray-500 px-2 py-1 bg-gray-800 rounded">AST-Aware</span>
          </div>
          <div className="flex-grow overflow-hidden relative">
            {diff ? (
              <DiffViewer original={diff.original} modified={diff.modified} />
            ) : (
              <div className="absolute inset-0 flex items-center justify-center text-gray-600">
                No diff available yet. Start a refactoring task.
              </div>
            )}
          </div>
        </div>

        <div className="flex flex-col gap-4 overflow-hidden">
          <ActionPanel 
            repoUrl={repoUrl} 
            setRepoUrl={setRepoUrl} 
            onStart={handleStart} 
            onApprove={handleApprove}
            hasDiff={!!diff}
          />
          <TerminalLog logs={logs} />
        </div>
      </div>
    </div>
  );
}

export default App;
