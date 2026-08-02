import { StrictMode, Component } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

// Catches React render-time errors that window.onerror can miss - same
// temporary debug purpose as the listeners below, safe to remove once
// the root cause is found.
class DebugErrorBoundary extends Component<{ children: React.ReactNode }, { hasError: boolean; message: string }> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, message: '' };
  }
  static getDerivedStateFromError(error: any) {
    return { hasError: true, message: `${error?.message || error}\n${error?.stack || ''}` };
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ position: 'fixed', inset: 0, zIndex: 999999, background: '#b91c1c', color: '#fff', padding: 16, fontSize: 13, fontFamily: 'monospace', whiteSpace: 'pre-wrap', overflow: 'auto' }}>
          [React render error] {this.state.message}
        </div>
      );
    }
    return this.props.children;
  }
}

// Temporary on-screen error display for tracking down a black-screen bug
// that isn't showing up in Safari's Web Inspector console. Shows the real
// error text directly on the device, no inspector connection needed.
// Safe to remove once the root cause is found.
function showOnScreenError(label: string, message: string) {
  let box = document.getElementById('debug-error-box');
  if (!box) {
    box = document.createElement('div');
    box.id = 'debug-error-box';
    box.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999999;background:#b91c1c;color:#fff;padding:16px;font-size:13px;font-family:monospace;white-space:pre-wrap;max-height:80vh;overflow:auto;';
    document.body.appendChild(box);
  }
  const entry = document.createElement('div');
  entry.style.cssText = 'margin-bottom:12px;border-bottom:1px solid rgba(255,255,255,0.3);padding-bottom:12px;';
  entry.textContent = `[${label}] ${message}`;
  box.appendChild(entry);
}

window.addEventListener('error', (event) => {
  showOnScreenError('error', `${event.message}\n${event.error?.stack || ''}`);
});

window.addEventListener('unhandledrejection', (event) => {
  showOnScreenError('unhandled promise rejection', String(event.reason?.stack || event.reason));
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <DebugErrorBoundary>
      <App />
    </DebugErrorBoundary>
  </StrictMode>,
)
