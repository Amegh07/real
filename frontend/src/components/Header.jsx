import React from 'react';

export default function Header({ isConnected, isRunning }) {
  return (
    <header className="glass-panel" style={{ padding: '1.5rem 2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div>
        <h1 style={{ fontSize: '1.8rem', margin: 0 }}>Reality Simulator Engine</h1>
        <p style={{ color: 'var(--text-muted)', marginTop: '0.25rem' }}>AI Agent World Dashboard</p>
      </div>
      <div style={{ display: 'flex', gap: '1rem' }}>
        <div style={{ textAlign: 'right' }}>
          <div style={{ color: isConnected ? (isRunning ? 'var(--accent-green)' : 'var(--accent-blue)') : 'var(--accent-red)', fontWeight: '600' }}>
            ● {isConnected ? (isRunning ? "Simulation Running" : "Simulation Paused") : "Disconnected"}
          </div>
          <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
            {isConnected ? "Linked to FastAPI" : "Trying to reach backend"}
          </div>
        </div>
      </div>
    </header>
  );
}
