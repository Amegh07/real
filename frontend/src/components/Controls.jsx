import React from 'react';
import { pauseSimulation, resumeSimulation } from '../api';

export default function Controls({ isRunning }) {
  return (
    <div className="glass-panel" style={{ padding: '1rem 1.5rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <button 
        onClick={resumeSimulation}
        disabled={isRunning}
        style={{
          background: isRunning ? 'var(--bg-dark)' : 'var(--accent-green)',
          color: isRunning ? 'var(--text-muted)' : '#000',
          border: 'none',
          padding: '0.6rem 1.2rem',
          borderRadius: '8px',
          fontWeight: 'bold',
          cursor: isRunning ? 'not-allowed' : 'pointer'
        }}>
        ▶ Resume
      </button>

      <button 
        onClick={pauseSimulation}
        disabled={!isRunning}
        style={{
          background: !isRunning ? 'var(--bg-dark)' : 'var(--accent-red)',
          color: !isRunning ? 'var(--text-muted)' : '#fff',
          border: 'none',
          padding: '0.6rem 1.2rem',
          borderRadius: '8px',
          fontWeight: 'bold',
          cursor: !isRunning ? 'not-allowed' : 'pointer'
        }}>
        ⏸ Pause
      </button>
      
      <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginLeft: 'auto' }}>
        Status: <strong style={{ color: isRunning ? 'var(--accent-green)' : 'var(--accent-red)' }}>
          {isRunning ? "Running" : "Paused"}
        </strong>
      </span>
    </div>
  );
}
