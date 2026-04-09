import React from 'react';

const PERSONALITY_COLORS = {
  industrious: 'var(--accent-blue)',
  lazy:        'var(--accent-yellow)',
  social:      'var(--accent-purple)',
  reclusive:   'var(--accent-cyan)',
  reckless:    'var(--accent-red)',
  cautious:    'var(--accent-green)',
};

const PERSONALITY_ICONS = {
  industrious: '⚙️', lazy: '😴', social: '🤝',
  reclusive: '🔮', reckless: '⚡', cautious: '🛡️',
};

const Bar = ({ value, color }) => (
  <div className="progress-track" style={{ flex: 1 }}>
    <div
      className="progress-fill"
      style={{
        width: `${Math.max(0, Math.min(100, value))}%`,
        background: value < 20
          ? 'var(--accent-red)'
          : value < 45
          ? 'var(--accent-yellow)'
          : color,
      }}
    />
  </div>
);

export default function AgentList({ agents, onSelect }) {
  if (!agents || agents.length === 0) {
    return (
      <div className="glass" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        Loading agents…
      </div>
    );
  }

  return (
    <div className="agent-grid">
      {agents.map(agent => {
        const isCritical = agent.hunger < 15 || agent.energy < 15 || agent.happiness < 15;
        const pColor = PERSONALITY_COLORS[agent.personality] || 'var(--accent-blue)';

        return (
          <div
            key={agent.id}
            className={`glass glass-clickable fade-in-up ${isCritical ? 'pulse-critical' : ''}`}
            onClick={() => onSelect && onSelect(agent)}
            style={{
              padding: '1.2rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.9rem',
              borderLeft: `3px solid ${pColor}`,
            }}
          >
            {/* Header row */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '1.05rem' }}>{PERSONALITY_ICONS[agent.personality] ?? '👤'}</span>
                  <span style={{ fontWeight: 700, fontSize: '1.05rem', color: 'var(--text-main)' }}>{agent.name}</span>
                  {isCritical && <span className="badge badge-red" style={{ padding: '1px 6px', fontSize: '0.65rem' }}>CRISIS</span>}
                </div>
                <div style={{ marginTop: '3px' }}>
                  <span className="badge" style={{ background: `${pColor}22`, color: pColor, border: `1px solid ${pColor}44`, fontSize: '0.65rem' }}>
                    {agent.personality}
                  </span>
                </div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ color: 'var(--accent-green)', fontWeight: 700, fontSize: '1.1rem' }}>
                  ${agent.money?.toFixed(0)}
                </div>
                <div style={{ marginTop: '3px' }}>
                  <span className="badge badge-cyan" style={{ fontSize: '0.65rem' }}>
                    {agent.job || 'Unemployed'}
                  </span>
                </div>
              </div>
            </div>

            {/* Goal & action */}
            <div style={{ background: 'rgba(0,0,0,0.2)', borderRadius: 8, padding: '0.55rem 0.75rem', fontSize: '0.8rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.3rem', gap: '0.5rem' }}>
                <span style={{ color: 'var(--text-muted)', flexShrink: 0 }}>Goal:</span>
                <span style={{ color: 'var(--accent-blue)', textAlign: 'right', wordBreak: 'break-word' }}>"{agent.goal}"</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: 'var(--text-muted)' }}>Doing:</span>
                <span style={{ textTransform: 'capitalize', color: 'var(--text-main)' }}>
                  {agent.current_action?.replace(/_/g, ' ') ?? '—'}
                </span>
              </div>
            </div>

            {/* Need bars */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {[
                { label: 'Hunger', value: agent.hunger, color: '#f87171' },
                { label: 'Energy', value: agent.energy, color: 'var(--accent-blue)' },
                { label: 'Happy',  value: agent.happiness, color: 'var(--accent-green)' },
              ].map(({ label, value, color }) => (
                <div key={label} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', width: 42, flexShrink: 0 }}>{label}</span>
                  <Bar value={value} color={color} />
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', width: 26, textAlign: 'right', flexShrink: 0 }}>
                    {Math.round(value)}
                  </span>
                </div>
              ))}
            </div>

            {/* Social footer */}
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.73rem', color: 'var(--text-muted)', borderTop: '1px solid var(--border-subtle)', paddingTop: '0.7rem' }}>
              <span>💖 {agent.friend_count} Friends</span>
              <span>⚔️ {agent.rival_count} Rivals</span>
              <span>🕰️ Age {agent.age_ticks}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
