import React, { useEffect, useRef } from 'react';
import { Terminal } from 'lucide-react';

const TerminalLog = ({ logs }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const getColor = (level) => {
    switch (level) {
      case 'info': return 'text-blue-400';
      case 'warn': return 'text-yellow-400';
      case 'error': return 'text-red-400';
      case 'success': return 'text-green-400';
      default: return 'text-gray-300';
    }
  };

  return (
    <div className="flex flex-col h-full rounded-xl border border-gray-800 bg-gray-950 shadow-xl overflow-hidden min-h-[300px]">
      <div className="p-3 border-b border-gray-800 bg-gray-900 flex items-center gap-2">
        <Terminal size={16} className="text-gray-400" />
        <span className="text-sm font-medium text-gray-300">Agent Execution Logs</span>
      </div>
      <div 
        ref={scrollRef}
        className="flex-grow p-4 overflow-y-auto font-mono text-sm leading-relaxed"
      >
        {logs.length === 0 ? (
          <div className="text-gray-600 italic">Waiting for agent to start...</div>
        ) : (
          logs.map((log) => (
            <div key={log.id} className="mb-1 flex gap-3 hover:bg-gray-800/50 px-2 py-1 rounded">
              <span className="text-gray-600 shrink-0">[{log.timestamp}]</span>
              <span className={`${getColor(log.level)}`}>{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default TerminalLog;
