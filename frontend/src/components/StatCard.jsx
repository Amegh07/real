import React from 'react';

export default function StatCard({ title, value, subtitle, color = 'var(--accent-blue)', icon, trend }) {
  const trendUp   = trend === 'up';
  const trendDown = trend === 'down';

  return (
    <div className="glass" style={{ padding: '1.4rem 1.6rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', position: 'relative', overflow: 'hidden' }}>
      {/* Background glow */}
      <div style={{
        position: 'absolute', top: -20, right: -20, width: 100, height: 100,
        background: color, borderRadius: '50%', opacity: 0.04, filter: 'blur(30px)',
        pointerEvents: 'none',
      }} />

      {/* Title row */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h3 style={{ margin: 0 }}>{title}</h3>
        {icon && <span style={{ fontSize: '1.2rem', opacity: 0.6 }}>{icon}</span>}
      </div>

      {/* Value */}
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem' }}>
        <div style={{
          fontSize: '2.2rem',
          fontWeight: 800,
          color: color,
          letterSpacing: '-0.03em',
          lineHeight: 1,
        }}>
          {value}
        </div>
        {trend && (
          <span style={{
            fontSize: '0.85rem',
            fontWeight: 700,
            color: trendUp ? 'var(--accent-green)' : trendDown ? 'var(--accent-red)' : 'var(--text-muted)',
          }}>
            {trendUp ? '↑' : trendDown ? '↓' : '→'}
          </span>
        )}
      </div>

      {subtitle && (
        <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', lineHeight: 1.4 }}>{subtitle}</div>
      )}
    </div>
  );
}
