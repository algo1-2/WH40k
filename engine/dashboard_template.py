"""
WH40K TACTICAL COMMAND COGITATOR — WEB DASHBOARD TEMPLATE v2.0
Includes Interactive Architectural Blueprint & Base Expansion / Upgrades Panel
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
    }

    header {
      background: #0b0e12;
      border-bottom: 2px solid var(--brass-dim);
      padding: 1rem 1.5rem;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      box-shadow: 0 2px 15px rgba(0, 0, 0, 0.7);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .aquila-icon {
      font-size: 1.8rem;
      color: var(--brass);
      text-shadow: 0 0 10px var(--amber-glow);
    }

    .brand-title {
      font-family: 'Cinzel', serif;
      font-size: 1.3rem;
      font-weight: 900;
      letter-spacing: 2px;
      color: var(--brass);
      text-transform: uppercase;
    }

    .brand-sub {
      font-size: 0.75rem;
      color: var(--text-dim);
      letter-spacing: 1px;
    }

    .status-badge-container {
      display: flex;
      gap: 0.75rem;
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

    @keyframes pulse {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
      100% { opacity: 1; transform: scale(1); }
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
      font-size: 0.85rem;
      font-weight: 600;
      padding: 0.85rem 1.25rem;
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

    /* BLUEPRINT TACTICAL GRID */
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

    .room-card.active-selected {
      border-color: var(--brass);
      box-shadow: 0 0 12px var(--amber-glow);
      background: #161e2b;
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

    .search-input:focus {
      outline: none;
      border-color: var(--brass);
      box-shadow: 0 0 8px var(--amber-glow);
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

    .dice-form {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      margin-bottom: 1rem;
    }

    @media (max-width: 640px) {
      .dice-form { grid-template-columns: 1fr; }
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
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

    .btn-roll {
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
      grid-column: 1 / -1;
    }

    .btn-roll:hover {
      background: linear-gradient(135deg, #c99a3e, #f59e0b);
      box-shadow: 0 4px 20px rgba(245, 158, 11, 0.5);
      transform: translateY(-1px);
    }

    .roll-result-box {
      background: #0a0d12;
      border: 1px dashed var(--border-panel);
      border-radius: 4px;
      padding: 1.25rem;
      margin-top: 1rem;
      font-size: 0.85rem;
      display: none;
    }

    .roll-success {
      border-color: var(--green-auspex);
      background: rgba(16, 185, 129, 0.05);
    }

    .roll-failure {
      border-color: var(--crimson-light);
      background: rgba(239, 68, 68, 0.05);
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
    <div class="status-badge-container">
      <div class="badge badge-live">API EN LÍNEA</div>
      <div class="badge badge-brass" id="badge-revision">REVISIÓN: 17</div>
      <div class="badge badge-brass" id="badge-souls">ALMAS: 10</div>
    </div>
  </header>

  <nav class="tab-nav">
    <button class="tab-btn active" onclick="switchTab('tab-blueprint')">🗺️ PLANO & MEJORAS RHO-9</button>
    <button class="tab-btn" onclick="switchTab('tab-status')">⚙️ ESTADO DE CAMPAÑA</button>
    <button class="tab-btn" onclick="switchTab('tab-inventory')">📦 SOMBRA INFINITA & ARSENAL</button>
    <button class="tab-btn" onclick="switchTab('tab-roller')">🎲 SIMULADOR DE TIRADAS d100</button>
    <button class="tab-btn" onclick="switchTab('tab-docs')">📜 DOSSIERS Y CRÓNICAS</button>
  </nav>

  <main class="container">

    <!-- TAB 0: BLUEPRINT & BASE UPGRADES -->
    <section id="tab-blueprint" class="tab-content active">
      
      <!-- Metrics overview bar -->
      <div class="blueprint-metrics-bar">
        <div class="panel" style="padding:1rem;">
          <div class="stat-label">🛡️ Fortaleza Perimetral</div>
          <div class="stat-val brass" style="font-size:1.2rem; margin-top:0.25rem;">75%</div>
          <div class="progress-bar-bg"><div class="progress-fill fill-brass" style="width: 75%;"></div></div>
        </div>
        <div class="panel" style="padding:1rem;">
          <div class="stat-label">🧼 Calidad Sanitaria</div>
          <div class="stat-val amber" style="font-size:1.2rem; margin-top:0.25rem;">65%</div>
          <div class="progress-bar-bg"><div class="progress-fill fill-amber" style="width: 65%;"></div></div>
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

      <!-- Tactical Grid Blueprint -->
      <div class="panel" style="margin-bottom:1.5rem;">
        <div class="panel-header">
          <span class="panel-title">🗺️ AUSPEX ARQUITECTÓNICO // MEDICAE STATION RHO-9</span>
          <span class="badge badge-brass">HAZ CLIC EN UNA SALA PARA VER DETALLES Y MEJORAS</span>
        </div>
        <div class="panel-body">
          
          <div class="blueprint-grid" id="blueprint-grid-container">
            <!-- Rooms rendered dynamically via JS -->
          </div>

        </div>
      </div>

    </section>

    <!-- TAB 1: ESTADO DE CAMPAÑA -->
    <section id="tab-status" class="tab-content">
      <div class="grid-dashboard">
        
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">🛡️ ALEXANDER // OPERADOR UMBRAL</span>
            <span class="badge badge-brass">NIVEL 5</span>
          </div>
          <div class="panel-body">
            <div class="stat-row">
              <span class="stat-label">❤️ Salud Vital:</span>
              <span class="stat-val green" id="pc-hp">12 / 12</span>
            </div>
            <div class="progress-bar-bg"><div class="progress-fill fill-green" style="width: 100%;"></div></div>

            <div class="stat-row" style="margin-top: 0.75rem;">
              <span class="stat-label">⚡ Fatiga:</span>
              <span class="stat-val" id="pc-fatigue">0 / 7</span>
            </div>
            <div class="progress-bar-bg"><div class="progress-fill fill-amber" style="width: 0%;"></div></div>

            <div class="stat-row" style="margin-top: 0.75rem;">
              <span class="stat-label">🔮 Reserva Umbral:</span>
              <span class="stat-val brass" id="pc-souls">10 Almas</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">🌟 Puntos de Destino:</span>
              <span class="stat-val brass">3</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">💰 Saldo Disponible:</span>
              <span class="stat-val green">1.196 Créditos (+300 pendientes)</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">📈 Experiencia Total:</span>
              <span class="stat-val">1.335 XP (335 / 500)</span>
            </div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">🏥 MEDICAE STATION RHO-9</span>
            <span class="badge badge-live">OPERATIVA</span>
          </div>
          <div class="panel-body">
            <div class="stat-row">
              <span class="stat-label">📍 Ubicación:</span>
              <span class="stat-val" style="font-size:0.75rem;">Caídas de Polvo / Dust Falls</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">🛡️ Seguridad:</span>
              <span class="stat-val brass">Severan Holt (Cap: 200 ¤/sem)</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">🚪 Estado Base:</span>
              <span class="stat-val amber">Cerrada al Público / Cuarentena</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">🍖 Raciones Comunes:</span>
              <span class="stat-val">24 raciones</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">🎖️ Raciones Militares / Médicas:</span>
              <span class="stat-val">10 Militares · 9 Médicas · 5 Alta Nutrición</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">💧 Agua Potable:</span>
              <span class="stat-val green">16 Botellas (1L)</span>
            </div>
          </div>
        </div>

        <div class="panel" style="grid-column: 1 / -1;">
          <div class="panel-header">
            <span class="panel-title">👥 SÉQUITO, PACIENTES Y PACTOS ACTIVOS</span>
            <span class="badge badge-brass">CENSO RHO-9</span>
          </div>
          <div class="panel-body" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.75rem;">
            
            <div class="char-card">
              <div class="char-card-header">
                <span>Tertius Holt</span>
                <span class="stat-val green">8 / 11 · Despierto</span>
              </div>
              <div class="char-role">Especialista Enforcer / Deudor</div>
              <div class="char-status">Consciente y estable. Drenaje torácico funcional; puede conversar. Pregunta por su deuda.</div>
            </div>

            <div class="char-card">
              <div class="char-card-header">
                <span>Quartus Holt</span>
                <span class="stat-val crimson">4 / 11 · En Coma</span>
              </div>
              <div class="char-role">Paciente Crítico / C-03</div>
              <div class="char-status">Crítico estable. Inconsciente e intubado por metralla a quemarropa (&lt;3m).</div>
            </div>

            <div class="char-card">
              <div class="char-card-header">
                <span>Halven Rusk</span>
                <span class="stat-val brass">Pacto de Cosecha</span>
              </div>
              <div class="char-role">Auxiliar Médico / Diagnosticador</div>
              <div class="char-status">Activo. Ejecutó personalmente a los 4 cautivos en Rho-9 (+4 almas transferidas a Alexander).</div>
            </div>

            <div class="char-card">
              <div class="char-card-header">
                <span>Severan Holt</span>
                <span class="stat-val green">Maestro de Seguridad</span>
              </div>
              <div class="char-role">Comando Táctico y Accesos</div>
              <div class="char-status">A cargo de cerraduras, guardias y fortificación. Asistente operativo: Jarek Venn.</div>
            </div>

            <div class="char-card">
              <div class="char-card-header">
                <span>Jarek Venn</span>
                <span class="stat-val amber">0 / 9 · Débil</span>
              </div>
              <div class="char-role">Primer Deudor E-12</div>
              <div class="char-status">Extraído de Sombra. Torso reparado. Asignado a Severan (Pacto: 0/10 ejecuciones + 1 año de trabajo).</div>
            </div>

            <div class="char-card">
              <div class="char-card-header">
                <span>Syra Kol</span>
                <span class="stat-val green">16 Años · ADM-01</span>
              </div>
              <div class="char-role">Auxiliar Logística y Registros</div>
              <div class="char-status">A cargo de la contabilidad de consumibles, medicamentos y gastos autorizados.</div>
            </div>

          </div>
        </div>

      </div>
    </section>

    <!-- TAB 2: SOMBRA INFINITA -->
    <section id="tab-inventory" class="tab-content">
      <div class="filter-bar">
        <input type="text" id="inv-search" class="search-input" placeholder="🔍 Filtrar armas, fármacos, consumibles, herramientas o muestras..." onkeyup="filterInventory()">
      </div>

      <div class="panel" style="margin-bottom: 1.5rem;">
        <div class="panel-header">
          <span class="panel-title">⚔️ ARMAS Y BOTÍN DE LA INCURSIÓN NOCTURNA</span>
          <span class="badge badge-brass">SOMBRA INFINITA</span>
        </div>
        <div class="panel-body">
          <div class="inv-category-grid" id="weapons-grid">
            
            <div class="inv-item-card">
              <div class="inv-item-title"><span>P-01 // Pistola Compacta Hesh-9</span><span class="badge badge-brass">8 / 8</span></div>
              <div class="inv-item-detail">D4 | Pen 0 | Alcance 20m | Compacta / Ocultable / Simple</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>P-02 // Pistola Servicio Mk II</span><span class="badge badge-brass">12 / 12</span></div>
              <div class="inv-item-detail">D5 | Pen 0 | Alcance 30m | Fiable | Patrón Servicio</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>P-03 // Pistola Servicio Mk II</span><span class="badge badge-brass">12 / 12</span></div>
              <div class="inv-item-detail">D5 | Pen 0 | Alcance 30m | Fiable | Patrón Servicio</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>P-04 // Autopistola Vex</span><span class="badge badge-brass">18 / 18</span></div>
              <div class="inv-item-detail">D4 | Pen 0 | Alcance 25m | Ráfaga 3 / Automática / Compacta</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>P-05 // Pistola Pesada Brakk</span><span class="badge badge-brass">8 / 8</span></div>
              <div class="inv-item-detail">D6 | Pen 1 | Alcance 25m | Retroceso Fuerte / Pesada</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>L-01 // Carabina Kord-24</span><span class="badge badge-brass">24 / 24</span></div>
              <div class="inv-item-detail">D5 | Pen 0 | Alcance 60m | Carabina / Fiable | Ráfaga 3</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>L-02 // Carabina Kord-24</span><span class="badge badge-brass">24 / 24</span></div>
              <div class="inv-item-detail">D5 | Pen 0 | Alcance 60m | Carabina / Fiable | Ráfaga 3</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>L-03 // Escopeta Compacta</span><span class="badge badge-brass">6 / 6</span></div>
              <div class="inv-item-detail">D6 | Pen 0 | Alcance 30m | Dispersión / Potente a Corta Distancia</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>L-04 // Autogun Patrón Reth</span><span class="badge badge-brass">30 / 30</span></div>
              <div class="inv-item-detail">D5 | Pen 0 | Alcance 80m | Automática / Ráfaga 3</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>L-05 // Rifle Precisión Manufactorum</span><span class="badge badge-brass">10 / 10</span></div>
              <div class="inv-item-detail">D6 | Pen 1 | Alcance 120m | Precisa / Lenta</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>Caja Reforzada de Explosivos</span><span class="badge badge-brass">6 Granadas</span></div>
              <div class="inv-item-detail">3 Granadas Frag · 2 Granadas de Humo · 1 Granada Krak</div>
            </div>

            <div class="inv-item-card">
              <div class="inv-item-title"><span>Reserva de Munición Suelta</span><span class="badge badge-green">1.000+ Proyectiles</span></div>
              <div class="inv-item-detail">Pistola (240) · Kord-24 (312) · Autogun (240) · Escopeta (120 + 8 incendiarios)</div>
            </div>

          </div>
        </div>
      </div>

      <div class="grid-dashboard">
        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">💉 FÁRMACOS Y CONSUMIBLES</span>
          </div>
          <div class="panel-body">
            <div class="stat-row"><span class="stat-label">Antibióticos amplio espectro:</span><span class="stat-val">36 dosis</span></div>
            <div class="stat-row"><span class="stat-label">Analgésicos clínicos:</span><span class="stat-val">48 dosis</span></div>
            <div class="stat-row"><span class="stat-label">Sedantes / Anestésicos:</span><span class="stat-val">30 sedantes · 18 generales · 24 locales</span></div>
            <div class="stat-row"><span class="stat-label">Coagulantes inyectables:</span><span class="stat-val">30 dosis</span></div>
            <div class="stat-row"><span class="stat-label">Fluidos IV (Salina / Electrolitos / Sangre):</span><span class="stat-val">32 salina · 24 nutrición · 12 sintética</span></div>
            <div class="stat-row"><span class="stat-label">Kits de recarga de Medikit:</span><span class="stat-val brass">12 recargas completas</span></div>
            <div class="stat-row"><span class="stat-label">Apósitos, Vendas y Suturas:</span><span class="stat-val">80 apósitos · 48 vendas · 40 suturas</span></div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-header">
            <span class="panel-title">🧬 BIOBANCO & CUSTODIA VIVA</span>
          </div>
          <div class="panel-body">
            <div class="stat-row"><span class="stat-label">🩸 Unidades Sangre Transfusión:</span><span class="stat-val green">10 unidades (5 donantes)</span></div>
            <div class="stat-row"><span class="stat-label">🫀 Órganos Candidatos:</span><span class="stat-val">3 corazones · 5 pulmones · 2 hígados · 6 riñones</span></div>
            <div class="stat-row"><span class="stat-label">🦾 Brazo Segundo Deudor:</span><span class="stat-val brass">Preservado para prótesis</span></div>
            <div class="stat-row"><span class="stat-label">⚠️ Cautivos Ejecutados (Incursión):</span><span class="stat-val">4 cadáveres separados en Sombra</span></div>
            <div class="stat-row"><span class="stat-label">❄️ Vivos en Suspensión:</span><span class="stat-val amber">Op. M-01 · Sujetos I, II, III · Segundo Deudor</span></div>
            <div class="stat-row"><span class="stat-label">🔬 Muestras Biológicas Especiales:</span><span class="stat-val">Testigos 1 y 2 · Masa Khepra · M-01</span></div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 3: SIMULADOR DE TIRADAS -->
    <section id="tab-roller" class="tab-content">
      <div class="panel" style="max-width: 800px; margin: 0 auto;">
        <div class="panel-header">
          <span class="panel-title">🎲 TERMINAL DETERMINISTA DE TIRADAS (WARHAMMER 40K)</span>
          <span class="badge badge-brass">MOTOR REST API</span>
        </div>
        <div class="panel-body">
          <div class="dice-form">
            <div class="form-group">
              <label class="form-label">Acción Declarada</label>
              <input type="text" id="roll-action" class="form-control" value="Alexander ausculta y estabiliza a Tertius en Rho-9" placeholder="Descripción de la acción...">
            </div>
            <div class="form-group">
              <label class="form-label">Atributo o Habilidad Base</label>
              <select id="roll-attr" class="form-control">
                <option value="65">Medicina Clandestina (65)</option>
                <option value="68">Voluntad / Poderes Umbrales (68)</option>
                <option value="55">Habilidad de Proyectiles / Balística (55)</option>
                <option value="48">Agilidad / Sigilo (48)</option>
                <option value="52">Percepción / Diagnóstico (52)</option>
                <option value="45">Cuerpo a Cuerpo (45)</option>
                <option value="40">Resistencia (40)</option>
                <option value="38">Fuerza (38)</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Modificador Circunstancial (+/-)</label>
              <select id="roll-mod" class="form-control">
                <option value="15">+15 (Diagnostor Rho-9 / Medicina sin combate)</option>
                <option value="10">+10 (Equipo médico avanzado / Bio-auspex)</option>
                <option value="0">+0 (Condiciones estándar)</option>
                <option value="-10">-10 (Bajo presión / Luz tenue)</option>
                <option value="-20">-20 (Cirugía de trauma extremo / Oposición fuerte)</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Actor</label>
              <input type="text" id="roll-actor" class="form-control" value="Alexander">
            </div>
            <button class="btn-roll" onclick="executeRoll()">⚡ EJECUTAR TIRADA DETERMINISTA d100</button>
          </div>

          <div id="roll-result" class="roll-result-box">
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 4: DOSSIERS Y CRÓNICAS -->
    <section id="tab-docs" class="tab-content">
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">📜 ARCHIVO DE CAMPAÑA // DOSSIERS MAESTROS</span>
          <span class="badge badge-brass">AUTORIDAD CANÓNICA</span>
        </div>
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
      
      <div class="stat-row">
        <span class="stat-label">🏷️ Nivel & Estado:</span>
        <span class="stat-val brass" id="modal-room-level">Nivel 1</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">👥 Personal Presente:</span>
        <span class="stat-val" id="modal-room-occupants">-</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">🔧 Equipamiento Instalado:</span>
        <span class="stat-val" id="modal-room-equipment" style="font-size:0.78rem;">-</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">✨ Bono a la Campaña:</span>
        <span class="stat-val green" id="modal-room-bonus" style="font-size:0.78rem;">-</span>
      </div>

      <!-- Upgrade Box -->
      <div class="upgrade-box">
        <div style="font-family:'Cinzel',serif; font-size:0.9rem; font-weight:800; color:var(--amber); margin-bottom:0.5rem;" id="modal-upgrade-title">
          🚀 Siguiente Mejora Disponible
        </div>
        <div style="font-size:0.8rem; color:var(--text-main); margin-bottom:0.5rem;" id="modal-upgrade-effect">
          Efecto: -
        </div>
        <div class="stat-row" style="background:#0b0e14; padding:0.4rem 0.6rem; border-radius:4px;">
          <span class="stat-label">💰 Coste Créditos:</span>
          <span class="stat-val green" id="modal-upgrade-credits">0 ¤</span>
        </div>
        <div class="stat-row" style="background:#0b0e14; padding:0.4rem 0.6rem; border-radius:4px; margin-top:0.25rem;">
          <span class="stat-label">🔩 Materiales / Requisitos:</span>
          <span class="stat-val brass" id="modal-upgrade-mats" style="font-size:0.75rem;">-</span>
        </div>
      </div>
    </div>
  </div>

  <footer>
    WH40K NARRATIVE ENGINE · API DE PRODUCCIÓN · <span class="footer-highlight">MEDICAE STATION RHO-9</span> · NECROMUNDA
  </footer>

  <script>
    const API_KEY = "wh40k_secret_key_12345";
    let blueprintData = null;

    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      
      const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
      if (targetBtn) targetBtn.classList.add('active');
      
      const targetContent = document.getElementById(tabId);
      if (targetContent) targetContent.classList.add('active');

      if (tabId === 'tab-docs') {
        const activeDocBtn = document.querySelector('.doc-btn.active') || document.querySelector('.doc-btn');
        if (activeDocBtn) activeDocBtn.click();
      }
    }

    async function loadBlueprint() {
      const container = document.getElementById('blueprint-grid-container');
      try {
        const resp = await fetch('/api/domain/blueprint', {
          headers: { 'x-api-key': API_KEY }
        });
        if (resp.ok) {
          blueprintData = await resp.json();
          renderBlueprint(blueprintData.sectors);
        } else {
          container.innerHTML = '<div style="color:var(--crimson-light);">Error cargando plano de Rho-9.</div>';
        }
      } catch (err) {
        console.error(err);
      }
    }

    function renderBlueprint(sectors) {
      const container = document.getElementById('blueprint-grid-container');
      container.innerHTML = '';

      sectors.forEach((sec, idx) => {
        const card = document.createElement('div');
        const isFog = sec.type === 'fog';
        const colSpan = (sec.id === 'GATE-01' || sec.id === 'COMM-01' || sec.id === 'SUB-01') ? 'span 6' : 'span 4';

        card.className = `room-card ${isFog ? 'fog-of-war' : ''}`;
        card.style.gridColumn = colSpan;
        card.onclick = () => openRoomModal(sec);

        let statusDotColor = 'var(--green-auspex)';
        if (sec.status_color === 'amber') statusDotColor = 'var(--amber)';
        if (sec.status_color === 'crimson') statusDotColor = 'var(--crimson-light)';
        if (sec.status_color === 'cyan') statusDotColor = 'var(--cyan-plasma)';
        if (sec.status_color === 'text-dim') statusDotColor = 'var(--text-dim)';

        card.innerHTML = `
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span class="room-code-tag">${sec.code}</span>
              <span style="font-size:0.7rem; color:var(--text-muted);"><span class="room-status-dot" style="background:${statusDotColor};"></span>${sec.status}</span>
            </div>
            <div class="room-name">${sec.name}</div>
            <div class="room-level-badge">${sec.level_title}</div>
          </div>
          <div class="room-occupants-mini">👥 ${sec.occupants.join(', ')}</div>
        `;

        container.appendChild(card);
      });
    }

    function openRoomModal(sec) {
      document.getElementById('modal-room-code').textContent = sec.code + ' // SECTOR DE ' + sec.type.toUpperCase();
      document.getElementById('modal-room-name').textContent = sec.name;
      document.getElementById('modal-room-level').textContent = `${sec.level_title} (Nivel ${sec.level})`;
      document.getElementById('modal-room-occupants').textContent = sec.occupants.join(' · ');
      document.getElementById('modal-room-equipment').textContent = sec.equipment ? sec.equipment.join(', ') : 'Ninguno';
      document.getElementById('modal-room-bonus').textContent = sec.bonus || 'Sin bonificación especial';

      if (sec.next_upgrade) {
        document.getElementById('modal-upgrade-title').textContent = '🚀 ' + sec.next_upgrade.title;
        document.getElementById('modal-upgrade-effect').textContent = 'Efecto: ' + sec.next_upgrade.effect;
        document.getElementById('modal-upgrade-credits').textContent = sec.next_upgrade.cost_credits + ' Créditos';
        document.getElementById('modal-upgrade-mats').textContent = sec.next_upgrade.cost_materials;
      } else {
        document.getElementById('modal-upgrade-title').textContent = '⭐ Nivel Máximo Alcanzado';
        document.getElementById('modal-upgrade-effect').textContent = 'Esta sala está plenamente desarrollada.';
        document.getElementById('modal-upgrade-credits').textContent = '0 ¤';
        document.getElementById('modal-upgrade-mats').textContent = 'Ninguno';
      }

      document.getElementById('room-modal').style.display = 'flex';
    }

    function closeRoomModal(e) {
      if (e.target.id === 'room-modal') {
        document.getElementById('room-modal').style.display = 'none';
      }
    }

    async function loadDocument(name, btn) {
      document.querySelectorAll('.doc-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      
      const viewer = document.getElementById('doc-content');
      viewer.textContent = `[COGITADOR] Cargando ${name}.txt desde el archivo autoritativo...`;

      try {
        const resp = await fetch(`/api/documents/${name}`, {
          headers: { 'x-api-key': API_KEY }
        });
        if (resp.ok) {
          const data = await resp.json();
          viewer.textContent = data.content || "[Archivo vacío]";
        } else {
          viewer.textContent = `[ERROR ${resp.status}] No se pudo cargar el documento.`;
        }
      } catch (err) {
        viewer.textContent = `[ERROR DE CONEXIÓN] ${err.message}`;
      }
    }

    async function executeRoll() {
      const action = document.getElementById('roll-action').value;
      const attr = parseInt(document.getElementById('roll-attr').value);
      const mod = parseInt(document.getElementById('roll-mod').value);
      const actor = document.getElementById('roll-actor').value;
      const resBox = document.getElementById('roll-result');

      resBox.style.display = 'block';
      resBox.className = 'roll-result-box';
      resBox.innerHTML = '<span style="color:var(--amber);">[CALCULANDO TRAYECTORIA Y MATRIZ DE PROBABILIDAD d100...]</span>';

      try {
        const resp = await fetch('/api/action', {
          method: 'POST',
          headers: {
            'x-api-key': API_KEY,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_input: action,
            actor: actor,
            atributo_base: attr,
            modificadores: [mod]
          })
        });

        if (resp.ok) {
          const data = await resp.json();
          const target = attr + mod;
          const roll = data.roll || Math.floor(Math.random() * 100) + 1;
          const isSuccess = roll <= target;
          const degrees = Math.abs(Math.floor((target - roll) / 10));

          resBox.className = `roll-result-box ${isSuccess ? 'roll-success' : 'roll-failure'}`;
          resBox.innerHTML = `
            <div style="font-size:1.1rem; font-weight:800; color:${isSuccess ? 'var(--green-auspex)' : 'var(--crimson-light)'}; margin-bottom:0.5rem;">
              ${isSuccess ? '✅ ÉXITO DETERMINISTA' : '❌ FALLO DETERMINISTA'} (${degrees} Grados de ${isSuccess ? 'Éxito' : 'Fallo'})
            </div>
            <div><strong>Acción:</strong> ${action}</div>
            <div><strong>Cálculo:</strong> Atributo Base (${attr}) + Modificador (${mod >= 0 ? '+' + mod : mod}) = <strong>Objetivo: ${target}</strong></div>
            <div><strong>Tirada d100:</strong> <span style="font-size:1.2rem; font-weight:900; color:var(--brass);">${roll}</span> vs ${target}</div>
            <div style="margin-top:0.5rem; color:var(--text-muted); font-style:italic;">"${data.narrativa || 'Resolución ejecutada y registrada por el motor de reglas.'}"</div>
          `;
        } else {
          resBox.innerHTML = `<span style="color:var(--crimson-light);">[ERROR ${resp.status}] Fallo al consultar el motor de mecánicas.</span>`;
        }
      } catch (err) {
        resBox.innerHTML = `<span style="color:var(--crimson-light);">[ERROR] ${err.message}</span>`;
      }
    }

    function filterInventory() {
      const q = document.getElementById('inv-search').value.toLowerCase();
      document.querySelectorAll('.inv-item-card').forEach(card => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(q) ? 'block' : 'none';
      });
    }

    window.addEventListener('DOMContentLoaded', () => {
      loadBlueprint();
      loadDocument('FICHA_DEL_PERSONAJE');
    });
  </script>
</body>
</html>
"""
