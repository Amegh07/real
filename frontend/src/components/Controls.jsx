import React, { useState } from 'react';
import { pauseSimulation, resumeSimulation, setSpeed } from '../api';

const SPEEDS = [
  { label: '0.5×', tps: 0.5 },
  { label: '1×',   tps: 1   },
  { label: '2×',   tps: 2   },
  { label: '5×',   tps: 5   },
];

export default function Controls({ isRunning, onToggle }) {
  const [activeSpeed, setActiveSpeed] = useState(1);
  const [error, setError] = useState(null);

  const handlePause = async () => {
    try {
      setError(null);
      await pauseSimulation();
      onToggle && onToggle();
    } catch (err) {
      setError('Failed to pause');
    }
  };
  const handleResume = async () => {
    try {
      setError(null);
      await resumeSimulation();
      onToggle && onToggle();
    } catch (err) {
      setError('Failed to resume');
    }
  };
  const handleSpeed = async (tps) => {
    try {
      setError(null);
      setActiveSpeed(tps);
      await setSpeed(tps);
    } catch (err) {
      setError('Failed to set speed');
    }
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.7rem', flexWrap: 'wrap' }}>
      {/* Play/Pause */}
      <button className="btn btn-green" onClick={handleResume} disabled={isRunning}>
        ▶ Resume
      </button>
      <button className="btn btn-red" onClick={handlePause} disabled={!isRunning}>
        ⏸ Pause
      </button>

      {/* Speed selector */}
      <div style={{
        display: 'flex', gap: '0.3rem',
        background: 'rgba(0,0,0,0.3)',
        padding: '4px',
        borderRadius: 'var(--radius-sm)',
        border: '1px solid var(--border-subtle)',
      }}>
        {SPEEDS.map(s => (
          <button
            key={s.tps}
            onClick={() => handleSpeed(s.tps)}
            style={{
              padding: '0.3rem 0.65rem',
              border: 'none',
              borderRadius: 6,
              fontFamily: 'var(--font-body)',
              fontWeight: 600,
              fontSize: '0.78rem',
              cursor: 'pointer',
              transition: 'all 0.15s',
              background: activeSpeed === s.tps ? 'var(--accent-blue-dim)' : 'transparent',
              color:      activeSpeed === s.tps ? 'var(--accent-blue)'     : 'var(--text-muted)',
              border:     activeSpeed === s.tps ? '1px solid rgba(59,130,246,0.35)' : '1px solid transparent',
            }}
          >
            {s.label}
          </button>
        ))}
      </div>
    </div>
  );
}
