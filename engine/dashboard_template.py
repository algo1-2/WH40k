"""
WH40K TACTICAL COMMAND COGITATOR — WEB DASHBOARD TEMPLATE v10.0
Master High-Immersion & Deep Chat-Sync Suite:
- Continuous Live Ticking Imperial Chrono-Clock (Seconds, Minutes, Hours, Turns)
- Red Alert / Defense Lockdown Mode with visual sirens & battle station deployments
- Live ChatGPT Narrative Importer & Fast Parser (Paste roleplay text -> Moves characters, shows dialogues, updates clock & logs)
- Full Turn Report Generator (1-Click Markdown Report for ChatGPT)
- Canonical ChatGPT Prompt Generator with 1-Click Clipboard Copying
- Interactive Anatomical Patient Trauma Monitor (Zonal wounds: Head, Chest, Abdomen, Limbs)
- Expanded 10-Procedure Surgery Suite & 9-Formula Clandestine Alchemy Lab
- Khepra-9 Cybernetics & Bionic Prosthesis Forge
- Clandestine Contracts Board & Dust Falls Black Market Bazaar
- Retinue Tactical Weapon Loadout Manager
- Active ChatGPT Sync Bridge & Real-Time Animated Tactical Motion Map
"""

def get_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WH40K // COGITADOR TÁCTICO DE CAMPAÑA</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800;900&family=JetBrains+Mono:ital,wght@0,300;0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-deep: #080a0d;
      --bg-card: #0f1318;
      --bg-card-hover: #161b22;
      --border-panel: #262e3b;
      --border-accent: #c99a3e;
      --brass: #c99a3e;
      --brass-dim: #8c6b2b;
      --amber: #f59e0b;
      --amber-glow: rgba(245, 158, 11, 0.25);
      --crimson: #991b1b;
      --crimson-light: #ef4444;
      --green-auspex: #10b981;
      --cyan-plasma: #06b6d4;
      --text-main: #e2e8f0;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --shadow-box: 0 4px 20px rgba(0, 0, 0, 0.6);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg-deep);
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      line-height: 1.5;
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(201, 154, 62, 0.05), transparent 60%),
        linear-gradient(to bottom, rgba(8, 10, 13, 0.95), rgba(8, 10, 13, 1));
      transition: background-color 0.4s ease;
    }

    body.red-alert-active {
      background-color: #120606;
      background-image: 
        radial-gradient(circle at 50% 0%, rgba(239, 68, 68, 0.15), transparent 70%),
        linear-gradient(to bottom, rgba(18, 6, 6, 0.95), rgba(18, 6, 6, 1));
    }

    header {
      background: #0b0e12;
      border-bottom: 2px solid var(--brass-dim);
      padding: 0.75rem 1.5rem;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      box-shadow: 0 2px 15px rgba(0, 0, 0, 0.7);
    }

    body.red-alert-active header {
      border-bottom-color: var(--crimson-light);
      box-shadow: 0 2px 20px rgba(239, 68, 68, 0.3);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }

    .aquila-icon {
      font-size: 1.8rem;
      color: var(--brass);
      text-shadow: 0 0 10px var(--amber-glow);
    }

    .brand-title {
      font-family: 'Cinzel', serif;
      font-size: 1.2rem;
      font-weight: 900;
      letter-spacing: 2px;
      color: var(--brass);
      text-transform: uppercase;
    }

    .brand-sub {
      font-size: 0.7rem;
      color: var(--text-dim);
      letter-spacing: 1px;
    }

    /* REAL-TIME IMPERIAL CHRONO CLOCK */
    .chrono-clock-box {
      background: #06090d;
      border: 1px solid var(--border-panel);
      padding: 0.4rem 0.85rem;
      border-radius: 4px;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
    }

    .chrono-display {
      display: flex;
      flex-direction: column;
    }

    .chrono-time {
      font-size: 0.88rem;
      font-weight: 800;
      color: var(--brass);
      letter-spacing: 1.5px;
      font-variant-numeric: tabular-nums;
    }

    .chrono-sub {
      font-size: 0.68rem;
      color: var(--text-dim);
    }

    .btn-header-action {
      background: #161d28;
      border: 1px solid var(--brass-dim);
      color: var(--brass);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.35rem 0.65rem;
      border-radius: 3px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }

    .btn-header-action:hover {
      background: var(--brass);
      color: #080a0d;
      box-shadow: 0 0 10px var(--amber-glow);
    }

    .btn-red-alert {
      background: #2a0808;
      border: 1px solid var(--crimson-light);
      color: #fca5a5;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      font-weight: 800;
      padding: 0.4rem 0.85rem;
      border-radius: 4px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.25s ease;
    }

    .btn-red-alert:hover, .btn-red-alert.active {
      background: var(--crimson-light);
      color: #080a0d;
      box-shadow: 0 0 15px rgba(239, 68, 68, 0.6);
      animation: alertPulse 1.5s infinite;
    }

    @keyframes alertPulse {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.8; transform: scale(0.97); }
      100% { opacity: 1; transform: scale(1); }
    }

    .status-badge-container {
      display: flex;
      gap: 0.6rem;
      align-items: center;
      flex-wrap: wrap;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.35rem 0.75rem;
      font-size: 0.75rem;
      font-weight: 600;
      border-radius: 4px;
      background: #141820;
      border: 1px solid var(--border-panel);
    }

    .badge-live {
      border-color: var(--green-auspex);
      color: var(--green-auspex);
    }

    .badge-live::before {
      content: "";
      width: 8px;
      height: 8px;
      background: var(--green-auspex);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--green-auspex);
      animation: pulse 2s infinite;
    }

    .badge-brass {
      border-color: var(--brass-dim);
      color: var(--brass);
    }

    .badge-green {
      border-color: var(--green-auspex);
      color: var(--green-auspex);
    }

    @keyframes pulse {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
      100% { opacity: 1; transform: scale(1); }
    }

    /* LIVE CHAT EVENT TICKER */
    .chat-ticker-bar {
      background: #090d13;
      border-bottom: 1px solid var(--border-panel);
      padding: 0.4rem 1.5rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-size: 0.75rem;
      overflow: hidden;
      white-space: nowrap;
    }

    .ticker-label {
      background: var(--brass-dim);
      color: #080a0d;
      font-weight: 800;
      padding: 0.15rem 0.5rem;
      border-radius: 3px;
      font-size: 0.68rem;
      letter-spacing: 1px;
    }

    .ticker-text {
      color: var(--text-main);
      overflow: hidden;
      text-overflow: ellipsis;
    }

    nav.tab-nav {
      background: #0d1015;
      display: flex;
      overflow-x: auto;
      border-bottom: 1px solid var(--border-panel);
      padding: 0 1.5rem;
      gap: 0.5rem;
    }

    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      font-weight: 600;
      padding: 0.75rem 1.15rem;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s ease;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .tab-btn:hover {
      color: var(--text-main);
      background: rgba(201, 154, 62, 0.05);
    }

    .tab-btn.active {
      color: var(--brass);
      border-bottom: 2px solid var(--brass);
      background: rgba(201, 154, 62, 0.08);
    }

    main.container {
      flex: 1;
      padding: 1.5rem;
      max-width: 1400px;
      margin: 0 auto;
      width: 100%;
    }

    .tab-content {
      display: none;
    }

    .tab-content.active {
      display: block;
      animation: fadeIn 0.25s ease-in-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .grid-dashboard {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1.5rem;
      margin-bottom: 1.5rem;
    }

    .panel {
      background: var(--bg-card);
      border: 1px solid var(--border-panel);
      border-radius: 6px;
      overflow: hidden;
      box-shadow: var(--shadow-box);
      transition: border-color 0.2s ease;
    }

    .panel:hover {
      border-color: #3b4656;
    }

    .panel-header {
      background: #131820;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-panel);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .panel-title {
      font-family: 'Cinzel', serif;
      font-size: 0.95rem;
      font-weight: 800;
      color: var(--brass);
      letter-spacing: 1px;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .panel-body {
      padding: 1rem;
    }

    .stat-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 0.85rem;
    }

    .stat-row:last-child {
      border-bottom: none;
    }

    .stat-label {
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .stat-val {
      font-weight: 700;
      color: var(--text-main);
    }

    .stat-val.brass { color: var(--brass); }
    .stat-val.green { color: var(--green-auspex); }
    .stat-val.amber { color: var(--amber); }
    .stat-val.crimson { color: var(--crimson-light); }
    .stat-val.cyan { color: var(--cyan-plasma); }

    .progress-bar-bg {
      width: 100%;
      height: 8px;
      background: #1e2430;
      border-radius: 4px;
      overflow: hidden;
      margin-top: 0.35rem;
    }

    .progress-fill {
      height: 100%;
      border-radius: 4px;
      transition: width 0.4s ease;
    }

    .fill-green { background: var(--green-auspex); }
    .fill-amber { background: var(--amber); }
    .fill-brass { background: var(--brass); }
    .fill-crimson { background: var(--crimson-light); }
    .fill-cyan { background: var(--cyan-plasma); }

    /* BLUEPRINT & FLOORS */
    .floor-controls {
      display: flex;
      gap: 0.75rem;
      margin-bottom: 1rem;
      align-items: center;
      flex-wrap: wrap;
    }

    .floor-btn {
      background: #131822;
      border: 1px solid var(--border-panel);
      color: var(--text-muted);
      font-family: 'Cinzel', serif;
      font-weight: 800;
      font-size: 0.82rem;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s ease;
      letter-spacing: 0.5px;
    }

    .floor-btn.active, .floor-btn:hover {
      background: rgba(201, 154, 62, 0.15);
      color: var(--brass);
      border-color: var(--brass);
      box-shadow: 0 0 10px rgba(201, 154, 62, 0.2);
    }

    .blueprint-metrics-bar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .blueprint-grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    @media (max-width: 1024px) {
      .blueprint-grid { grid-template-columns: repeat(6, 1fr); }
    }
    @media (max-width: 640px) {
      .blueprint-grid { grid-template-columns: 1fr; }
    }

    .room-card {
      background: #0d1117;
      border: 1px solid #2d3748;
      border-radius: 6px;
      padding: 1rem;
      cursor: pointer;
      position: relative;
      transition: all 0.25s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 140px;
    }

    .room-card:hover {
      border-color: var(--brass);
      background: #141a24;
      transform: translateY(-2px);
      box-shadow: 0 4px 15px rgba(201, 154, 62, 0.2);
    }

    .room-card.fog-of-war {
      border-style: dashed;
      border-color: #3b4252;
      background: repeating-linear-gradient(
        45deg,
        #0a0d12,
        #0a0d12 10px,
        #0e131a 10px,
        #0e131a 20px
      );
    }

    .room-code-tag {
      font-size: 0.7rem;
      font-weight: 700;
      color: var(--brass-dim);
      letter-spacing: 1px;
    }

    .room-name {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-main);
      margin: 0.25rem 0;
    }

    .room-level-badge {
      font-size: 0.7rem;
      display: inline-block;
      padding: 0.15rem 0.45rem;
      border-radius: 3px;
      background: #1e2530;
      color: var(--brass);
      font-weight: 600;
      margin-top: 0.25rem;
    }

    .room-occupants-mini {
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-top: 0.5rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .room-status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
      margin-right: 0.35rem;
    }

    /* ENHANCED HD MOTION RADAR STYLES */
    .radar-container-layout {
      display: grid;
      grid-template-columns: 2fr 1.2fr;
      gap: 1.5rem;
    }

    @media (max-width: 960px) {
      .radar-container-layout { grid-template-columns: 1fr; }
    }

    .radar-canvas-box {
      background: #040608;
      border: 2px solid var(--border-panel);
      border-radius: 6px;
      position: relative;
      overflow: hidden;
      box-shadow: inset 0 0 35px rgba(0,0,0,0.95), 0 0 20px rgba(16, 185, 129, 0.15);
      min-height: 520px;
    }

    #radarCanvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    .radar-scanline {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(rgba(16, 185, 129, 0) 50%, rgba(16, 185, 129, 0.05) 50%);
      background-size: 100% 4px;
      pointer-events: none;
    }

    .radar-sidebar {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .chat-sync-box {
      background: #0b0f16;
      border: 1px solid var(--brass-dim);
      border-radius: 6px;
      padding: 1rem;
      box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }

    .quick-orders-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.45rem;
      margin-top: 0.6rem;
    }

    .btn-quick-order {
      background: #131923;
      border: 1px solid var(--border-panel);
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.7rem;
      padding: 0.45rem 0.55rem;
      border-radius: 4px;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .btn-quick-order:hover {
      background: rgba(201, 154, 62, 0.2);
      border-color: var(--brass);
      color: var(--brass);
      transform: translateY(-1px);
    }

    .agent-tracker-card {
      background: #111620;
      border: 1px solid var(--border-panel);
      border-radius: 4px;
      padding: 0.65rem 0.85rem;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .agent-tracker-card:hover, .agent-tracker-card.active {
      border-color: var(--green-auspex);
      background: #16202c;
      transform: translateX(3px);
    }

    .agent-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text-main);
    }

    .agent-task {
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-top: 0.2rem;
    }

    /* ANATOMICAL PATIENT MONITOR STYLES */
    .anatomy-zone-card {
      background: #0d121a;
      border: 1px solid var(--border-panel);
      border-radius: 4px;
      padding: 0.6rem 0.8rem;
      margin-bottom: 0.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.2s ease;
    }

    .anatomy-zone-card:hover {
      border-color: var(--brass-dim);
      background: #131a24;
    }

    /* CHAT PROMPT COPIER BOX */
    .prompt-copier-box {
      background: #0a0e14;
      border: 1px solid var(--brass-dim);
      border-radius: 6px;
      padding: 0.85rem 1rem;
      box-shadow: 0 4px 15px rgba(0,0,0,0.6);
      position: relative;
    }

    .prompt-text-pre {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.75rem;
      color: #93c5fd;
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.5;
    }

    .btn-copy-prompt {
      background: var(--brass-dim);
      color: #080a0d;
      font-family: 'Cinzel', serif;
      font-size: 0.75rem;
      font-weight: 800;
      border: none;
      padding: 0.35rem 0.75rem;
      border-radius: 3px;
      cursor: pointer;
      transition: all 0.2s ease;
      margin-top: 0.5rem;
    }

    .btn-copy-prompt:hover {
      background: var(--brass);
      box-shadow: 0 0 10px var(--amber-glow);
    }

    /* Modal / Drawer for Room Details */
    .room-detail-modal {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }

    .room-detail-content {
      background: #0f1319;
      border: 2px solid var(--brass);
      border-radius: 8px;
      max-width: 650px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      padding: 1.5rem;
      box-shadow: 0 0 30px rgba(201, 154, 62, 0.3);
      position: relative;
    }

    .modal-close-btn {
      position: absolute;
      top: 1rem;
      right: 1rem;
      background: transparent;
      border: none;
      color: var(--text-dim);
      font-size: 1.5rem;
      cursor: pointer;
    }

    .modal-close-btn:hover { color: var(--crimson-light); }

    .upgrade-box {
      background: #141923;
      border: 1px solid var(--brass-dim);
      border-radius: 6px;
      padding: 1rem;
      margin-top: 1rem;
    }

    .btn-upgrade-action {
      background: linear-gradient(135deg, #a87d2b, #c99a3e);
      color: #080a0d;
      border: none;
      font-family: 'Cinzel', serif;
      font-size: 0.85rem;
      font-weight: 900;
      padding: 0.6rem 1.25rem;
      border-radius: 4px;
      cursor: pointer;
      letter-spacing: 1px;
      text-transform: uppercase;
      transition: all 0.2s ease;
      width: 100%;
      margin-top: 0.75rem;
    }

    .btn-upgrade-action:hover {
      background: linear-gradient(135deg, #c99a3e, #f59e0b);
      box-shadow: 0 0 15px var(--amber-glow);
    }

    .btn-explore-action {
      background: linear-gradient(135deg, #0284c7, #06b6d4);
      color: #080a0d;
      border: none;
      font-family: 'Cinzel', serif;
      font-size: 0.85rem;
      font-weight: 900;
      padding: 0.6rem 1.25rem;
      border-radius: 4px;
      cursor: pointer;
      letter-spacing: 1px;
      text-transform: uppercase;
      transition: all 0.2s ease;
      width: 100%;
      margin-top: 0.75rem;
    }

    /* Staff & Feed */
    .staff-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
      margin-top: 0.5rem;
    }

    .staff-table th, .staff-table td {
      padding: 0.6rem 0.75rem;
      border-bottom: 1px solid var(--border-panel);
      text-align: left;
    }

    .staff-table th {
      color: var(--brass);
      font-weight: 700;
      background: #111620;
    }

    .staff-select {
      background: #10141b;
      border: 1px solid var(--border-panel);
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      padding: 0.35rem 0.6rem;
      border-radius: 4px;
      font-size: 0.78rem;
      width: 100%;
    }

    .terminal-feed {
      background: #080b0f;
      border: 1px solid var(--border-panel);
      border-radius: 4px;
      padding: 0.85rem;
      max-height: 220px;
      overflow-y: auto;
      font-size: 0.78rem;
      line-height: 1.5;
    }

    .feed-entry {
      margin-bottom: 0.4rem;
      padding-bottom: 0.4rem;
      border-bottom: 1px dashed rgba(255, 255, 255, 0.05);
    }

    .feed-time { color: var(--brass-dim); margin-right: 0.5rem; }
    .feed-tag { font-weight: 700; margin-right: 0.5rem; }
    .feed-tag.SECURITY { color: var(--green-auspex); }
    .feed-tag.UPGRADE { color: var(--amber); }
    .feed-tag.EXPLORATION { color: var(--cyan-plasma); }
    .feed-tag.MEDICAL { color: var(--crimson-light); }
    .feed-tag.COSECHA { color: var(--brass); }

    /* FORMS & BUTTONS */
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
      margin-bottom: 0.85rem;
    }

    .form-label {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--brass);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .form-control {
      background: #10141b;
      border: 1px solid var(--border-panel);
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      padding: 0.6rem 0.8rem;
      border-radius: 4px;
      font-size: 0.85rem;
    }

    .form-control:focus {
      outline: none;
      border-color: var(--brass);
    }

    .btn-action-primary {
      background: linear-gradient(135deg, #a87d2b, #c99a3e);
      color: #080a0d;
      border: none;
      font-family: 'Cinzel', serif;
      font-size: 0.95rem;
      font-weight: 900;
      padding: 0.75rem 1.5rem;
      border-radius: 4px;
      cursor: pointer;
      letter-spacing: 1px;
      text-transform: uppercase;
      transition: all 0.2s ease;
      box-shadow: 0 4px 15px rgba(201, 154, 62, 0.3);
      width: 100%;
    }

    .btn-action-primary:hover {
      background: linear-gradient(135deg, #c99a3e, #f59e0b);
      box-shadow: 0 4px 20px rgba(245, 158, 11, 0.5);
      transform: translateY(-1px);
    }

    .btn-synth {
      background: #131924;
      border: 1px solid var(--brass-dim);
      color: var(--brass);
      font-family: 'Cinzel', serif;
      font-weight: 700;
      font-size: 0.75rem;
      padding: 0.4rem 0.75rem;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .btn-synth:hover {
      background: var(--brass);
      color: #080a0d;
    }

    .char-card {
      background: #131821;
      border: 1px solid #1f2733;
      border-radius: 4px;
      padding: 0.75rem;
      margin-bottom: 0.75rem;
    }

    .char-card:last-child { margin-bottom: 0; }

    .char-card-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--brass);
      margin-bottom: 0.25rem;
    }

    .char-role {
      font-size: 0.75rem;
      color: var(--text-dim);
      margin-bottom: 0.35rem;
    }

    .char-status {
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    .filter-bar {
      display: flex;
      gap: 0.75rem;
      margin-bottom: 1rem;
      flex-wrap: wrap;
    }

    .search-input {
      flex: 1;
      min-width: 240px;
      background: #10141b;
      border: 1px solid var(--border-panel);
      color: var(--text-main);
      font-family: 'JetBrains Mono', monospace;
      padding: 0.6rem 0.9rem;
      border-radius: 4px;
      font-size: 0.85rem;
    }

    .inv-category-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }

    .inv-item-card {
      background: #11151d;
      border: 1px solid var(--border-panel);
      border-radius: 4px;
      padding: 0.85rem;
      transition: all 0.2s ease;
    }

    .inv-item-card:hover {
      border-color: var(--brass-dim);
      background: #141923;
      transform: translateY(-2px);
    }

    .inv-item-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--brass);
      margin-bottom: 0.35rem;
      display: flex;
      justify-content: space-between;
    }

    .inv-item-detail {
      font-size: 0.75rem;
      color: var(--text-muted);
    }

    .doc-selector {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 1rem;
    }

    .doc-btn {
      background: #131822;
      border: 1px solid var(--border-panel);
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.8rem;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .doc-btn.active, .doc-btn:hover {
      background: rgba(201, 154, 62, 0.15);
      color: var(--brass);
      border-color: var(--brass);
    }

    .doc-viewer-area {
      background: #090c10;
      border: 1px solid var(--border-panel);
      border-radius: 4px;
      padding: 1.25rem;
      max-height: 550px;
      overflow-y: auto;
      font-size: 0.82rem;
      white-space: pre-wrap;
      word-break: break-word;
      color: #cbd5e1;
      line-height: 1.6;
    }

    footer {
      background: #080a0d;
      border-top: 1px solid var(--border-panel);
      padding: 1rem 1.5rem;
      text-align: center;
      font-size: 0.75rem;
      color: var(--text-dim);
    }

    .footer-highlight { color: var(--brass); }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <span class="aquila-icon">⚜</span>
      <div>
        <div class="brand-title">WH40K // COGITADOR TÁCTICO</div>
        <div class="brand-sub">MEDICAE STATION RHO-9 · SUBMUNDO DE NECROMUNDA</div>
      </div>
    </div>

    <!-- LIVE CONTINUOUS TICKING CHRONO CLOCK -->
    <div class="chrono-clock-box">
      <span style="font-size:1.2rem;">⏱️</span>
      <div class="chrono-display">
        <div class="chrono-time" id="chrono-clock-time">DÍA 04 · NOCHE 23:54:00</div>
        <div class="chrono-sub" id="chrono-clock-turn">TURNO 918 · VIGILIA NOCTURNA RHO-9</div>
      </div>
      <button class="btn-header-action" onclick="advanceCycleHour()" title="Avanza 1 hora/turno en la base">+1 HORA</button>
    </div>

    <div style="display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap;">
      <button class="btn-header-action" onclick="fetchFullTurnReport()" title="Genera el reporte de estado completo del turno">📡 REPORTE DE TURNO</button>
      <button class="btn-header-action" onclick="fetchHudStandard()" title="Genera el estándar mandatorio de HUD y Telemetría para ChatGPT">📊 ESTÁNDAR HUD CHAT</button>
      <button class="btn-header-action" onclick="fetchTimeDirective()" title="Genera la directiva de tiempo para ChatGPT">⏱️ DIRECTIVA DE TIEMPO</button>
      <button class="btn-red-alert" id="btn-red-alert-toggle" onclick="toggleRedAlert()">🚨 ALERTA ROJA</button>
    </div>

    <div class="status-badge-container">
      <div class="badge badge-live">API EN LÍNEA</div>
      <div class="badge badge-green" id="badge-credits">1.046 ¤ DISPONIBLES</div>
      <div class="badge badge-brass" id="badge-souls">10 ALMAS</div>
    </div>
  </header>

  <!-- PERSISTENT CANONICAL HUD STATUS BAR -->
  <div style="background:#090d14; border-bottom:1px solid var(--border-panel); padding:0.4rem 1.5rem; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:0.75rem; font-size:0.75rem;">
    <div style="display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap;">
      <span style="color:var(--brass); font-weight:800;">👤 ALEXANDER:</span>
      <span class="stat-val green" id="hud-alex-hp">❤️ 12/12 PV</span>
      <span class="stat-val" id="hud-alex-fatigue">⚡ 0/7 Fatiga</span>
      <span class="stat-val brass" id="hud-alex-souls">🔮 10 Almas</span>
      <span class="stat-val green" id="hud-alex-credits">💰 1.046 ¤</span>
      <span class="stat-val" style="color:var(--cyan-plasma);">🌟 3 Destino</span>
    </div>
    <div style="display:flex; align-items:center; gap:0.8rem; flex-wrap:wrap;">
      <span style="color:var(--brass);">📍 SECTOR:</span>
      <span class="stat-val" id="hud-alex-location" style="color:var(--text-main);">C-01 // Medicae Station Rho-9</span>
      <span style="color:var(--brass);">🛡️ BASE:</span>
      <span class="stat-val green">75% Def · 70% San · 80% Red</span>
    </div>
  </div>

  <!-- NARRATIVE CHAT TICKER -->
  <div class="chat-ticker-bar">
    <span class="ticker-label">TRANSMISIÓN CHAT</span>
    <span class="ticker-text" id="live-chat-ticker">Alexander mantiene la perfusión tisular activa en C-03 mientras Severan custodia la compuerta.</span>
  </div>

  <nav class="tab-nav">
    <button class="tab-btn active" onclick="switchTab('tab-blueprint')">🗺️ PLANO & MEJORAS</button>
    <button class="tab-btn" onclick="switchTab('tab-radar')">📡 RADAR & MOVIMIENTO</button>
    <button class="tab-btn" onclick="switchTab('tab-medicae')">🩸 CIRUGÍA & BIÓNICA</button>
    <button class="tab-btn" onclick="switchTab('tab-alchemy')">⚗️ FARMACOLOGÍA</button>
    <button class="tab-btn" onclick="switchTab('tab-factions')">⚖️ FACCIONES & MERCADO</button>
    <button class="tab-btn" onclick="switchTab('tab-status')">⚙️ ESTADO & SÉQUITO</button>
    <button class="tab-btn" onclick="switchTab('tab-inventory')">📦 SOMBRA INFINITA</button>
    <button class="tab-btn" onclick="switchTab('tab-roller')">🎲 SIMULADOR d100</button>
    <button class="tab-btn" onclick="switchTab('tab-docs')">📜 DOSSIERS</button>
  </nav>

  <main class="container">

    <!-- GLOBAL CHAT PROMPT COPIER BAR (WHEN AN ACTION IS GENERATED) -->
    <div id="global-prompt-card" class="prompt-copier-box" style="display:none; margin-bottom:1.5rem; border-color:var(--green-auspex);">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-family:'Cinzel',serif; font-size:0.85rem; font-weight:800; color:var(--green-auspex);">📋 PROMPT CANÓNICO LISTO PARA CHATGPT</span>
        <button class="btn-copy-prompt" onclick="copyCanonicalPrompt()">📋 COPIAR AL PORTAPAPELES</button>
      </div>
      <pre id="global-prompt-content" class="prompt-text-pre" style="margin-top:0.5rem;"></pre>
    </div>

    <!-- TAB 0: BLUEPRINT & BASE UPGRADES -->
    <section id="tab-blueprint" class="tab-content active">
      <div class="blueprint-metrics-bar">
        <div class="panel" style="padding:1rem;">
          <div class="stat-label">🛡️ Fortaleza Perimetral</div>
          <div class="stat-val brass" id="metric-defensa" style="font-size:1.2rem; margin-top:0.25rem;">75%</div>
          <div class="progress-bar-bg"><div class="progress-fill fill-brass" id="bar-defensa" style="width: 75%;"></div></div>
        </div>
        <div class="panel" style="padding:1rem;">
          <div class="stat-label">🧼 Calidad Sanitaria</div>
          <div class="stat-val amber" id="metric-sanidad" style="font-size:1.2rem; margin-top:0.25rem;">70%</div>
          <div class="progress-bar-bg"><div class="progress-fill fill-amber" id="bar-sanidad" style="width: 70%;"></div></div>
        </div>
        <div class="panel" style="padding:1rem;">
          <div class="stat-label">⚡ Red Eléctrica (Plasma)</div>
          <div class="stat-val green" style="font-size:1.2rem; margin-top:0.25rem;">80%</div>
          <div class="progress-bar-bg"><div class="progress-fill fill-green" style="width: 80%;"></div></div>
        </div>
        <div class="panel" style="padding:1rem;">
          <div class="stat-label">🛏️ Ocupación Camas / Cuartos</div>
          <div class="stat-val cyan" style="font-size:1.2rem; margin-top:0.25rem;">2 / 3 Camas · 3 / 4 Cuartos</div>
          <div class="progress-bar-bg"><div class="progress-fill fill-cyan" style="width: 70%;"></div></div>
        </div>
      </div>

      <div class="panel" style="margin-bottom:1.5rem;">
        <div class="panel-header">
          <div class="panel-title">
            <span>🗺️ AUSPEX ARQUITECTÓNICO // </span>
            <span id="current-floor-title" style="color:var(--text-main); font-size:0.85rem;">PLANTA 0 (CLÍNICA)</span>
          </div>
          <div class="floor-controls">
            <button class="floor-btn active" id="btn-floor-0" onclick="changeFloor(0)">📍 PLANTA 0: CLÍNICA</button>
            <button class="floor-btn" id="btn-floor-sub1" onclick="changeFloor(-1)">🌑 SUBNIVEL -1: CRIPTAS</button>
          </div>
        </div>
        <div class="panel-body">
          <div class="blueprint-grid" id="blueprint-grid-container"></div>
        </div>
      </div>

      <div class="grid-dashboard">
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">👥 ASIGNACIÓN TÁCTICA DE SÉQUITO</span>
          </div>
          <div class="panel-body">
            <table class="staff-table">
              <thead>
                <tr><th>Operador / PNJ</th><th>Puesto Asignado</th></tr>
              </thead>
              <tbody>
                <tr><td><strong>Severan Holt</strong></td><td><select class="staff-select" onchange="assignStaff('Severan Holt', this.value)"><option>Mando de Guardia & Seguridad</option><option>Rondas Nocturnas</option><option>Escolta de Exploración</option></select></td></tr>
                <tr><td><strong>Khepra-9</strong></td><td><select class="staff-select" onchange="assignStaff('Khepra-9', this.value)"><option>Taller Mecatrónico T-01</option><option>Mantenimiento de Plasma</option><option>Fabricación Protésica</option></select></td></tr>
                <tr><td><strong>Syra Kol (16a)</strong></td><td><select class="staff-select" onchange="assignStaff('Syra Kol', this.value)"><option>Contabilidad & Farmacia ADM-01</option><option>Intercepción Vox</option><option>Triaje de Consumibles</option></select></td></tr>
                <tr><td><strong>Jarek Venn</strong></td><td><select class="staff-select" onchange="assignStaff('Jarek Venn', this.value)"><option>Centinela en Compuerta GATE-01</option><option>Trabajos de Carga Pesada</option><option>Escolta de Guardia</option></select></td></tr>
                <tr><td><strong>Halven Rusk</strong></td><td><select class="staff-select" onchange="assignStaff('Halven Rusk', this.value)"><option>Auxiliar de Quirófano Q-01</option><option>Cosecha y Triaje Vigilado</option><option>Limpieza de Residuos</option></select></td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">📟 CRÓNICA & TELEMETRÍA DE RHO-9</span>
            <span class="badge badge-brass">LOG EN VIVO</span>
          </div>
          <div class="panel-body">
            <div class="terminal-feed" id="telemetry-feed-container"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 1: ENHANCED HD MOTION RADAR & CHAT BRIDGE -->
    <section id="tab-radar" class="tab-content">
      <div class="panel" style="margin-bottom:1rem;">
        <div class="panel-header">
          <div class="panel-title">
            <span>📡 AUSPEX TÁCTICO // RADAR DE MOVIMIENTO EN VIVO & ENLACE DE CHAT</span>
          </div>
          <div style="display:flex; gap:0.5rem; align-items:center;">
            <span class="badge badge-live">SEGUIMIENTO ACTIVO</span>
            <span class="badge badge-brass" id="radar-agent-count">8 AGENTES</span>
          </div>
        </div>
        <div class="panel-body">
          <div class="radar-container-layout">
            
            <div class="radar-canvas-box">
              <canvas id="radarCanvas" width="760" height="500"></canvas>
              <div class="radar-scanline"></div>
            </div>
            
            <div class="radar-sidebar">
              
              <!-- CHATGPT LIVE NARRATIVE IMPORTER / FAST PARSER -->
              <div class="chat-sync-box" style="border-color:var(--cyan-plasma);">
                <div style="font-family:'Cinzel',serif; font-size:0.85rem; font-weight:800; color:var(--cyan-plasma); display:flex; justify-content:space-between; align-items:center;">
                  <span>📥 IMPORTAR NARRATIVA DE CHATGPT</span>
                  <span class="badge badge-live" style="font-size:0.65rem; padding:0.15rem 0.4rem;">PARSER</span>
                </div>
                <p style="font-size:0.7rem; color:var(--text-muted); margin:0.35rem 0 0.5rem 0;">
                  Pega cualquier texto o respuesta del rol en ChatGPT. El cogitador extraerá automáticamente personajes, diálogos y los moverá en el radar.
                </p>
                <textarea id="narrative-import-input" class="form-control" style="font-size:0.75rem; height:65px; resize:none;" placeholder="Ej: Severan avanza a la compuerta y grita '¡Cerrojos listos!' mientras Alexander supervisa el quirófano..."></textarea>
                <button class="btn-synth" style="margin-top:0.4rem; width:100%; border-color:var(--cyan-plasma); color:var(--cyan-plasma);" onclick="importChatNarrative()">⚡ PROCESAR Y MOVER AGENTES EN EL MAPA</button>
              </div>

              <!-- QUICK ORDER CONSOLE -->
              <div class="chat-sync-box">
                <div style="font-family:'Cinzel',serif; font-size:0.85rem; font-weight:800; color:var(--brass); display:flex; justify-content:space-between; align-items:center;">
                  <span>💬 CONSOLA DE ENLACE RÁPIDO</span>
                  <span class="badge badge-live" style="font-size:0.65rem; padding:0.15rem 0.4rem;">SYNC</span>
                </div>
                
                <div class="quick-orders-grid">
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Severan Holt', 'GATE-01', 'Inspección de cerrojos y guardia en compuerta principal')">🛡️ Severan a Compuerta</button>
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Severan Holt', 'COMM-01', 'Ronda nocturna por sala común')">🌙 Severan Ronda Comedor</button>
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Khepra-9', 'E-01', 'Calibración de circuito aséptico en esterilización')">⚙️ Khepra a Filtros</button>
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Khepra-9', 'T-01', 'Supervisión de generador de plasma en T-01')">⚡ Khepra a Plasma</button>
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Alexander', 'Q-01', 'Revisión quirúrgica y signos vitales')">👤 Alex a Quirófano</button>
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Alexander', 'HAB-01', 'Meditación y canalización de almas en Sanctum')">🔮 Alex a Sanctum</button>
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Syra Kol', 'F-02', 'Auditoría de estimulantes y biobanco')">📋 Syra a Farmacia</button>
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Syra Kol', 'ADM-01', 'Intercepción vox de patrullas Enforcers')">📻 Syra a Intercepción Vox</button>
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Halven Rusk', 'C-03', 'Control de perfusión tisular de Quartus')">🩺 Halven a C-03 (Quartus)</button>
                  <button class="btn-quick-order" onclick="dispatchChatOrder('Jarek Venn', 'GATE-01', 'Centinela armado en tronera izquierda')">⛓️ Jarek Guardia Compuerta</button>
                </div>

                <div style="margin-top:0.75rem; display:flex; gap:0.4rem;">
                  <input type="text" id="custom-chat-msg" class="form-control" style="font-size:0.75rem; padding:0.4rem 0.6rem;" placeholder="Escribir orden personalizada...">
                  <button class="btn-synth" style="padding:0.4rem 0.8rem;" onclick="dispatchCustomChatOrder()">ENVIAR</button>
                </div>
              </div>

              <!-- AGENT CENSO -->
              <div style="font-family:'Cinzel',serif; font-size:0.85rem; font-weight:800; color:var(--brass); margin-top:0.25rem;">📍 CENSO DE POSICIÓN Y ACCIONES</div>
              <div id="radar-agents-list" style="display:flex; flex-direction:column; gap:0.45rem; max-height:200px; overflow-y:auto;"></div>
            </div>

          </div>
        </div>
      </div>
    </section>

    <!-- TAB 2: SURGERY LAB, ANATOMICAL MONITOR & CYBERNETICS -->
    <section id="tab-medicae" class="tab-content">
      <div class="grid-dashboard">
        
        <!-- Operating Table & Anatomical Monitor -->
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">🩸 MESA QUIRÚRGICA & MONITOR ANATÓMICO (Q-01)</span>
            <span class="badge badge-brass">DIAGNOSTOR RHO-9</span>
          </div>
          <div class="panel-body">
            <div class="form-group">
              <label class="form-label">Seleccionar Paciente</label>
              <select id="surg-patient" class="form-control" onchange="loadPatientAnatomy(this.value)">
                <option value="Quartus Holt">Quartus Holt (4/11 · Desintubación Activa · C-03)</option>
                <option value="Tertius Holt">Tertius Holt (8/11 · Drenaje Torácico · C-01)</option>
                <option value="Paciente C-02">Paciente de Emergencia (Cama C-02)</option>
                <option value="Jarek Venn">Jarek Venn (0/9 · Torso Reconstruido)</option>
              </select>
            </div>

            <!-- ZONAL ANATOMICAL BREAKDOWN -->
            <div style="font-size:0.75rem; font-weight:700; color:var(--brass); margin-bottom:0.4rem;">🩺 EVALUACIÓN ANATÓMICA ZONAL:</div>
            <div id="anatomy-zones-container"></div>

            <div class="form-group" style="margin-top:0.75rem;">
              <label class="form-label">Procedimiento Clínico</label>
              <select id="surg-procedure" class="form-control">
                <option value="PERFUSION_TISULAR">Mantenimiento de Perfusión & Desintubación (Quartus) (+3 PV)</option>
                <option value="TORACICA">Cirugía Torácica Mayor / Drenaje Pleural (+3 PV)</option>
                <option value="TRAQUEOTOMIA_EMERGENCIA">Traqueotomía de Emergencia & Desobstrucción Aérea (+2 PV)</option>
                <option value="SUTURA_MAYOR">Desbridamiento & Sutura Antiséptica Profunda (+2 PV)</option>
                <option value="INJERTO_TISULAR">Injerto Tisular Biológico de Biobanco (+4 PV)</option>
                <option value="INFUSION_SHOCK">Estabilización de Shock Hemorrágico & Transfusión (+3 PV)</option>
                <option value="AMPUTACION_LIMPIA">Amputación Quirúrgica Limpia & Cauterización Láser (+2 PV)</option>
                <option value="EXTRACCION_PARASITOS">Extracción de Parásitos & Quistes del Sumidero (+3 PV)</option>
                <option value="ESTIMULACION_NEURAL_COMA">Electro-Estimulación Neural para Despertar de Coma (+2 PV)</option>
                <option value="INSTALACION_BIONICA">Instalación y Sincronización de Prótesis Biónica (+2 PV)</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Instrumental & Soporte</label>
              <div style="display:flex; flex-direction:column; gap:0.4rem; font-size:0.8rem; color:var(--text-muted);">
                <label><input type="checkbox" id="surg-diag" checked> Diagnostor Multispectral de Rho-9 (+15% a tirada)</label>
                <label><input type="checkbox" id="surg-blood"> Unidad de Sangre de Biobanco (+10% y evita shock)</label>
              </div>
            </div>

            <button class="btn-action-primary" onclick="executeSurgery()">⚡ INICIAR INTERVENCIÓN QUIRÚRGICA</button>
            <div id="surgery-result-box" style="margin-top:1rem; display:none;"></div>
          </div>
        </div>

        <!-- Khepra-9 Cybernetics Forge -->
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">⚙️ FORJA MECATRÓNICA DE KHEPRA-9 (T-01)</span>
            <span class="badge badge-green">BANCO BIÓNICO</span>
          </div>
          <div class="panel-body">
            
            <div class="char-card">
              <div class="char-card-header">
                <span>Prótesis Mecatrónica de Brazo Industrial</span>
                <span class="stat-val green">90 ¤</span>
              </div>
              <div class="char-role">Biónica de Trabajo · Destinatario: Jarek / Deudor</div>
              <div class="char-status">+10 a Fuerza, +1d5 daño desarmado y repara al 2º deudor.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="craftCybernetic('BRAZO_BIONICO_MECANICO')">🔧 FORJAR PRÓTESIS</button>
            </div>

            <div class="char-card">
              <div class="char-card-header">
                <span>Ojo Biónico con Visor Auspex Retiniano</span>
                <span class="stat-val green">120 ¤</span>
              </div>
              <div class="char-role">Cibernética de Detección · Destinatario: Severan / Alexander</div>
              <div class="char-status">+15 a Percepción visual, visión térmica e inmunidad a deslumbramiento.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="craftCybernetic('OJO_BIONICO_AUSPEX')">🔧 FORJAR IMPLANTE</button>
            </div>

            <div class="char-card">
              <div class="char-card-header">
                <span>Filtro Respiratorio Biomecánico Anti-Tox</span>
                <span class="stat-val green">80 ¤</span>
              </div>
              <div class="char-role">Implante Pulmonar · Destinatario: Séquito</div>
              <div class="char-status">Inmunidad total a gases cáusticos, humo de combate y asfixia.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="craftCybernetic('FILTRO_PULMONAR_TOX')">🔧 FORJAR FILTRO</button>
            </div>

            <div class="char-card">
              <div class="char-card-header">
                <span>Placas de Subdermo-Blindaje de Aleación</span>
                <span class="stat-val green">150 ¤</span>
              </div>
              <div class="char-role">Blindaje Corporal · Destinatario: Severan / Jarek</div>
              <div class="char-status">+1 Punto de Armadura permanente en todas las localizaciones.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="craftCybernetic('SUBDERMO_BLINDAJE')">🔧 FORJAR BLINDAJE</button>
            </div>

            <div id="cybernetics-result-box" style="margin-top:1rem; display:none;"></div>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 3: ALCHEMY & CLANDESTINE PHARMACOLOGY -->
    <section id="tab-alchemy" class="tab-content">
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">⚗️ LABORATORIO ALQUÍMICO & FARMACOLOGÍA DE RHO-9</span>
          <span class="badge badge-green">FÓRMULAS MAESTRAS</span>
        </div>
        <div class="panel-body">
          <div class="grid-dashboard" style="grid-template-columns:repeat(auto-fill, minmax(290px, 1fr));">
            
            <div class="char-card">
              <div class="char-card-header"><span>Stimm de Combate Hiper-Adrenal</span><span class="stat-val green">30 ¤</span></div>
              <div class="char-role">Farmacología Táctica · Req. Med 50</div>
              <div class="char-status">+10 a Reflejos y Fuerza x 3 turnos. Anula fatiga.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="synthesizeCompound('STIMM_COMBATE')">🧪 SINTETIZAR DOSIS</button>
            </div>

            <div class="char-card">
              <div class="char-card-header"><span>Concentrado Neurotóxico E-12 [Toxic(1)]</span><span class="stat-val green">40 ¤</span></div>
              <div class="char-role">Toxinas & Armas · Req. Med 60</div>
              <div class="char-status">Impregna arma blanca. Daño de veneno 1d5 PV/turno.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="synthesizeCompound('VENENO_TOXIC1')">🧪 SINTETIZAR DOSIS</button>
            </div>

            <div class="char-card">
              <div class="char-card-header"><span>Antídoto Químico Amplio Espectro</span><span class="stat-val green">35 ¤</span></div>
              <div class="char-role">Farmacología Médica · Req. Med 55</div>
              <div class="char-status">Neutraliza quimio-toxinas Escher y venenos orgánicos.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="synthesizeCompound('ANTIDOTO_UNIVERSAL')">🧪 SINTETIZAR DOSIS</button>
            </div>

            <div class="char-card">
              <div class="char-card-header"><span>Bálsamo Hemostático Cauterizante</span><span class="stat-val green">25 ¤</span></div>
              <div class="char-role">Traumatología · Req. Med 45</div>
              <div class="char-status">Detiene hemorragias al instante (+3 PV y sella vasos).</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="synthesizeCompound('BALSAMO_CAUTERIZANTE')">🧪 SINTETIZAR DOSIS</button>
            </div>

            <div class="char-card">
              <div class="char-card-header"><span>Suero Químico de la Verdad Escher</span><span class="stat-val green">45 ¤</span></div>
              <div class="char-role">Inquisición & Inteligencia · Req. Med 55</div>
              <div class="char-status">+20 a Interrogatorio y Persuasión durante 1 escena.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="synthesizeCompound('SUERO_VERDAD_ESCHER')">🧪 SINTETIZAR DOSIS</button>
            </div>

            <div class="char-card">
              <div class="char-card-header"><span>Tónico Coagulante Fúngico</span><span class="stat-val green">20 ¤</span></div>
              <div class="char-role">Urgencias Clandestinas · Req. Med 40</div>
              <div class="char-status">Estabiliza inmediatamente a pacientes agónicos (0 PV).</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="synthesizeCompound('TONICO_FUNGICO_COAGULANTE')">🧪 SINTETIZAR DOSIS</button>
            </div>

            <div class="char-card">
              <div class="char-card-header"><span>Neuro-Bloqueador de Dolor</span><span class="stat-val green">35 ¤</span></div>
              <div class="char-role">Farmacología Táctica · Req. Med 50</div>
              <div class="char-status">Ignora penalizadores de dolor y heridas críticas x 4 turnos.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="synthesizeCompound('NEURO_BLOQUEADOR_DOLOR')">🧪 SINTETIZAR DOSIS</button>
            </div>

            <div class="char-card">
              <div class="char-card-header"><span>Incienso Litúrgico de Purificación</span><span class="stat-val green">50 ¤</span></div>
              <div class="char-role">Bio-Ocultismo · Req. Med 60</div>
              <div class="char-status">Purifica Sanctum y restaura +1 Alma a la Reserva Umbral.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="synthesizeCompound('INCIENSO_PURIFICADOR_SANCTUM')">🧪 SINTETIZAR DOSIS</button>
            </div>

            <div class="char-card">
              <div class="char-card-header"><span>Suero Estabilizador de Mente Umbral</span><span class="stat-val green">60 ¤</span></div>
              <div class="char-role">Bio-Ocultismo · Req. Med 65</div>
              <div class="char-status">+15 de bono de Voluntad contra fenómenos Disformes.</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="synthesizeCompound('SUERO_UMBRAL')">🧪 SINTETIZAR DOSIS</button>
            </div>

          </div>
          <div id="alchemy-result-box" style="margin-top:1rem; display:none;"></div>
        </div>
      </div>
    </section>

    <!-- TAB 4: FACTIONS, CONTRACTS & BLACK MARKET -->
    <section id="tab-factions" class="tab-content">
      <div class="grid-dashboard">
        
        <!-- Factions Matrix & Contracts -->
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">⚖️ MATRIZ DE FACCIONES & CONTRATOS</span>
            <span class="badge badge-brass">DUST FALLS</span>
          </div>
          <div class="panel-body">
            <div id="factions-container"></div>
            
            <div style="font-family:'Cinzel',serif; font-size:0.9rem; font-weight:800; color:var(--brass); margin:1.25rem 0 0.5rem 0;">
              📜 BOLSA DE CONTRATOS CLANDESTINOS
            </div>
            <div id="contracts-container" style="display:flex; flex-direction:column; gap:0.5rem;"></div>
          </div>
        </div>

        <!-- Dust Falls Black Market Materials Bazaar -->
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">📦 MERCADO NEGRO // MATERIALES DE MEJORA</span>
            <span class="badge badge-green">PROVEEDOR ACTIVO</span>
          </div>
          <div class="panel-body">
            <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:1rem;">
              Adquiere suministros técnicos y piezas de contención para las mejoras de salas de Rho-9.
            </p>
            <div id="market-items-container" style="display:flex; flex-direction:column; gap:0.6rem;"></div>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 5: ESTADO & SÉQUITO -->
    <section id="tab-status" class="tab-content">
      <div class="grid-dashboard">
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">🛡️ ALEXANDER // OPERADOR UMBRAL</span>
            <span class="badge badge-brass">NIVEL 5</span>
          </div>
          <div class="panel-body">
            <div class="stat-row"><span class="stat-label">❤️ Salud Vital:</span><span class="stat-val green" id="pc-hp">12 / 12</span></div>
            <div class="progress-bar-bg"><div class="progress-fill fill-green" style="width: 100%;"></div></div>
            <div class="stat-row" style="margin-top: 0.75rem;"><span class="stat-label">⚡ Fatiga:</span><span class="stat-val" id="pc-fatigue">0 / 7</span></div>
            <div class="progress-bar-bg"><div class="progress-fill fill-amber" style="width: 0%;"></div></div>
            <div class="stat-row" style="margin-top: 0.75rem;"><span class="stat-label">🔮 Reserva Umbral:</span><span class="stat-val brass" id="pc-souls">10 Almas</span></div>
            <div class="stat-row"><span class="stat-label">🌟 Puntos de Destino:</span><span class="stat-val brass">3</span></div>
            <div class="stat-row"><span class="stat-label">💰 Saldo Disponible:</span><span class="stat-val green" id="pc-credits">1.046 Créditos (+300 pendientes)</span></div>
            <div class="stat-row"><span class="stat-label">📈 Experiencia Total:</span><span class="stat-val">1.335 XP (335 / 500)</span></div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">👥 EQUIPAMIENTO TÁCTICO DEL SÉQUITO</span>
            <span class="badge badge-brass">ARMAMENTO ASIGNADO</span>
          </div>
          <div class="panel-body">
            <div class="char-card">
              <div class="char-card-header"><span>Severan Holt (Capitán)</span><span class="badge badge-brass">L-01 // Carabina Kord-24</span></div>
              <div class="char-role">Seguridad & Mando · Armadura: Chaleco Antibalas (3 pts)</div>
              <div class="char-status">D5 | Pen 0 | Alcance 60m | Fiable / Ráfaga 3</div>
            </div>
            <div class="char-card">
              <div class="char-card-header"><span>Jarek Venn (Deudor)</span><span class="badge badge-brass">L-03 // Escopeta Compacta</span></div>
              <div class="char-role">Centinela de Compuerta · Armadura: Cuero Endurecido (1 pt)</div>
              <div class="char-status">D6 | Pen 0 | Alcance 30m | Dispersión / Potente</div>
            </div>
            <div class="char-card">
              <div class="char-card-header"><span>Syra Kol (Logística)</span><span class="badge badge-brass">P-01 // Pistola Compacta Hesh-9</span></div>
              <div class="char-role">Recepción & Farmacia · Armadura: Ropa Reforzada (1 pt)</div>
              <div class="char-status">D4 | Pen 0 | Alcance 20m | Ocultable</div>
            </div>
            <div class="char-card">
              <div class="char-card-header"><span>Khepra-9 (Tecnosacerdote)</span><span class="badge badge-brass">P-04 // Autopistola Vex</span></div>
              <div class="char-role">Taller & Plasma · Armadura: Túnicas Blindadas (2 pts)</div>
              <div class="char-status">D4 | Pen 0 | Alcance 25m | Ráfaga 3 / Automática</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 6: SOMBRA INFINITA -->
    <section id="tab-inventory" class="tab-content">
      <div class="filter-bar">
        <input type="text" id="inv-search" class="search-input" placeholder="🔍 Filtrar armas, fármacos, consumibles, herramientas o muestras..." onkeyup="filterInventory()">
      </div>
      <div class="panel">
        <div class="panel-header"><span class="panel-title">⚔️ ARMAS Y BOTÍN DE LA INCURSIÓN NOCTURNA</span><span class="badge badge-brass">SOMBRA INFINITA</span></div>
        <div class="panel-body">
          <div class="inv-category-grid" id="weapons-grid">
            <div class="inv-item-card"><div class="inv-item-title"><span>P-01 // Pistola Compacta Hesh-9</span><span class="badge badge-brass">8 / 8</span></div><div class="inv-item-detail">D4 | Pen 0 | Alcance 20m | Compacta / Ocultable</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>P-02 // Pistola Servicio Mk II</span><span class="badge badge-brass">12 / 12</span></div><div class="inv-item-detail">D5 | Pen 0 | Alcance 30m | Fiable | Patrón Servicio</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>P-03 // Pistola Servicio Mk II</span><span class="badge badge-brass">12 / 12</span></div><div class="inv-item-detail">D5 | Pen 0 | Alcance 30m | Fiable | Patrón Servicio</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>P-04 // Autopistola Vex</span><span class="badge badge-brass">18 / 18</span></div><div class="inv-item-detail">D4 | Pen 0 | Alcance 25m | Ráfaga 3 / Automática</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>P-05 // Pistola Pesada Brakk</span><span class="badge badge-brass">8 / 8</span></div><div class="inv-item-detail">D6 | Pen 1 | Alcance 25m | Retroceso Fuerte / Pesada</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>L-01 // Carabina Kord-24</span><span class="badge badge-brass">24 / 24</span></div><div class="inv-item-detail">D5 | Pen 0 | Alcance 60m | Carabina / Fiable | Ráfaga 3</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>L-02 // Carabina Kord-24</span><span class="badge badge-brass">24 / 24</span></div><div class="inv-item-detail">D5 | Pen 0 | Alcance 60m | Carabina / Fiable | Ráfaga 3</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>L-03 // Escopeta Compacta</span><span class="badge badge-brass">6 / 6</span></div><div class="inv-item-detail">D6 | Pen 0 | Alcance 30m | Dispersión / Potente</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>L-04 // Autogun Patrón Reth</span><span class="badge badge-brass">30 / 30</span></div><div class="inv-item-detail">D5 | Pen 0 | Alcance 80m | Automática / Ráfaga 3</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>L-05 // Rifle Precisión Manufactorum</span><span class="badge badge-brass">10 / 10</span></div><div class="inv-item-detail">D6 | Pen 1 | Alcance 120m | Precisa / Lenta</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>Caja Reforzada de Explosivos</span><span class="badge badge-brass">6 Granadas</span></div><div class="inv-item-detail">3 Granadas Frag · 2 Granadas de Humo · 1 Granada Krak</div></div>
            <div class="inv-item-card"><div class="inv-item-title"><span>Reserva de Munición Suelta</span><span class="badge badge-green">1.000+ Proyectiles</span></div><div class="inv-item-detail">Pistola (240) · Kord-24 (312) · Autogun (240) · Escopeta (120 + 8 incendiarios)</div></div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 7: SIMULATOR -->
    <section id="tab-roller" class="tab-content">
      <div class="panel" style="max-width: 800px; margin: 0 auto;">
        <div class="panel-header">
          <span class="panel-title">🎲 TERMINAL DETERMINISTA DE TIRADAS (WARHAMMER 40K)</span>
          <span class="badge badge-brass">MOTOR REST API</span>
        </div>
        <div class="panel-body">
          <div class="dice-form" style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-bottom:1rem;">
            <div class="form-group"><label class="form-label">Acción Declarada</label><input type="text" id="roll-action" class="form-control" value="Alexander ausculta y estabiliza a Tertius en Rho-9"></div>
            <div class="form-group"><label class="form-label">Atributo o Habilidad Base</label><select id="roll-attr" class="form-control"><option value="65">Medicina Clandestina (65)</option><option value="68">Voluntad / Poderes Umbrales (68)</option><option value="55">Habilidad de Proyectiles / Balística (55)</option><option value="48">Agilidad / Sigilo (48)</option><option value="52">Percepción / Diagnóstico (52)</option><option value="45">Cuerpo a Cuerpo (45)</option></select></div>
            <div class="form-group"><label class="form-label">Modificador (+/-)</label><select id="roll-mod" class="form-control"><option value="15">+15 (Diagnostor Rho-9)</option><option value="10">+10 (Equipo médico avanzado)</option><option value="0">+0 (Estándar)</option><option value="-10">-10 (Bajo presión)</option></select></div>
            <div class="form-group"><label class="form-label">Actor</label><input type="text" id="roll-actor" class="form-control" value="Alexander"></div>
            <button class="btn-action-primary" style="grid-column: 1 / -1;" onclick="executeRoll()">⚡ EJECUTAR TIRADA DETERMINISTA d100</button>
          </div>
          <div id="roll-result" class="roll-result-box" style="display:none; background:#0a0d12; border:1px dashed var(--border-panel); padding:1rem; border-radius:4px;"></div>
        </div>
      </div>
    </section>

    <!-- TAB 8: DOSSIERS -->
    <section id="tab-docs" class="tab-content">
      <div class="panel">
        <div class="panel-header"><span class="panel-title">📜 ARCHIVO DE CAMPAÑA // DOSSIERS MAESTROS</span></div>
        <div class="panel-body">
          <div class="doc-selector">
            <button class="doc-btn active" onclick="loadDocument('FICHA_DEL_PERSONAJE', this)">FICHA DEL PERSONAJE</button>
            <button class="doc-btn" onclick="loadDocument('HISTORIA_DEL_PERSONAJE', this)">HISTORIA & CRÓNICA</button>
            <button class="doc-btn" onclick="loadDocument('PERSONAJES', this)">PERSONAJES & PNJ</button>
            <button class="doc-btn" onclick="loadDocument('BASES_Y_DOMINIOS', this)">BASES Y DOMINIOS</button>
            <button class="doc-btn" onclick="loadDocument('REPUTACION_DE_FACCIONES', this)">REPUTACIÓN DE FACCIONES</button>
            <button class="doc-btn" onclick="loadDocument('SEQUITO', this)">SÉQUITO</button>
          </div>
          <div class="doc-viewer-area" id="doc-content">Cargando documento maestro...</div>
        </div>
      </div>
    </section>

  </main>

  <!-- MODAL FOR ROOM DETAILS & UPGRADES -->
  <div id="room-modal" class="room-detail-modal" onclick="closeRoomModal(event)">
    <div class="room-detail-content" onclick="event.stopPropagation()">
      <button class="modal-close-btn" onclick="document.getElementById('room-modal').style.display='none'">&times;</button>
      <div style="font-size:0.75rem; color:var(--brass-dim);" id="modal-room-code">SECTOR</div>
      <h2 style="font-family:'Cinzel',serif; color:var(--brass); margin-bottom:0.75rem;" id="modal-room-name">Nombre de la Sala</h2>
      <div class="stat-row"><span class="stat-label">🏷️ Nivel & Estado:</span><span class="stat-val brass" id="modal-room-level">Nivel 1</span></div>
      <div class="stat-row"><span class="stat-label">👥 Personal Presente:</span><span class="stat-val" id="modal-room-occupants">-</span></div>
      <div class="stat-row"><span class="stat-label">🔧 Equipamiento Instalado:</span><span class="stat-val" id="modal-room-equipment" style="font-size:0.78rem;">-</span></div>
      <div class="stat-row"><span class="stat-label">✨ Bono a la Campaña:</span><span class="stat-val green" id="modal-room-bonus" style="font-size:0.78rem;">-</span></div>
      
      <div class="upgrade-box" id="modal-upgrade-section">
        <div style="font-family:'Cinzel',serif; font-size:0.9rem; font-weight:800; color:var(--amber); margin-bottom:0.5rem;" id="modal-upgrade-title">🚀 Siguiente Mejora</div>
        <div style="font-size:0.8rem; color:var(--text-main); margin-bottom:0.5rem;" id="modal-upgrade-effect">Efecto: -</div>
        <div class="stat-row" style="background:#0b0e14; padding:0.4rem 0.6rem; border-radius:4px;"><span class="stat-label">💰 Coste Créditos:</span><span class="stat-val green" id="modal-upgrade-credits">0 ¤</span></div>
        <div class="stat-row" style="background:#0b0e14; padding:0.4rem 0.6rem; border-radius:4px; margin-top:0.25rem;"><span class="stat-label">🔩 Materiales:</span><span class="stat-val brass" id="modal-upgrade-mats" style="font-size:0.75rem;">-</span></div>
        <button class="btn-upgrade-action" id="btn-execute-upgrade" onclick="executeUpgrade()">🔨 EJECUTAR PROYECTO DE MEJORA</button>
      </div>

      <div class="upgrade-box" id="modal-explore-section" style="display:none; border-color:var(--cyan-plasma);">
        <div style="font-family:'Cinzel',serif; font-size:0.9rem; font-weight:800; color:var(--cyan-plasma); margin-bottom:0.5rem;">🔦 Exploración de Subnivel</div>
        <div style="font-size:0.8rem; color:var(--text-main); margin-bottom:0.5rem;" id="modal-explore-cost">Requisito: 1 Turno + Auspex</div>
        <button class="btn-explore-action" id="btn-execute-explore" onclick="executeExploration()">🔦 DESPEJAR NIEBLA & ASEGURAR SECTOR</button>
      </div>
      <div id="modal-feedback" style="margin-top:0.75rem; font-size:0.8rem; display:none;"></div>
    </div>
  </div>

  <footer>
    WH40K NARRATIVE ENGINE · API DE PRODUCCIÓN · <span class="footer-highlight">MEDICAE STATION RHO-9</span> · NECROMUNDA
  </footer>

  <script>
    const API_KEY = "wh40k_secret_key_12345";
    let currentFloor = 0;
    let currentSelectedRoom = null;
    let availableCredits = 1046;
    let currentPatient = null;
    let isRedAlert = false;
    let lastGeneratedPrompt = "";

    // REAL-TIME CHRONO CLOCK (TICKING CONTINUOUSLY EVERY SECOND)
    let currentDay = 4;
    let currentHour = 23;
    let currentMinute = 54;
    let currentSecond = 0;
    let currentTurn = 918;

    function updateClockDisplay() {
      const hh = String(currentHour).padStart(2, '0');
      const mm = String(currentMinute).padStart(2, '0');
      const ss = String(currentSecond).padStart(2, '0');
      const phase = (currentHour >= 6 && currentHour < 18) ? 'CICLO DIURNO' : 'VIGILIA NOCTURNA';
      document.getElementById('chrono-clock-time').textContent = `DÍA ${String(currentDay).padStart(2, '0')} · ${phase} ${hh}:${mm}:${ss}`;
      document.getElementById('chrono-clock-turn').textContent = `TURNO ${currentTurn} · MEDICAE STATION RHO-9`;
    }

    // Tick every 1 second continuously
    setInterval(() => {
      currentSecond++;
      if (currentSecond >= 60) {
        currentSecond = 0;
        currentMinute++;
        if (currentMinute >= 60) {
          currentMinute = 0;
          currentHour = (currentHour + 1) % 24;
          if (currentHour === 0) currentDay++;
        }
      }
      updateClockDisplay();
    }, 1000);

    function advanceCycleHour() {
      currentHour = (currentHour + 1) % 24;
      if (currentHour === 0) currentDay++;
      currentTurn++;
      currentSecond = 0;
      updateClockDisplay();
      triggerRadarSweep();
      loadTelemetry();
    }

    function showCanonicalPrompt(promptText) {
      lastGeneratedPrompt = promptText;
      const card = document.getElementById('global-prompt-card');
      const content = document.getElementById('global-prompt-content');
      content.textContent = promptText;
      card.style.display = 'block';
      card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function copyCanonicalPrompt() {
      if (!lastGeneratedPrompt) return;
      navigator.clipboard.writeText(lastGeneratedPrompt).then(() => {
        alert("¡Prompt canónico copiado al portapapeles! Pégalo directamente en ChatGPT.");
      }).catch(err => {
        prompt("Copia el texto manualmente:", lastGeneratedPrompt);
      });
    }

    async function fetchFullTurnReport() {
      try {
        const resp = await fetch('/api/chat/turn_report', { headers: { 'x-api-key': API_KEY } });
        if (resp.ok) {
          const d = await resp.json();
          showCanonicalPrompt(d.turn_report);
        }
      } catch (e) { console.error(e); }
    }

    async function fetchTimeDirective() {
      try {
        const resp = await fetch('/api/chat/time_directive', { headers: { 'x-api-key': API_KEY } });
        if (resp.ok) {
          const d = await resp.json();
          showCanonicalPrompt(d.time_directive);
        }
      } catch (e) { console.error(e); }
    }

    async function fetchHudStandard() {
      try {
        const resp = await fetch('/api/chat/hud_standard', { headers: { 'x-api-key': API_KEY } });
        if (resp.ok) {
          const d = await resp.json();
          showCanonicalPrompt(d.hud_standard);
        }
      } catch (e) { console.error(e); }
    }

    async function importChatNarrative() {
      const input = document.getElementById('narrative-import-input');
      const text = input.value.trim();
      if (!text) return;

      try {
        const resp = await fetch('/api/chat/parse_narrative', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ narrative_text: text })
        });
        const d = await resp.json();
        if (resp.ok && d.success) {
          input.value = '';
          alert(`✅ Sincronización Exitosa: ${d.detected_speaker} se desplaza a ${d.detected_room || 'su sector'}. Reloj y telemetría actualizados.`);
          
          if (d.detected_speaker && d.detected_room) {
            const agent = radarAgents.find(a => a.name.toLowerCase().includes(d.detected_speaker.toLowerCase().split(' ')[0]));
            const room = roomNodes[d.detected_room];
            if (agent && room) {
              agent.dialogue = d.extracted_dialogue || 'Órden en curso.';
              agent.dialogueTimer = 240;
              agent.currentRoom = d.detected_room;
              agent.path.unshift({
                x: room.x + room.w / 2,
                y: room.y + room.h / 2,
                task: `Misión activa en ${room.name}`,
                room: d.detected_room
              });
              agent.pathIdx = 0;
            }
          }
          
          advanceCycleHour();
          renderRadarLegend();
          await loadTelemetry();
        } else {
          alert(d.error || 'Error procesando texto');
        }
      } catch (e) { alert("Error: " + e.message); }
    }

    function toggleRedAlert() {
      isRedAlert = !isRedAlert;
      document.body.classList.toggle('red-alert-active', isRedAlert);
      const btn = document.getElementById('btn-red-alert-toggle');
      btn.classList.toggle('active', isRedAlert);
      btn.innerHTML = isRedAlert ? '🚨 ALERTA ROJA (ACTIVA)' : '🚨 ALERTA ROJA';

      if (isRedAlert) {
        document.getElementById('live-chat-ticker').textContent = '🚨 [ALERTA ROJA] ¡COMPUERTA PRINCIPAL SELLADA! Personal a puestos de combate.';
        dispatchChatOrder('Severan Holt', 'GATE-01', 'Tomando posición con carabina en tronera principal');
        dispatchChatOrder('Jarek Venn', 'GATE-01', 'Armando afuste de escopeta en compuerta');
        dispatchChatOrder('Alexander', 'Q-01', 'Preparando instrumental quirúrgico de emergencia');
        showCanonicalPrompt(
          `[ALERTA ROJA // PROTOCOLO DE DEFENSA EN MEDICAE STATION RHO-9]\n` +
          `Turno ${currentTurn} · Día ${currentDay:02d} · VIGILIA NOCTURNA\n` +
          `Severan Holt y Jarek Venn han sellado los cerrojos blindados de GATE-01 con carabina Kord-24 y escopeta listas.\n` +
          `Alexander toma posición en el Quirófano Q-01 con el Diagnostor Multispectral encendido.\n` +
          `Defensa Perimetral activa: 75% | Estado: Zafarrancho de Combate.`
        );
      } else {
        document.getElementById('live-chat-ticker').textContent = '✅ [VIGILIA ESTÁNDAR] Protocolo de alerta levantado. Personal en guardia rutinaria.';
      }
    }

    // ==========================================
    // ENHANCED HD MOTION RADAR & PATHFINDING
    // ==========================================
    const roomNodes = {
      'GATE-01': { x: 90, y: 250, name: 'Compuerta', w: 100, h: 80, type: 'sec' },
      'ADM-01': { x: 230, y: 130, name: 'Recepción', w: 100, h: 75, type: 'log' },
      'COMM-01': { x: 230, y: 250, name: 'Sala Común', w: 100, h: 80, type: 'liv' },
      'HAB-02': { x: 230, y: 370, name: 'Dorm. Guardia', w: 100, h: 75, type: 'liv' },
      'HAB-01': { x: 375, y: 65, name: 'Sanctum Alex', w: 110, h: 65, type: 'liv' },
      'Q-01': { x: 375, y: 170, name: 'Quirófano Central', w: 120, h: 100, type: 'med' },
      'E-01': { x: 375, y: 300, name: 'Esterilización', w: 110, h: 70, type: 'med' },
      'T-01': { x: 375, y: 395, name: 'Taller Mecatrónico', w: 110, h: 75, type: 'tech' },
      'F-02': { x: 535, y: 105, name: 'Biobanco & Farmacia', w: 105, h: 80, type: 'sto' },
      'C-01': { x: 535, y: 215, name: 'Cama Tertius', w: 95, h: 60, type: 'rec' },
      'C-02': { x: 535, y: 295, name: 'Cama Triaje', w: 95, h: 60, type: 'rec' },
      'C-03': { x: 535, y: 375, name: 'Cama Quartus (Nvl 2)', w: 95, h: 65, type: 'rec' },
      'HAB-03': { x: 670, y: 145, name: 'Dorm. Syra/Khepra', w: 100, h: 80, type: 'liv' },
      'HAB-04': { x: 670, y: 260, name: 'Refugio Clandestino', w: 100, h: 80, type: 'liv' },
      'SUB-01': { x: 670, y: 375, name: 'Acceso Subniveles', w: 100, h: 70, type: 'fog' }
    };

    const radarAgents = [
      {
        id: 'severan',
        name: 'Severan Holt',
        role: 'Mando de Seguridad',
        icon: '🛡️',
        color: '#10b981',
        x: 140, y: 290,
        currentRoom: 'GATE-01',
        dialogue: 'Compuerta atrancada. Cero intrusiones.',
        dialogueTimer: 180,
        path: [
          { x: 140, y: 290, task: 'Vigilancia en Compuerta Principal', room: 'GATE-01' },
          { x: 280, y: 290, task: 'Patrullando Pasillo Central', room: 'COMM-01' },
          { x: 280, y: 405, task: 'Inspección de Armero de Guardia', room: 'HAB-02' },
          { x: 140, y: 290, task: 'Custodiando Acceso GATE-01', room: 'GATE-01' }
        ],
        pathIdx: 0,
        speed: 0.75
      },
      {
        id: 'khepra',
        name: 'Khepra-9',
        role: 'Tecnosacerdote',
        icon: '⚙️',
        color: '#06b6d4',
        x: 430, y: 430,
        currentRoom: 'T-01',
        dialogue: 'Omnissiah preserve la red de plasma.',
        dialogueTimer: 150,
        path: [
          { x: 430, y: 430, task: 'Calibrando Torno en Taller T-01', room: 'T-01' },
          { x: 430, y: 335, task: 'Purgando Filtros en Esterilización', room: 'E-01' },
          { x: 435, y: 220, task: 'Revisando Diagnostor en Quirófano', room: 'Q-01' },
          { x: 430, y: 430, task: 'Ensamblando Prótesis en T-01', room: 'T-01' }
        ],
        pathIdx: 0,
        speed: 0.55
      },
      {
        id: 'syra',
        name: 'Syra Kol (16a)',
        role: 'Logística & Farmacia',
        icon: '📋',
        color: '#f59e0b',
        x: 280, y: 165,
        currentRoom: 'ADM-01',
        dialogue: 'Inventario de fármacos auditado: 200+ ampollas.',
        dialogueTimer: 200,
        path: [
          { x: 280, y: 165, task: 'Contabilidad en Cogitador ADM-01', room: 'ADM-01' },
          { x: 585, y: 145, task: 'Clasificando Químicos en Farmacia', room: 'F-02' },
          { x: 280, y: 290, task: 'Control de Raciones en Comedor', room: 'COMM-01' },
          { x: 280, y: 165, task: 'Auditando en Recepción ADM-01', room: 'ADM-01' }
        ],
        pathIdx: 0,
        speed: 0.65
      },
      {
        id: 'jarek',
        name: 'Jarek Venn',
        role: 'Deudor en Guardia',
        icon: '⛓️',
        color: '#94a3b8',
        x: 110, y: 270,
        currentRoom: 'GATE-01',
        dialogue: 'Cumpliendo mi guardia, amo Alexander.',
        dialogueTimer: 120,
        path: [
          { x: 110, y: 270, task: 'Centinela en Tronera Izquierda', room: 'GATE-01' },
          { x: 145, y: 300, task: 'Centinela en Tronera Derecha', room: 'GATE-01' }
        ],
        pathIdx: 0,
        speed: 0.3
      },
      {
        id: 'halven',
        name: 'Halven Rusk',
        role: 'Auxiliar Quirúrgico',
        icon: '🩺',
        color: '#c99a3e',
        x: 410, y: 220,
        currentRoom: 'Q-01',
        dialogue: 'Cosecha completada. Cauterizando instrumental.',
        dialogueTimer: 160,
        path: [
          { x: 410, y: 220, task: 'Asistencia Médica en Quirófano', room: 'Q-01' },
          { x: 580, y: 405, task: 'Supervisando Perfusión de Quartus', room: 'C-03' },
          { x: 580, y: 245, task: 'Auscultando Drenaje de Tertius', room: 'C-01' },
          { x: 410, y: 220, task: 'Limpiando Autoclave en Q-01', room: 'Q-01' }
        ],
        pathIdx: 0,
        speed: 0.6
      },
      {
        id: 'alexander',
        name: 'Alexander',
        role: 'Operador Umbral',
        icon: '👤',
        color: '#e2e8f0',
        x: 430, y: 95,
        currentRoom: 'HAB-01',
        dialogue: 'Las sombras susurran... mantened la guardia.',
        dialogueTimer: 240,
        path: [
          { x: 430, y: 95, task: 'Meditación Umbral en Sanctum', room: 'HAB-01' },
          { x: 435, y: 215, task: 'Supervisión en Quirófano Central', room: 'Q-01' },
          { x: 585, y: 145, task: 'Inspección de Muestras en Biobanco', room: 'F-02' },
          { x: 430, y: 95, task: 'Canalización de Reserva Umbral', room: 'HAB-01' }
        ],
        pathIdx: 0,
        speed: 0.45
      }
    ];

    let radarSweepAngle = 0;
    let selectedAgentId = 'severan';

    function initRadar() {
      renderRadarLegend();
      requestAnimationFrame(renderRadarLoop);
    }

    function renderRadarLegend() {
      const list = document.getElementById('radar-agents-list');
      if (!list) return;
      list.innerHTML = '';

      radarAgents.forEach(a => {
        const card = document.createElement('div');
        card.className = `agent-tracker-card ${a.id === selectedAgentId ? 'active' : ''}`;
        card.onclick = () => { selectedAgentId = a.id; renderRadarLegend(); };
        card.innerHTML = `
          <div class="agent-header">
            <span>${a.icon} ${a.name}</span>
            <span style="color:${a.color}; font-size:0.7rem;">[${a.currentRoom || 'RHO-9'}]</span>
          </div>
          <div class="agent-task">📍 ${a.path[a.pathIdx].task}</div>
        `;
        list.appendChild(card);
      });
    }

    function triggerRadarSweep() {
      radarSweepAngle = 0;
    }

    async function dispatchChatOrder(speaker, targetRoom, customTask) {
      const agent = radarAgents.find(a => a.name.toLowerCase().includes(speaker.toLowerCase().split(' ')[0]));
      const room = roomNodes[targetRoom];

      if (agent && room) {
        agent.dialogue = `¡Entendido! Me dirijo a ${room.name}.`;
        agent.dialogueTimer = 220;
        agent.currentRoom = targetRoom;
        
        agent.path.unshift({
          x: room.x + room.w / 2,
          y: room.y + room.h / 2,
          task: customTask || `En misión en ${room.name}`,
          room: targetRoom
        });
        agent.pathIdx = 0;
      }

      try {
        const resp = await fetch('/api/chat/sync', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({
            event_type: 'MOVEMENT',
            speaker: speaker,
            message: customTask || `Traslado táctico a ${targetRoom}`,
            target_room: targetRoom,
            advance_turns: 1
          })
        });
        const data = await resp.json();
        if (resp.ok) {
          document.getElementById('live-chat-ticker').textContent = `[${speaker}] ${customTask || 'Traslado táctico a ' + targetRoom}`;
          advanceCycleHour();
          renderRadarLegend();
          showCanonicalPrompt(
            `[DESPLAZAMIENTO TÁCTICO // COGITADOR RHO-9]\n` +
            `Operador: ${speaker}\n` +
            `Sector Destino: ${targetRoom} (${room ? room.name : 'Sector'})\n` +
            `Acción Ejecutada: ${customTask || 'Traslado de reconocimiento'}\n` +
            `Turno Actual: ${currentTurn} · Día ${currentDay:02d}`
          );
        }
      } catch (err) { console.error(err); }
    }

    async function dispatchCustomChatOrder() {
      const input = document.getElementById('custom-chat-msg');
      const text = input.value.trim();
      if (!text) return;

      document.getElementById('live-chat-ticker').textContent = `[ORDEN CHAT] ${text}`;

      const agent = radarAgents.find(a => a.id === selectedAgentId) || radarAgents[0];
      agent.dialogue = text;
      agent.dialogueTimer = 260;

      try {
        await fetch('/api/chat/sync', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({
            event_type: 'DIALOGUE',
            speaker: agent.name,
            message: text,
            target_room: agent.currentRoom,
            advance_turns: 0
          })
        });
        input.value = '';
        await loadTelemetry();
        showCanonicalPrompt(
          `[ORDEN NARRATIVA // COGITADOR RHO-9]\n` +
          `Emisor: ${agent.name} (${agent.role})\n` +
          `Ubicación: ${agent.currentRoom}\n` +
          `Transmisión Vox: "${text}"\n` +
          `Turno: ${currentTurn}`
        );
      } catch (e) { console.error(e); }
    }

    function renderRadarLoop() {
      const canvas = document.getElementById('radarCanvas');
      if (canvas && canvas.offsetParent !== null) {
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;

        ctx.fillStyle = isRedAlert ? 'rgba(20, 6, 6, 0.3)' : 'rgba(4, 6, 8, 0.3)';
        ctx.fillRect(0, 0, w, h);

        ctx.strokeStyle = isRedAlert ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.06)';
        ctx.lineWidth = 1;
        for (let x = 0; x < w; x += 35) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
        for (let y = 0; y < h; y += 35) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }

        ctx.strokeStyle = 'rgba(201, 154, 62, 0.18)';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(140, 290); ctx.lineTo(280, 290);
        ctx.lineTo(280, 165); ctx.lineTo(435, 95);
        ctx.moveTo(280, 290); ctx.lineTo(280, 405);
        ctx.moveTo(280, 290); ctx.lineTo(435, 220);
        ctx.lineTo(430, 335); ctx.lineTo(430, 430);
        ctx.moveTo(435, 220); ctx.lineTo(585, 145);
        ctx.moveTo(435, 220); ctx.lineTo(580, 245);
        ctx.lineTo(580, 325); ctx.lineTo(580, 405);
        ctx.moveTo(580, 325); ctx.lineTo(720, 300);
        ctx.stroke();

        Object.entries(roomNodes).forEach(([id, r]) => {
          ctx.fillStyle = 'rgba(15, 20, 28, 0.85)';
          ctx.strokeStyle = (id === 'GATE-01' || id === 'Q-01' || id === 'C-03') ? 'rgba(201, 154, 62, 0.8)' : 'rgba(38, 46, 59, 0.9)';
          ctx.lineWidth = (id === 'GATE-01' || id === 'Q-01' || id === 'C-03') ? 2 : 1.5;
          ctx.fillRect(r.x, r.y, r.w, r.h);
          ctx.strokeRect(r.x, r.y, r.w, r.h);

          ctx.fillStyle = 'rgba(201, 154, 62, 0.7)';
          ctx.font = 'bold 9px "JetBrains Mono"';
          ctx.fillText(id, r.x + 6, r.y + 13);

          ctx.fillStyle = 'rgba(226, 232, 240, 0.9)';
          ctx.font = '10px "JetBrains Mono"';
          ctx.fillText(r.name, r.x + 6, r.y + 26);

          if (id === 'Q-01') {
            ctx.fillStyle = 'rgba(16, 185, 129, 0.15)';
            ctx.fillRect(r.x + 20, r.y + 35, r.w - 40, r.h - 45);
            ctx.strokeStyle = 'rgba(16, 185, 129, 0.5)';
            ctx.strokeRect(r.x + 20, r.y + 35, r.w - 40, r.h - 45);
          } else if (id === 'T-01') {
            if (Math.random() > 0.6) {
              ctx.fillStyle = '#f59e0b';
              ctx.fillRect(r.x + 40 + (Math.random()*20), r.y + 40 + (Math.random()*20), 2, 2);
            }
          } else if (id === 'C-03') {
            ctx.strokeStyle = '#10b981';
            ctx.lineWidth = 1;
            ctx.beginPath();
            const ecgX = r.x + 10;
            const ecgY = r.y + 45;
            const t = (Date.now() / 120) % 60;
            ctx.moveTo(ecgX, ecgY);
            ctx.lineTo(ecgX + t, ecgY + (t > 25 && t < 35 ? (t % 2 === 0 ? -6 : 6) : 0));
            ctx.stroke();
          }
        });

        radarAgents.forEach(a => {
          const target = a.path[a.pathIdx];
          const dx = target.x - a.x;
          const dy = target.y - a.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 3) {
            a.pathIdx = (a.pathIdx + 1) % a.path.length;
            if (target.room) a.currentRoom = target.room;
          } else {
            a.x += (dx / dist) * a.speed;
            a.y += (dy / dist) * a.speed;
          }

          ctx.beginPath();
          ctx.arc(a.x, a.y, a.id === selectedAgentId ? 6.5 : 5, 0, Math.PI * 2);
          ctx.fillStyle = a.color;
          ctx.fill();

          ctx.beginPath();
          ctx.arc(a.x, a.y, (Date.now() / 150) % 15 + 4, 0, Math.PI * 2);
          ctx.strokeStyle = a.color + '44';
          ctx.lineWidth = 1.5;
          ctx.stroke();

          ctx.fillStyle = a.color;
          ctx.font = 'bold 9.5px "JetBrains Mono"';
          ctx.fillText(`${a.icon} ${a.name.split(' ')[0]}`, a.x + 8, a.y + 3);

          if (a.dialogueTimer > 0) {
            a.dialogueTimer--;
            ctx.fillStyle = 'rgba(11, 15, 22, 0.92)';
            ctx.strokeStyle = a.color;
            ctx.lineWidth = 1;
            
            const msgWidth = Math.min(ctx.measureText(a.dialogue).width + 12, 160);
            ctx.fillRect(a.x - msgWidth / 2, a.y - 32, msgWidth, 18);
            ctx.strokeRect(a.x - msgWidth / 2, a.y - 32, msgWidth, 18);

            ctx.fillStyle = '#ffffff';
            ctx.font = '8.5px "JetBrains Mono"';
            ctx.fillText(a.dialogue.length > 22 ? a.dialogue.substring(0, 20) + '...' : a.dialogue, a.x - msgWidth / 2 + 5, a.y - 20);
          }
        });

        radarSweepAngle = (radarSweepAngle + 0.02) % (Math.PI * 2);
        const sweepLen = Math.max(w, h);
        ctx.beginPath();
        ctx.moveTo(w / 2, h / 2);
        ctx.lineTo(w / 2 + Math.cos(radarSweepAngle) * sweepLen, h / 2 + Math.sin(radarSweepAngle) * sweepLen);
        ctx.strokeStyle = isRedAlert ? 'rgba(239, 68, 68, 0.4)' : 'rgba(16, 185, 129, 0.3)';
        ctx.lineWidth = 2;
        ctx.stroke();
      }
      requestAnimationFrame(renderRadarLoop);
    }

    // ==========================================
    // ANATOMICAL MONITOR & CYBERNETICS METHODS
    // ==========================================
    async function loadPatientAnatomy(patientName) {
      const c = document.getElementById('anatomy-zones-container');
      try {
        const resp = await fetch(`/api/medicae/patient_anatomy?patient_name=${encodeURIComponent(patientName)}`, {
          headers: { 'x-api-key': API_KEY }
        });
        if (resp.ok) {
          const d = await resp.json();
          c.innerHTML = '';
          Object.entries(d.zones || {}).forEach(([zoneKey, z]) => {
            let color = 'var(--green-auspex)';
            if (z.status === 'CRÍTICO') color = 'var(--crimson-light)';
            if (z.status === 'MODERADO') color = 'var(--amber)';

            const card = document.createElement('div');
            card.className = 'anatomy-zone-card';
            card.innerHTML = `
              <div>
                <span style="font-weight:700; color:var(--text-main); font-size:0.8rem;">[${zoneKey}] ${z.condition}</span>
                <div style="font-size:0.7rem; color:var(--text-muted);">Daño: ${z.damage} pts · Proc. recomendado: ${z.rec_proc || 'SUTURA_MAYOR'}</div>
              </div>
              <span class="badge" style="border-color:${color}; color:${color}; font-size:0.68rem;">${z.status}</span>
            `;
            c.appendChild(card);
          });
        }
      } catch (e) { console.error(e); }
    }

    async function executeSurgery() {
      const p = document.getElementById('surg-patient').value;
      const proc = document.getElementById('surg-procedure').value;
      const useDiag = document.getElementById('surg-diag').checked;
      const useBlood = document.getElementById('surg-blood').checked;
      const res = document.getElementById('surgery-result-box');

      res.style.display = 'block';
      res.innerHTML = '<span style="color:var(--amber);">[CIRUGÍA EN CURSO // APLICANDO ANESTESIA E INSTRUMENTAL...]</span>';

      try {
        const resp = await fetch('/api/medicae/operate', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ patient_name: p, procedure: proc, medic_skill: 65, use_diagnostor: useDiag, use_blood: useBlood })
        });
        const d = await resp.json();
        res.innerHTML = `
          <div class="upgrade-box" style="border-color:${d.success ? 'var(--green-auspex)' : 'var(--crimson-light)'};">
            <div style="font-weight:800; color:${d.success ? 'var(--green-auspex)' : 'var(--crimson-light)'};">${d.message}</div>
            <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.35rem;">Consumibles empleados: ${d.consumables_used}</div>
          </div>
        `;
        await loadTelemetry();
        await loadPatientAnatomy(p);
        if (d.chat_prompt) showCanonicalPrompt(d.chat_prompt);
      } catch (e) { res.innerHTML = `<span style="color:var(--crimson-light);">Error: ${e.message}</span>`; }
    }

    async function craftCybernetic(implantKey) {
      const res = document.getElementById('cybernetics-result-box');
      res.style.display = 'block';
      res.innerHTML = '<span style="color:var(--amber);">[CALIBRANDO TORNO & UNIDAD LÓGICA DE KHEPRA-9...]</span>';

      try {
        const resp = await fetch('/api/medicae/craft_cybernetic', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ implant_key: implantKey, available_credits: availableCredits, tech_skill: 65 })
        });
        const d = await resp.json();
        if (resp.ok && d.success) {
          availableCredits = d.remaining_credits;
          document.getElementById('badge-credits').textContent = availableCredits + ' ¤ DISPONIBLES';
          document.getElementById('pc-credits').textContent = availableCredits + ' Créditos (+300 pendientes)';
          res.innerHTML = `<div class="upgrade-box" style="border-color:var(--green-auspex); color:var(--green-auspex); font-weight:700;">${d.message}</div>`;
          await loadTelemetry();
          if (d.chat_prompt) showCanonicalPrompt(d.chat_prompt);
        } else {
          res.innerHTML = `<div class="upgrade-box" style="border-color:var(--crimson-light); color:var(--crimson-light);">${d.error || 'Fallo'}</div>`;
        }
      } catch (e) { res.innerHTML = `<span style="color:var(--crimson-light);">Error: ${e.message}</span>`; }
    }

    async function synthesizeCompound(key) {
      const res = document.getElementById('alchemy-result-box');
      res.style.display = 'block';
      res.innerHTML = '<span style="color:var(--amber);">[CALENTANDO REACTORES Y CONDENSADORES...]</span>';

      try {
        const resp = await fetch('/api/alchemy/synthesize', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ compound_key: key, medic_skill: 65, available_credits: availableCredits })
        });
        const d = await resp.json();
        if (resp.ok && d.success) {
          availableCredits = d.remaining_credits;
          document.getElementById('badge-credits').textContent = availableCredits + ' ¤ DISPONIBLES';
          document.getElementById('pc-credits').textContent = availableCredits + ' Créditos (+300 pendientes)';
          res.innerHTML = `<div class="upgrade-box" style="border-color:var(--green-auspex); color:var(--green-auspex); font-weight:700;">${d.message}</div>`;
          await loadTelemetry();
          if (d.chat_prompt) showCanonicalPrompt(d.chat_prompt);
        } else {
          res.innerHTML = `<div class="upgrade-box" style="border-color:var(--crimson-light); color:var(--crimson-light);">${d.error || 'Fallo'}</div>`;
        }
      } catch (e) { res.innerHTML = `<span style="color:var(--crimson-light);">Error: ${e.message}</span>`; }
    }

    // ==========================================
    // CONTRACTS & BLACK MARKET METHODS
    // ==========================================
    async function loadContractsAndMarket() {
      const cBox = document.getElementById('contracts-container');
      try {
        const resp = await fetch('/api/factions/contracts', { headers: { 'x-api-key': API_KEY } });
        if (resp.ok) {
          const d = await resp.json();
          cBox.innerHTML = '';
          (d.contracts || []).forEach(c => {
            const card = document.createElement('div');
            card.className = 'char-card';
            card.innerHTML = `
              <div class="char-card-header">
                <span>${c.title}</span>
                <span class="stat-val green">+${c.reward_credits} ¤</span>
              </div>
              <div class="char-role">${c.faction_name} · Recompensa: +${c.reward_favors} Favor</div>
              <div class="char-status">${c.description}</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="completeContract('${c.id}')" ${c.status === 'COMPLETADO' ? 'disabled' : ''}>
                ${c.status === 'COMPLETADO' ? '✅ COMPLETADO' : '🏆 ENTREGAR CONTRATO'}
              </button>
            `;
            cBox.appendChild(card);
          });
        }
      } catch (e) { console.error(e); }

      const mBox = document.getElementById('market-items-container');
      try {
        const respM = await fetch('/api/market/items', { headers: { 'x-api-key': API_KEY } });
        if (respM.ok) {
          const dM = await respM.json();
          mBox.innerHTML = '';
          (dM.items || []).forEach(i => {
            const card = document.createElement('div');
            card.className = 'char-card';
            card.innerHTML = `
              <div class="char-card-header">
                <span>${i.name}</span>
                <span class="stat-val green">${i.price} ¤</span>
              </div>
              <div class="char-role">${i.category}</div>
              <div class="char-status">${i.effect}</div>
              <button class="btn-synth" style="margin-top:0.4rem;" onclick="buyMarketItem('${i.id}')">🛒 COMPRAR LOTE</button>
            `;
            mBox.appendChild(card);
          });
        }
      } catch (e) { console.error(e); }
    }

    async function completeContract(contractId) {
      try {
        const resp = await fetch('/api/factions/complete_contract', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ contract_id: contractId, current_credits: availableCredits })
        });
        const d = await resp.json();
        if (resp.ok && d.success) {
          availableCredits = d.new_credits;
          document.getElementById('badge-credits').textContent = availableCredits + ' ¤ DISPONIBLES';
          document.getElementById('pc-credits').textContent = availableCredits + ' Créditos (+300 pendientes)';
          alert(d.message);
          await loadFactions();
          await loadContractsAndMarket();
          await loadTelemetry();
          if (d.chat_prompt) showCanonicalPrompt(d.chat_prompt);
        } else { alert(d.error || 'Error completando contrato'); }
      } catch (e) { alert(e.message); }
    }

    async function buyMarketItem(itemId) {
      try {
        const resp = await fetch('/api/market/buy', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ item_id: itemId, current_credits: availableCredits })
        });
        const d = await resp.json();
        if (resp.ok && d.success) {
          availableCredits = d.remaining_credits;
          document.getElementById('badge-credits').textContent = availableCredits + ' ¤ DISPONIBLES';
          document.getElementById('pc-credits').textContent = availableCredits + ' Créditos (+300 pendientes)';
          alert(d.message);
          await loadTelemetry();
          if (d.chat_prompt) showCanonicalPrompt(d.chat_prompt);
        } else { alert(d.error || 'Error al comprar'); }
      } catch (e) { alert(e.message); }
    }

    async function executeRoll() {
      const act = document.getElementById('roll-action').value;
      const attr = parseInt(document.getElementById('roll-attr').value);
      const mod = parseInt(document.getElementById('roll-mod').value);
      const actor = document.getElementById('roll-actor').value;
      const res = document.getElementById('roll-result');

      res.style.display = 'block';
      res.innerHTML = '<span style="color:var(--amber);">[CONSULTANDO MOTOR DETERMINISTA REST API...]</span>';

      try {
        const resp = await fetch('/api/action', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_input: act, actor: actor, target_stat: attr, modifier: mod })
        });
        const d = await resp.json();
        const outcome = d.outcome || {};
        const success = outcome.success;
        res.innerHTML = `
          <div style="font-size:0.95rem; font-weight:800; color:${success ? 'var(--green-auspex)' : 'var(--crimson-light)'};">
            ${success ? '✅ ÉXITO DETERMINISTA' : '❌ FALLO DETERMINISTA'} (d100: ${outcome.roll} vs Objetivo: ${outcome.target_number || (attr + mod)})
          </div>
          <div style="font-size:0.8rem; color:var(--text-main); margin-top:0.35rem;">Grados: ${outcome.degrees_of_success || outcome.degrees_of_failure || 0} | Efecto: ${d.resolution || 'Acción completada.'}</div>
        `;
        showCanonicalPrompt(
          `[TIRADA DETERMINISTA // SISTEMA WH40K]\n` +
          `Actor: ${actor}\n` +
          `Acción Declarada: ${act}\n` +
          `Resultado d100: ${outcome.roll} vs Objetivo ${attr + mod} (${outcome.degrees_of_success || outcome.degrees_of_failure || 0} Grados de ${success ? 'Éxito' : 'Fallo'})\n` +
          `Resolución: ${d.resolution || 'Completado.'}`
        );
      } catch (e) { res.innerHTML = `<span style="color:var(--crimson-light);">Error: ${e.message}</span>`; }
    }

    // ==========================================
    // STANDARD DASHBOARD METHODS
    // ==========================================
    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      
      const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
      if (targetBtn) targetBtn.classList.add('active');
      
      const targetContent = document.getElementById(tabId);
      if (targetContent) targetContent.classList.add('active');

      if (tabId === 'tab-radar') initRadar();
      if (tabId === 'tab-medicae') loadPatientAnatomy('Quartus Holt');
      if (tabId === 'tab-factions') {
        loadFactions();
        loadContractsAndMarket();
      }
      if (tabId === 'tab-docs') {
        const activeDocBtn = document.querySelector('.doc-btn.active') || document.querySelector('.doc-btn');
        if (activeDocBtn) activeDocBtn.click();
      }
    }

    async function loadStateHeader() {
      try {
        const resp = await fetch('/api/state', { headers: { 'x-api-key': API_KEY } });
        if (resp.ok) {
          const data = await resp.json();
          const sheet = data.character_sheet || {};
          const recursos = sheet.recursos_economicos || {};
          if (recursos.creditos_disponibles !== undefined) {
            availableCredits = recursos.creditos_disponibles;
            document.getElementById('badge-credits').textContent = availableCredits + ' ¤ DISPONIBLES';
            document.getElementById('pc-credits').textContent = availableCredits + ' Créditos (+300 pendientes)';
            const hCred = document.getElementById('hud-alex-credits');
            if (hCred) hCred.textContent = `💰 ${availableCredits} ¤`;
          }
          if (sheet.salud_actual !== undefined) {
            document.getElementById('pc-hp').textContent = `${sheet.salud_actual} / ${sheet.salud_maxima || 12}`;
            const hHp = document.getElementById('hud-alex-hp');
            if (hHp) hHp.textContent = `❤️ ${sheet.salud_actual}/${sheet.salud_maxima || 12} PV`;
          }
          if (sheet.reserva_almas !== undefined) {
            document.getElementById('badge-souls').textContent = `${sheet.reserva_almas} ALMAS`;
            document.getElementById('pc-souls').textContent = `${sheet.reserva_almas} Almas`;
            const hSouls = document.getElementById('hud-alex-souls');
            if (hSouls) hSouls.textContent = `🔮 ${sheet.reserva_almas} Almas`;
          }
        }
      } catch (e) { console.error(e); }

      try {
        const respEv = await fetch('/api/chat/live_events', { headers: { 'x-api-key': API_KEY } });
        if (respEv.ok) {
          const dEv = await respEv.json();
          const pts = dEv.patients || {};
          if (pts['Quartus Holt']) {
            const hQ = document.getElementById('hud-quartus-hp');
            if (hQ) hQ.textContent = `Quartus: ${pts['Quartus Holt'].hp}/11 PV [C-03]`;
          }
          if (pts['Tertius Holt']) {
            const hT = document.getElementById('hud-tertius-hp');
            if (hT) hT.textContent = `Tertius: ${pts['Tertius Holt'].hp}/11 PV [C-01]`;
          }
        }
      } catch (e) { console.error(e); }
    }

    async function changeFloor(floor) {
      currentFloor = floor;
      document.getElementById('btn-floor-0').classList.toggle('active', floor === 0);
      document.getElementById('btn-floor-sub1').classList.toggle('active', floor === -1);
      document.getElementById('current-floor-title').textContent = floor === 0 ? 'PLANTA 0 (CLÍNICA RHO-9)' : 'SUBNIVEL -1 (CRIPTAS INEXPLORADAS)';
      await loadBlueprint();
    }

    async function loadBlueprint() {
      const container = document.getElementById('blueprint-grid-container');
      try {
        const resp = await fetch(`/api/domain/blueprint?floor=${currentFloor}`, {
          headers: { 'x-api-key': API_KEY }
        });
        if (resp.ok) {
          const data = await resp.json();
          if (data.global_metrics && currentFloor === 0) {
            document.getElementById('metric-defensa').textContent = data.global_metrics.defensa_perimetral + '%';
            document.getElementById('bar-defensa').style.width = data.global_metrics.defensa_perimetral + '%';
            document.getElementById('metric-sanidad').textContent = data.global_metrics.calidad_sanitaria + '%';
            document.getElementById('bar-sanidad').style.width = data.global_metrics.calidad_sanitaria + '%';
          }
          renderBlueprint(data.sectors);
        }
      } catch (err) { console.error(err); }
    }

    function renderBlueprint(sectors) {
      const container = document.getElementById('blueprint-grid-container');
      container.innerHTML = '';

      sectors.forEach((sec) => {
        const card = document.createElement('div');
        const isFog = (sec.type === 'fog' || sec.status === 'NIEBLA_DE_GUERRA');
        const colSpan = (currentFloor === -1) ? 'span 6' : ((sec.id === 'GATE-01' || sec.id === 'COMM-01' || sec.id === 'SUB-01') ? 'span 6' : 'span 4');

        card.className = `room-card ${isFog ? 'fog-of-war' : ''}`;
        card.style.gridColumn = colSpan;
        card.onclick = () => openRoomModal(sec);

        let statusDotColor = 'var(--green-auspex)';
        if (sec.status_color === 'amber') statusDotColor = 'var(--amber)';
        if (sec.status_color === 'crimson') statusDotColor = 'var(--crimson-light)';
        if (sec.status_color === 'cyan') statusDotColor = 'var(--cyan-plasma)';
        if (sec.status_color === 'text-dim') statusDotColor = 'var(--text-dim)';

        const vitalTag = sec.is_vital ? '<span style="color:var(--brass); margin-left:0.3rem;">[VITAL · 5 TIERS]</span>' : '';

        card.innerHTML = `
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span class="room-code-tag">${sec.code} ${vitalTag}</span>
              <span style="font-size:0.7rem; color:var(--text-muted);"><span class="room-status-dot" style="background:${statusDotColor};"></span>${sec.status}</span>
            </div>
            <div class="room-name">${sec.name}</div>
            <div class="room-level-badge">${sec.level_title} (Nvl ${sec.level}/${sec.max_level || 3})</div>
          </div>
          <div class="room-occupants-mini">${isFog ? '🔍 ' + (sec.exploration_cost || 'Por explorar') : '👥 ' + sec.occupants.join(', ')}</div>
        `;

        container.appendChild(card);
      });
    }

    function openRoomModal(sec) {
      currentSelectedRoom = sec;
      const feedback = document.getElementById('modal-feedback');
      feedback.style.display = 'none';

      document.getElementById('modal-room-code').textContent = `${sec.code} // SECTOR DE ${sec.type.toUpperCase()} ${sec.is_vital ? '(SALA VITAL · MÁX 5 NIVELES)' : '(SALA ESTÁNDAR · MÁX 3 NIVELES)'}`;
      document.getElementById('modal-room-name').textContent = sec.name;
      document.getElementById('modal-room-level').textContent = `${sec.level_title} (Nivel ${sec.level} de ${sec.max_level || 3})`;
      document.getElementById('modal-room-occupants').textContent = sec.occupants ? sec.occupants.join(' · ') : 'Ninguno';
      document.getElementById('modal-room-equipment').textContent = sec.equipment ? sec.equipment.join(', ') : 'Ninguno';
      document.getElementById('modal-room-bonus').textContent = sec.bonus || 'Sin bonificación especial';

      const upgSection = document.getElementById('modal-upgrade-section');
      const expSection = document.getElementById('modal-explore-section');

      if (currentFloor === -1 && sec.status === 'NIEBLA_DE_GUERRA') {
        upgSection.style.display = 'none';
        expSection.style.display = 'block';
        document.getElementById('modal-explore-cost').textContent = 'Requisito: ' + (sec.exploration_cost || '1 Turno');
      } else if (sec.next_upgrade) {
        upgSection.style.display = 'block';
        expSection.style.display = 'none';
        document.getElementById('modal-upgrade-title').textContent = '🚀 ' + sec.next_upgrade.title;
        document.getElementById('modal-upgrade-effect').textContent = 'Efecto: ' + sec.next_upgrade.effect;
        document.getElementById('modal-upgrade-credits').textContent = sec.next_upgrade.cost_credits + ' Créditos';
        document.getElementById('modal-upgrade-mats').textContent = sec.next_upgrade.cost_mats || sec.next_upgrade.cost_materials || '-';
        document.getElementById('btn-execute-upgrade').style.display = 'block';
      } else {
        upgSection.style.display = 'block';
        expSection.style.display = 'none';
        document.getElementById('modal-upgrade-title').textContent = `⭐ Nivel Máximo Alcanzado (Nivel ${sec.max_level || 3})`;
        document.getElementById('modal-upgrade-effect').textContent = 'Esta sala está plenamente desarrollada en su tier máximo.';
        document.getElementById('modal-upgrade-credits').textContent = '0 ¤';
        document.getElementById('modal-upgrade-mats').textContent = 'Ninguno';
        document.getElementById('btn-execute-upgrade').style.display = 'none';
      }

      document.getElementById('room-modal').style.display = 'flex';
    }

    async function executeUpgrade() {
      if (!currentSelectedRoom) return;
      const feedback = document.getElementById('modal-feedback');
      feedback.style.display = 'block';
      feedback.innerHTML = '<span style="color:var(--amber);">[EJECUTANDO MEJORA...]</span>';

      try {
        const resp = await fetch('/api/domain/upgrade', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ room_id: currentSelectedRoom.id, available_credits: availableCredits })
        });
        const data = await resp.json();
        if (resp.ok && data.success) {
          availableCredits = data.remaining_credits;
          document.getElementById('badge-credits').textContent = availableCredits + ' ¤ DISPONIBLES';
          document.getElementById('pc-credits').textContent = availableCredits + ' Créditos (+300 pendientes)';
          feedback.innerHTML = `<span style="color:var(--green-auspex); font-weight:700;">✅ ${data.message}</span>`;
          await loadBlueprint();
          await loadTelemetry();
          showCanonicalPrompt(
            `[MEJORA ARQUITECTÓNICA // COGITADOR RHO-9]\n` +
            `Sector Desarrollado: ${currentSelectedRoom.name} (${currentSelectedRoom.code})\n` +
            `Nuevo Nivel: ${data.new_level}\n` +
            `Créditos Restantes: ${data.remaining_credits} ¤\n` +
            `Métricas Base: Defensa ${document.getElementById('metric-defensa').textContent} | Sanidad ${document.getElementById('metric-sanidad').textContent}`
          );
          setTimeout(() => { document.getElementById('room-modal').style.display = 'none'; }, 1800);
        } else {
          feedback.innerHTML = `<span style="color:var(--crimson-light);">❌ ${data.error || 'Error'}</span>`;
        }
      } catch (err) { feedback.innerHTML = `<span style="color:var(--crimson-light);">❌ ${err.message}</span>`; }
    }

    async function executeExploration() {
      if (!currentSelectedRoom) return;
      const feedback = document.getElementById('modal-feedback');
      feedback.style.display = 'block';
      feedback.innerHTML = '<span style="color:var(--cyan-plasma);">[EXPLORANDO SUBNIVEL...]</span>';

      try {
        const resp = await fetch('/api/domain/explore_step', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ sector_id: currentSelectedRoom.id, actor: 'Alexander' })
        });
        const data = await resp.json();
        if (resp.ok && data.success) {
          feedback.innerHTML = `<span style="color:var(--cyan-plasma); font-weight:700;">✅ ${data.message}</span>`;
          await loadBlueprint();
          await loadTelemetry();
          showCanonicalPrompt(
            `[EXPLORACIÓN DE SUBNIVEL // COGITADOR RHO-9]\n` +
            `Alexander ha explorado y asegurado: ${currentSelectedRoom.name} (${currentSelectedRoom.code}).\n` +
            `Sector despejado de la niebla de guerra.\n` +
            `Nuevo Bono Activado: ${currentSelectedRoom.bonus || 'Acceso asegurado'}`
          );
          setTimeout(() => { document.getElementById('room-modal').style.display = 'none'; }, 1800);
        } else {
          feedback.innerHTML = `<span style="color:var(--crimson-light);">❌ ${data.error || 'Error'}</span>`;
        }
      } catch (err) { feedback.innerHTML = `<span style="color:var(--crimson-light);">❌ ${err.message}</span>`; }
    }

    async function loadFactions() {
      const c = document.getElementById('factions-container');
      try {
        const resp = await fetch('/api/factions/status', { headers: { 'x-api-key': API_KEY } });
        if (resp.ok) {
          const d = await resp.json();
          c.innerHTML = '';
          (d.factions || []).forEach(f => {
            const card = document.createElement('div');
            card.className = 'char-card';
            card.innerHTML = `
              <div class="char-card-header">
                <span>${f.name}</span>
                <span class="stat-val ${f.stance_color}">Reputación: ${f.reputation >= 0 ? '+' + f.reputation : f.reputation}</span>
              </div>
              <div class="char-role">${f.stance} · Favores Disponibles: <strong>${f.favors_available}</strong></div>
              <div style="margin-top:0.4rem; display:flex; flex-direction:column; gap:0.3rem;">
                ${f.claimable_perks.map(p => `
                  <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; background:#0b0e14; padding:0.3rem 0.5rem; border-radius:3px;">
                    <span>${p.title} (${p.effect})</span>
                    <button class="btn-synth" onclick="claimFactionFavor('${f.key}', '${p.id}')">COBRAR (${p.cost_favors} F)</button>
                  </div>
                `).join('')}
              </div>
            `;
            c.appendChild(card);
          });
        }
      } catch (e) { console.error(e); }
    }

    async function claimFactionFavor(factionKey, perkId) {
      try {
        const resp = await fetch('/api/factions/claim_favor', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ faction_key: factionKey, perk_id: perkId })
        });
        const d = await resp.json();
        alert(d.message || (d.success ? 'Favor cobrado' : d.error));
        await loadFactions();
        await loadTelemetry();
        if (d.chat_prompt) showCanonicalPrompt(d.chat_prompt);
      } catch (e) { alert(e.message); }
    }

    async function assignStaff(npcName, task) {
      try {
        await fetch('/api/domain/assign', {
          method: 'POST',
          headers: { 'x-api-key': API_KEY, 'Content-Type': 'application/json' },
          body: JSON.stringify({ npc_name: npcName, task: task })
        });
        await loadTelemetry();
      } catch (err) { console.error(err); }
    }

    async function loadTelemetry() {
      const container = document.getElementById('telemetry-feed-container');
      try {
        const resp = await fetch('/api/domain/logs', { headers: { 'x-api-key': API_KEY } });
        if (resp.ok) {
          const data = await resp.json();
          container.innerHTML = '';
          (data.logs || []).forEach(l => {
            const entry = document.createElement('div');
            entry.className = 'feed-entry';
            entry.innerHTML = `<span class="feed-time">[${l.time}]</span><span class="feed-tag ${l.type}">${l.type}</span>${l.text}`;
            container.appendChild(entry);
          });
        }
      } catch (err) { console.error(err); }
    }

    async function loadDocument(name, btn) {
      document.querySelectorAll('.doc-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      const viewer = document.getElementById('doc-content');
      viewer.textContent = `[COGITADOR] Cargando ${name}.txt...`;

      try {
        const resp = await fetch(`/api/documents/${name}`, { headers: { 'x-api-key': API_KEY } });
        if (resp.ok) {
          const data = await resp.json();
          viewer.textContent = data.content || "[Archivo vacío]";
        }
      } catch (err) { viewer.textContent = err.message; }
    }

    function closeRoomModal(e) {
      if (e.target.id === 'room-modal') document.getElementById('room-modal').style.display = 'none';
    }

    function filterInventory() {
      const q = document.getElementById('inv-search').value.toLowerCase();
      document.querySelectorAll('.inv-item-card').forEach(card => {
        card.style.display = card.textContent.toLowerCase().includes(q) ? 'block' : 'none';
      });
    }

    window.addEventListener('DOMContentLoaded', () => {
      updateClockDisplay();
      loadStateHeader();
      loadBlueprint();
      loadTelemetry();
      loadPatientAnatomy('Quartus Holt');
      loadDocument('FICHA_DEL_PERSONAJE');
    });
  </script>
</body>
</html>
"""
