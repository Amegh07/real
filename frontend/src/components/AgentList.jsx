import React from 'react';

const ProgressBar = ({ label, value, color }) => (
  <div style={{ marginBottom: '0.5rem' }}>
    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '0.2rem', color: 'var(--text-muted)' }}>
      <span>{label}</span>
      <span>{value.toFixed(0)}/100</span>
    </div>
    <div style={{ height: '6px', background: 'rgba(0,0,0,0.3)', borderRadius: '3px', overflow: 'hidden' }}>
      <div style={{ width: `${value}%`, height: '100%', background: color, transition: 'width 0.3s ease' }} />
    </div>
  </div>
);

export default function AgentList({ agents }) {
  if (!agents || agents.length === 0) return <div className="glass-panel" style={{ padding: '2rem' }}>Loading agents...</div>;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.2rem' }}>
      {agents.map(agent => (
        <div key={agent.id} className="glass-panel" style={{ padding: '1.2rem', display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
          
          {/* Header */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <h3 style={{ margin: 0, textTransform: 'none', color: 'var(--text-main)', fontSize: '1.2rem' }}>{agent.name}</h3>
              <div style={{ fontSize: '0.8rem', color: 'var(--accent-purple)' }}>{agent.personality.toUpperCase()}</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ color: 'var(--accent-green)', fontWeight: 'bold', fontSize: '1.1rem' }}>${agent.money.toFixed(0)}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', background: 'rgba(255,255,255,0.05)', padding: '2px 6px', borderRadius: '4px', marginTop: '4px', display: 'inline-block' }}>
                {agent.job || "Unemployed"}
              </div>
            </div>
          </div>

          {/* Goal & Action */}
          <div style={{ background: 'rgba(0,0,0,0.2)', padding: '0.6rem', borderRadius: '8px', fontSize: '0.85rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
              <strong style={{ color: 'var(--text-muted)' }}>Goal:</strong>
              <span style={{ color: 'var(--accent-blue)', textAlign: 'right', wordBreak: 'break-word', maxWidth: '70%' }}>"{agent.goal}"</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <strong style={{ color: 'var(--text-muted)' }}>Doing:</strong>
              <span style={{ textTransform: 'capitalize' }}>{agent.current_action.replace('_', ' ')}</span>
            </div>
          </div>

          {/* Needs */}
          <div style={{ marginTop: '0.5rem' }}>
            <ProgressBar label="Hunger" value={agent.hunger} color="var(--accent-red)" />
            <ProgressBar label="Energy" value={agent.energy} color="var(--accent-blue)" />
            <ProgressBar label="Happiness" value={agent.happiness} color="var(--accent-green)" />
          </div>

          {/* Social */}
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '0.8rem', marginTop: 'auto' }}>
            <span style={{ color: 'var(--text-muted)' }}>💖 {agent.friend_count} Friends</span>
            <span style={{ color: 'var(--text-muted)' }}>⚔️ {agent.rival_count} Rivals</span>
            <span style={{ color: 'var(--text-muted)' }}>🕰️ Age: {agent.age_ticks}</span>
          </div>
          
        </div>
      ))}
    </div>
  );
}
