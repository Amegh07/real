import React from 'react';

export default function EventTimeline({ events }) {
  if (!events || events.length === 0) return <div className="glass-panel" style={{ padding: '2rem' }}>Awaiting events...</div>;

  return (
    <div className="glass-panel" style={{ padding: '1.5rem', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.8rem', marginBottom: '1rem' }}>Global Ledger</h3>
      <div style={{ overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.6rem', flex: 1, paddingRight: '0.5rem' }}>
        {events.map((ev, i) => {
            // Regex to parse the "[TXX] " prefix gracefully
            const match = ev.match(/^\[T(\d+)\]\s*(.*)/);
            if (!match) return <div key={i} style={{ fontSize: '0.85rem' }}>{ev}</div>;
            
            const tick = match[1];
            const text = match[2];
            
            let color = 'var(--text-main)';
            let borderColor = 'var(--border-subtle)';
            if (text.includes('[ALERT]')) {
                color = 'var(--accent-red)'; borderColor = 'var(--accent-red)';
            } else if (text.includes('🗣️')) {
                color = 'var(--accent-purple)'; borderColor = 'var(--accent-purple)';
            } else if (text.includes('Economy')) {
                borderColor = 'var(--accent-green)';
            }

            return (
              <div key={i} style={{ 
                  fontSize: '0.85rem', 
                  padding: '0.6rem', 
                  background: 'rgba(255,255,255,0.02)', 
                  borderRadius: '6px', 
                  borderLeft: `3px solid ${borderColor}`,
                  lineHeight: '1.4'
              }}>
                <span style={{ color: 'var(--text-muted)', marginRight: '0.6rem', fontWeight: 'bold' }}>T{tick}</span>
                <span style={{ color: color }}>{text}</span>
              </div>
            );
        })}
      </div>
    </div>
  );
}
