import React from 'react';
import { Play, GitPullRequest, Settings } from 'lucide-react';

const ActionPanel = ({ 
  repoUrl, 
  setRepoUrl, 
  onStart, 
  onApprove,
  hasDiff
}) => {
  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900 p-5 shadow-xl">
      <h2 className="text-lg font-medium text-gray-200 mb-4 flex items-center gap-2">
        <Settings size={18} className="text-purple-400" />
        Task Configuration
      </h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-400 mb-1">Target Repository</label>
          <input 
            type="text" 
            placeholder="e.g., https://github.com/user/repo"
            className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-2 text-sm text-gray-200 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-all"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
          />
        </div>

        <div className="pt-2 flex flex-col gap-3">
          <button 
            onClick={onStart}
            disabled={!repoUrl}
            className="w-full flex items-center justify-center gap-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-800 disabled:text-gray-500 text-white font-medium py-2.5 px-4 rounded-lg transition-colors"
          >
            <Play size={16} />
            Start Refactoring Agent
          </button>
          
          <button 
            onClick={onApprove}
            disabled={!hasDiff}
            className="w-full flex items-center justify-center gap-2 bg-gray-800 hover:bg-green-600/90 disabled:bg-gray-900 disabled:text-gray-700 disabled:border-gray-800 border border-green-500/30 text-green-400 disabled:border-gray-800 font-medium py-2.5 px-4 rounded-lg transition-all"
          >
            <GitPullRequest size={16} />
            Approve & Create PR
          </button>
        </div>
      </div>
    </div>
  );
};

export default ActionPanel;
