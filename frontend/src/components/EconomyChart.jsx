import React, { useEffect, useRef } from 'react';

/**
 * SVG line chart for economy history data.
 * Renders two overlaid charts: Treasury and Inflation Rate.
 */

const W = 500;
const H = 140;
const PAD = { top: 12, right: 12, bottom: 28, left: 52 };
const INNER_W = W - PAD.left - PAD.right;
const INNER_H = H - PAD.top - PAD.bottom;

function normalize(arr) {
  const min = Math.min(...arr);
  const max = Math.max(...arr);
  const range = max - min || 1;
  return { min, max, fn: v => (v - min) / range };
}

function buildPath(points) {
  if (points.length === 0) return '';
  return points.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x},${p.y}`).join(' ');
}

function buildAreaPath(points, baseline) {
  if (points.length === 0) return '';
  const line = buildPath(points);
  return `${line} L${points[points.length-1].x},${baseline} L${points[0].x},${baseline} Z`;
}

function LineChart({ data, yKey, color, gradId, label, formatter = v => v }) {
  const vals = data.map(d => d[yKey]);
  if (vals.length < 2) return (
    <div style={{ padding: '2rem', color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center' }}>
      Collecting data… ({vals.length} ticks)
    </div>
  );

  const { min, max, fn } = normalize(vals);
  const step = INNER_W / (vals.length - 1);

  const points = vals.map((v, i) => ({
    x: PAD.left + i * step,
    y: PAD.top  + INNER_H - fn(v) * INNER_H,
  }));

  const baseline = PAD.top + INNER_H;
  const linePath = buildPath(points);
  const areaPath = buildAreaPath(points, baseline);

  // Y-axis labels (3 ticks)
  const yTicks = [min, (min + max) / 2, max];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
          {label}
        </span>
        <span style={{ fontSize: '0.82rem', color: color, fontWeight: 700 }}>
          {formatter(vals[vals.length - 1])}
        </span>
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} style={{ width: '100%', height: 'auto', display: 'block' }}>
        <defs>
          <linearGradient id={gradId} x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%"   stopColor={color} stopOpacity={0.25} />
            <stop offset="100%" stopColor={color} stopOpacity={0}    />
          </linearGradient>
        </defs>

        {/* Grid lines */}
        {yTicks.map((_, i) => {
          const y = PAD.top + (i === 0 ? INNER_H : i === 2 ? 0 : INNER_H / 2);
          return (
            <g key={i}>
              <line x1={PAD.left} y1={y} x2={PAD.left + INNER_W} y2={y}
                stroke="rgba(255,255,255,0.05)" strokeWidth={1} />
              <text x={PAD.left - 6} y={y + 4} textAnchor="end"
                fill="rgba(255,255,255,0.25)" fontSize={9} fontFamily="JetBrains Mono, monospace">
                {formatter(yTicks[2 - i])}
              </text>
            </g>
          );
        })}

        {/* Area fill */}
        <path d={areaPath} fill={`url(#${gradId})`} />

        {/* Line */}
        <path d={linePath} fill="none" stroke={color} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />

        {/* Last point dot */}
        <circle cx={points[points.length-1].x} cy={points[points.length-1].y}
          r={4} fill={color} stroke="rgba(6,13,26,0.9)" strokeWidth={2} />

        {/* X-axis label */}
        <text x={PAD.left} y={H - 4} fill="rgba(255,255,255,0.2)" fontSize={9} fontFamily="JetBrains Mono, monospace">
          T{data[0]?.tick ?? 0}
        </text>
        <text x={PAD.left + INNER_W} y={H - 4} textAnchor="end" fill="rgba(255,255,255,0.2)" fontSize={9} fontFamily="JetBrains Mono, monospace">
          T{data[data.length-1]?.tick ?? 0}
        </text>
      </svg>
    </div>
  );
}

export default function EconomyChart({ history }) {
  const data = history || [];

  return (
    <div className="glass" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <h2>Economy Charts</h2>

      <LineChart
        data={data}
        yKey="treasury"
        color="var(--accent-green)"
        gradId="grad-treasury"
        label="Global Treasury"
        formatter={v => `$${Math.round(v).toLocaleString()}`}
      />

      <hr className="divider" />

      <LineChart
        data={data}
        yKey="inflation"
        color="var(--accent-yellow)"
        gradId="grad-inflation"
        label="Inflation Rate"
        formatter={v => `${v?.toFixed ? v.toFixed(3) : v}×`}
      />

      <hr className="divider" />

      {/* Employment ratio as stacked bar */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em' }}>
            Employment Rate
          </span>
          {data.length > 0 && (
            <span style={{ fontSize: '0.82rem', color: 'var(--accent-blue)', fontWeight: 700 }}>
              {data[data.length - 1].employed}/{data[data.length - 1].population} employed
            </span>
          )}
        </div>
        {data.length > 0 && (() => {
          const last = data[data.length - 1];
          const pct = Math.round((last.employed / Math.max(last.population, 1)) * 100);
          return (
            <div>
              <div className="progress-track" style={{ height: 10, borderRadius: 5 }}>
                <div className="progress-fill" style={{ width: `${pct}%`, background: 'linear-gradient(90deg, var(--accent-blue), var(--accent-purple))', borderRadius: 5 }} />
              </div>
              <div style={{ textAlign: 'right', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 4 }}>{pct}%</div>
            </div>
          );
        })()}
      </div>
    </div>
  );
}
