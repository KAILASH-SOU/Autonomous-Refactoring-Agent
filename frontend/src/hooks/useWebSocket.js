import { useState, useEffect, useRef, useCallback } from 'react';

export function useWebSocket(url) {
  const [isConnected, setIsConnected] = useState(false);
  const [logs, setLogs] = useState([]);
  const [diff, setDiff] = useState(null);
  
  const wsRef = useRef(null);

  useEffect(() => {
    const connect = () => {
      try {
        const ws = new WebSocket(url);
        
        ws.onopen = () => {
          setIsConnected(true);
        };
        
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          
          if (data.type === 'log') {
            setLogs((prev) => [...prev, {
              id: Math.random().toString(36).substr(2, 9),
              timestamp: new Date().toLocaleTimeString(),
              level: data.payload.level || 'info',
              message: data.payload.message
            }]);
          } else if (data.type === 'diff') {
            setDiff({
              original: data.payload.original,
              modified: data.payload.modified
            });
          }
        };
        
        ws.onclose = () => {
          setIsConnected(false);
          // Try to reconnect after 3 seconds
          setTimeout(connect, 3000);
        };
        
        wsRef.current = ws;
      } catch (err) {
        console.error("WebSocket connection error:", err);
      }
    };
    
    connect();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [url]);

  const sendMessage = useCallback((message) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, [isConnected]);

  return { isConnected, logs, diff, sendMessage };
}
