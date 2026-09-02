import React from 'react';
import { DiffEditor } from '@monaco-editor/react';

const DiffViewer = ({ original, modified, language = 'python' }) => {
  return (
    <DiffEditor
      height="100%"
      language={language}
      original={original}
      modified={modified}
      theme="vs-dark"
      options={{
        readOnly: true,
        renderSideBySide: true,
        minimap: { enabled: false },
        fontSize: 14,
        scrollBeyondLastLine: false,
        automaticLayout: true,
      }}
    />
  );
};

export default DiffViewer;
