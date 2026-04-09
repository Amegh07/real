import React from 'react';

const WEATHER_ICONS = {
  Clear: '🌙', Sunny: '☀️', Cloudy: '☁️', Rainy: '🌧️', Stormy: '⛈️',
};

export default function Header({ isConnected, isRunning, status }) {
  const day      = status?.day      ?? '—';
  const timeOfDay = status?.time_of_day ?? '—';
  const weather  = status?.weather  ?? '—';
  const pop      = status?.population ?? '—';

  return (
    <header className="glass" style={{ padding: '1.2rem 2rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1.5rem' }}>
      {/* Left: title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{
          width: 44, height: 44,
          background: 'linear-gradient(135deg, var(--accent-blue), var(--accent-purple))',
          borderRadius: 12,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '1.3rem', flexShrink: 0,
          boxShadow: '0 0 20px rgba(59,130,246,0.35)',
        }}>🌍</div>
        <div>
          <h1 style={{ fontSize: '1.45rem', margin: 0 }}>Reality Simulator</h1>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>AI Agent World — Phase 7</div>
        </div>
      </div>

      {/* Center: world telemetry pills */}
      <div style={{ display: 'flex', gap: '0.6rem', flexWrap: 'wrap' }}>
        <span className="badge badge-blue">📅 Day {day}</span>
        <span className="badge badge-purple">🕐 {timeOfDay}</span>
        <span className="badge badge-cyan">{WEATHER_ICONS[weather] ?? '🌡️'} {weather}</span>
        <span className="badge badge-green">👥 {pop} Agents</span>
      </div>

      {/* Right: connection status */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 0.7 + 'rem', flexShrink: 0 }}>
        <div style={{ textAlign: 'right' }}>
          <div style={{
            display: 'flex', alignItems: 'center', gap: '0.4rem',
            color: !isConnected ? 'var(--accent-red)'
                 : isRunning   ? 'var(--accent-green)'
                 :                'var(--accent-yellow)',
            fontWeight: 600, fontSize: '0.9rem',
          }}>
            <span className={isRunning ? 'dot-live' : ''} style={{ fontSize: '0.6rem' }}>●</span>
            {!isConnected ? 'Disconnected' : isRunning ? 'Simulation Running' : 'Paused'}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
            {isConnected ? 'FastAPI Backend Linked' : 'Attempting reconnect…'}
          </div>
        </div>
      </div>
    </header>
  );
}
