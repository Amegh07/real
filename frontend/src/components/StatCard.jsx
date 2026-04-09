import React from 'react';

export default function StatCard({ title, value, subtitle, color = 'var(--accent-blue)' }) {
  return (
    <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
      <h3 style={{ margin: 0 }}>{title}</h3>
      <div style={{ fontSize: '2.5rem', fontWeight: '700', color: color }}>
        {value}
      </div>
      {subtitle && <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>{subtitle}</div>}
    </div>
  );
}
