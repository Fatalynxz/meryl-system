const fs = require('fs');
const path = require('path');

const outDir = path.join(__dirname, '..', 'diagrams_output');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

// Canvas & Box Dimensions
const canvasW = 2820;
const canvasH = 1620;
const W = 270;
const H = 126;

// Precise Node definitions aligned on clean grid with ample vertical spacing
const nodes = {
  // ROW 1 (Left to Right, Y baseline = 250)
  "Start": { id: "Start", type: "terminal", label: "Start", x: 160, y: 250, w: 140, h: 66 },
  "A": { id: "A", wbs: "1.1", name: "Requirements Elicitation\n& Stakeholder Interviews", dur: 14, es: 0, ef: 14, ls: 0, lf: 14, slack: 0, crit: true, x: 490, y: 250 },
  "B": { id: "B", wbs: "1.2", name: "Process Observation &\nInventory Workflow Audit", dur: 16, es: 5, ef: 21, ls: 5, lf: 21, slack: 0, crit: true, x: 820, y: 250 },
  "C": { id: "C", wbs: "2.1", name: "UI/UX Wireframing, DFDs\n(0-2) & ERD Modeling", dur: 16, es: 15, ef: 31, ls: 15, lf: 31, slack: 0, crit: true, x: 1150, y: 250 },
  "D": { id: "D", wbs: "2.2", name: "System Architecture &\nSecurity Design (JWT/Crypt)", dur: 16, es: 21, ef: 37, ls: 21, lf: 37, slack: 0, crit: true, x: 1480, y: 250 },
  "E": { id: "E", wbs: "2.3", name: "Analytics Modeling &\nPromotions Design", dur: 18, es: 27, ef: 45, ls: 29, lf: 47, slack: 2, crit: false, x: 1820, y: 150 },
  "F": { id: "F", wbs: "3.1", name: "Master Catalog & Item\nParameters Design", dur: 14, es: 38, ef: 52, ls: 38, lf: 52, slack: 0, crit: true, x: 1820, y: 355 },
  "G": { id: "G", wbs: "3.2", name: "POS Terminal, Multi-Tender\n& Receipt Design", dur: 14, es: 41, ef: 55, ls: 41, lf: 55, slack: 0, crit: true, x: 2170, y: 355 },
  "H": { id: "H", wbs: "3.3", name: "Replacement Intake &\nHardware Camera QR Design", dur: 16, es: 44, ef: 60, ls: 44, lf: 60, slack: 0, crit: true, x: 2520, y: 355 },

  // ROW 2 (Right to Left, Y baseline = 670)
  "I": { id: "I", wbs: "4.1", name: "Database Setup, RLS &\nCloud Storage Buckets", dur: 15, es: 54, ef: 69, ls: 54, lf: 69, slack: 0, crit: true, x: 2520, y: 670 },
  "J": { id: "J", wbs: "4.2", name: "Front-End UI Development\n(React, TS, Tailwind)", dur: 24, es: 60, ef: 84, ls: 62, lf: 86, slack: 2, crit: false, x: 2170, y: 555 },
  "K": { id: "K", wbs: "4.3", name: "Back-End API Services &\nSession Cryptography", dur: 24, es: 64, ef: 88, ls: 64, lf: 88, slack: 0, crit: true, x: 2170, y: 785 },
  "L": { id: "L", wbs: "4.4", name: "Core POS Checkout &\nThermal Receipt Engine", dur: 22, es: 71, ef: 93, ls: 71, lf: 93, slack: 0, crit: true, x: 1820, y: 670 },
  "M": { id: "M", wbs: "4.5", name: "Predictive Sales Forecast\n& Brevo Marketing Blast", dur: 22, es: 76, ef: 98, ls: 76, lf: 98, slack: 0, crit: true, x: 1480, y: 555 },
  "N": { id: "N", wbs: "4.6", name: "Replacement Intake &\nHardware Camera Scanner", dur: 20, es: 78, ef: 98, ls: 78, lf: 98, slack: 0, crit: true, x: 1480, y: 785 },
  "O": { id: "O", wbs: "5.1", name: "Module Unit Testing &\nWhite-Box Test Cases", dur: 22, es: 84, ef: 106, ls: 86, lf: 108, slack: 2, crit: false, x: 1150, y: 670 },

  // ROW 3 (Left to Right, Y baseline = 1090)
  "P": { id: "P", wbs: "5.2", name: "Subsystem & Cross-Tab\nIntegration Testing", dur: 21, es: 95, ef: 116, ls: 95, lf: 116, slack: 0, crit: true, x: 820, y: 1090 },
  "Q": { id: "Q", wbs: "5.3", name: "Functional Black-Box\nAlpha Testing (POS/Inv)", dur: 22, es: 105, ef: 127, ls: 105, lf: 127, slack: 0, crit: true, x: 1150, y: 975 },
  "R": { id: "R", wbs: "5.4", name: "Security, Pen-Testing &\nRLS Lockout Validation", dur: 21, es: 112, ef: 133, ls: 113, lf: 134, slack: 1, crit: false, x: 1150, y: 1205 },
  "S": { id: "S", wbs: "5.5", name: "Full System Stress &\nHardware Concurrency", dur: 20, es: 119, ef: 139, ls: 119, lf: 139, slack: 0, crit: true, x: 1480, y: 1090 },
  "T": { id: "T", wbs: "5.6", name: "Bug Resolution, Retesting\n& System Hardening", dur: 19, es: 128, ef: 147, ls: 128, lf: 147, slack: 0, crit: true, x: 1820, y: 975 },
  "U": { id: "U", wbs: "5.7", name: "ISO/IEC 25010:2011 Product\nQuality Evaluation", dur: 14, es: 133, ef: 147, ls: 133, lf: 147, slack: 0, crit: true, x: 1820, y: 1205 },

  // ROW 4 (Right to Left, Y baseline = 1420)
  "V": { id: "V", wbs: "6.1", name: "Beta Testing & User\nAcceptance Testing (UAT)", dur: 8, es: 144, ef: 152, ls: 144, lf: 152, slack: 0, crit: true, x: 1820, y: 1420 },
  "W": { id: "W", wbs: "6.2", name: "Client Feedback &\nUI Final Polish", dur: 6, es: 149, ef: 155, ls: 149, lf: 155, slack: 0, crit: true, x: 1480, y: 1420 },
  "X": { id: "X", wbs: "6.3", name: "Final Documentation &\nSystem Turnover Closeout", dur: 7, es: 152, ef: 159, ls: 152, lf: 159, slack: 0, crit: true, x: 1150, y: 1420 },
  "Finish": { id: "Finish", type: "terminal", label: "Finish", x: 820, y: 1420, w: 140, h: 66 }
};

function right(k) {
  const n = nodes[k];
  const w = n.w || W;
  return [n.x + w/2, n.y];
}
function left(k) {
  const n = nodes[k];
  const w = n.w || W;
  return [n.x - w/2, n.y];
}

// ==============================================================================
// 1. GENERATE CPM SVG (RED CRITICAL PATH & ALL BLACK FONT)
// ==============================================================================
function generateCpmSvg() {
  let svg = `<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${canvasW}" height="${canvasH}" viewBox="0 0 ${canvasW} ${canvasH}">
  <defs>
    <style>
      .font-main { font-family: Arial, "Helvetica Neue", Helvetica, sans-serif; }
      .crit-line { stroke: #D32F2F; stroke-width: 3.8; fill: none; }
      .noncrit-line { stroke: #000000; stroke-width: 2.4; stroke-dasharray: 9,5; fill: none; }
    </style>
    <marker id="arrow-crit" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#D32F2F" />
    </marker>
    <marker id="arrow-noncrit" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#000000" />
    </marker>
  </defs>

  <!-- Clean Canvas -->
  <rect width="${canvasW}" height="${canvasH}" fill="#FFFFFF" />

  <!-- Header -->
  <text x="70" y="70" class="font-main" font-size="52" font-weight="900" fill="#000000">CPM</text>
  <text x="215" y="56" class="font-main" font-size="24" font-weight="900" fill="#000000">CRITICAL PATH METHOD (CPM) NETWORK DIAGRAM</text>
  <text x="215" y="84" class="font-main" font-size="16" font-weight="700" fill="#000000">Early Start (ES), Late Start (LS), Duration (D), Early Finish (EF), Late Finish (LF), and Total Slack [Float] Analysis | Total: 159 Calendar Days</text>

  <!-- Connectors -->
`;

  function drawArrow(p1, p2, isCrit, directH = false) {
    const cls = isCrit ? 'crit-line' : 'noncrit-line';
    const marker = isCrit ? 'url(#arrow-crit)' : 'url(#arrow-noncrit)';
    if (Math.abs(p1[1] - p2[1]) < 2 || directH) {
      svg += `  <line x1="${p1[0]}" y1="${p1[1]}" x2="${p2[0]}" y2="${p2[1]}" class="${cls}" marker-end="${marker}" />\n`;
    } else {
      const midX = (p1[0] + p2[0]) / 2;
      svg += `  <path d="M ${p1[0]} ${p1[1]} L ${midX} ${p1[1]} L ${midX} ${p2[1]} L ${p2[0]} ${p2[1]}" class="${cls}" marker-end="${marker}" />\n`;
    }
  }

  // Row 1 Connections
  drawArrow(right("Start"), left("A"), true, true);
  drawArrow(right("A"), left("B"), true, true);
  drawArrow(right("B"), left("C"), true, true);
  drawArrow(right("C"), left("D"), true, true);
  drawArrow(right("D"), left("E"), false);
  drawArrow(right("D"), left("F"), true);
  drawArrow(right("F"), left("G"), true, true);
  drawArrow(right("G"), left("H"), true, true);

  // Turn Row 1 -> Row 2 (H & E to I)
  const hR = right("H");
  const eR = right("E");
  const iR = right("I");
  const turnX1 = hR[0] + 55;
  svg += `  <path d="M ${hR[0]} ${hR[1]} L ${turnX1} ${hR[1]} L ${turnX1} ${iR[1]} L ${iR[0]} ${iR[1]}" class="crit-line" marker-end="url(#arrow-crit)" />\n`;
  svg += `  <path d="M ${eR[0]} ${eR[1]} L ${turnX1} ${eR[1]} L ${turnX1} ${hR[1]}" class="noncrit-line" />\n`;

  // Row 2 Connections (Right to Left)
  drawArrow(left("I"), right("J"), false);
  drawArrow(left("I"), right("K"), true);
  drawArrow(left("J"), right("L"), false);
  drawArrow(left("K"), right("L"), true);
  drawArrow(left("L"), right("M"), true);
  drawArrow(left("L"), right("N"), true);

  // J and K to O (Dedicated overhead lane at y = 430, entering top-right of O)
  const jL = left("J");
  const kL = left("K");
  const oTopX = nodes["O"].x + 85;
  const oTopY = nodes["O"].y - H/2;
  svg += `  <path d="M ${jL[0]} ${jL[1]} L ${jL[0] - 25} ${jL[1]} L ${jL[0] - 25} 430 L ${oTopX} 430 L ${oTopX} ${oTopY}" class="noncrit-line" marker-end="url(#arrow-noncrit)" />\n`;
  svg += `  <path d="M ${kL[0]} ${kL[1]} L ${jL[0] - 25} ${kL[1]} L ${jL[0] - 25} ${jL[1]}" class="noncrit-line" />\n`;

  // Turn Row 2 -> Row 3 (Critical path from M and N down to P; O joins non-critically)
  const mL = left("M");
  const nL = left("N");
  const oL = left("O");
  const pL = left("P");
  const turnX2 = pL[0] - 55;
  // Critical Path trunk from M down to P
  svg += `  <path d="M ${mL[0]} ${mL[1]} L ${mL[0] - 30} ${mL[1]} L ${mL[0] - 30} 505 L ${turnX2} 505 L ${turnX2} ${pL[1]} L ${pL[0]} ${pL[1]}" class="crit-line" marker-end="url(#arrow-crit)" />\n`;
  // Critical Path merge from N into the trunk
  svg += `  <path d="M ${nL[0]} ${nL[1]} L ${nL[0] - 30} ${nL[1]} L ${nL[0] - 30} 835 L ${turnX2} 835" class="crit-line" />\n`;
  // Non-Critical merge from O into the trunk
  svg += `  <path d="M ${oL[0]} ${oL[1]} L ${turnX2} ${oL[1]}" class="noncrit-line" />\n`;

  // Row 3 Connections (Left to Right)
  drawArrow(right("P"), left("Q"), true);
  drawArrow(right("P"), left("R"), false);
  drawArrow(right("Q"), left("S"), true);
  drawArrow(right("R"), left("S"), false);
  drawArrow(right("S"), left("T"), true);
  drawArrow(right("S"), left("U"), true);

  // Turn Row 3 -> Row 4 (T & U to V)
  const tR = right("T");
  const uR = right("U");
  const vR = right("V");
  const turnX3 = tR[0] + 65;
  svg += `  <path d="M ${tR[0]} ${tR[1]} L ${turnX3} ${tR[1]} L ${turnX3} ${vR[1]} L ${vR[0]} ${vR[1]}" class="crit-line" marker-end="url(#arrow-crit)" />\n`;
  svg += `  <path d="M ${uR[0]} ${uR[1]} L ${turnX3} ${uR[1]}" class="crit-line" />\n`;

  // Row 4 Connections (Right to Left)
  drawArrow(left("V"), right("W"), true, true);
  drawArrow(left("W"), right("X"), true, true);
  drawArrow(left("X"), right("Finish"), true, true);

  // Render Nodes
  for (const [key, n] of Object.entries(nodes)) {
    if (n.type === "terminal") {
      const x0 = n.x - n.w/2;
      const y0 = n.y - n.h/2;
      svg += `
  <!-- Terminal: ${n.label} -->
  <g>
    <rect x="${x0}" y="${y0}" width="${n.w}" height="${n.h}" rx="10" ry="10" fill="#FFFFFF" stroke="#000000" stroke-width="2.8" />
    <text x="${n.x}" y="${n.y + 9}" class="font-main" font-size="26" font-weight="900" fill="#000000" text-anchor="middle">${n.label}</text>
  </g>`;
    } else {
      const x0 = n.x - W/2;
      const y0 = n.y - H/2;

      const sw = 86;
      const sh = 38;
      const sx0 = n.x - sw/2;
      const sy0 = y0 - sh - 8;

      const colW1 = 82;
      const colW2 = 106;
      const colW3 = 82;
      const midY = y0 + H/2;
      const lineX1 = x0 + colW1;
      const lineX2 = x0 + colW1 + colW2;

      svg += `
  <!-- Activity Node ${n.id} -->
  <g>
    <!-- Floating Slack Box (High-Contrast Black Border & Text) -->
    <rect x="${sx0}" y="${sy0}" width="${sw}" height="${sh}" rx="6" ry="6" fill="#FFFFFF" stroke="#000000" stroke-width="2.2" />
    <text x="${n.x}" y="${sy0 + 28}" class="font-main" font-size="28" font-weight="900" fill="#000000" text-anchor="middle">${n.slack}</text>

    <!-- Main Container -->
    <rect x="${x0}" y="${y0}" width="${W}" height="${H}" rx="8" ry="8" fill="#FFFFFF" stroke="#000000" stroke-width="2.8" />
    
    <!-- Dividing Lines -->
    <line x1="${x0}" y1="${midY}" x2="${x0 + W}" y2="${midY}" stroke="#000000" stroke-width="2.0" />
    <line x1="${lineX1}" y1="${y0}" x2="${lineX1}" y2="${y0 + H}" stroke="#000000" stroke-width="2.0" />
    <line x1="${lineX2}" y1="${y0}" x2="${lineX2}" y2="${y0 + H}" stroke="#000000" stroke-width="2.0" />

    <!-- Top Row: ES | Activity ID | EF (ALL BOLD BLACK) -->
    <text x="${x0 + colW1/2}" y="${y0 + 40}" class="font-main" font-size="20" font-weight="900" fill="#000000" text-anchor="middle">ES: ${n.es}</text>
    <text x="${x0 + colW1 + colW2/2}" y="${y0 + 42}" class="font-main" font-size="25" font-weight="900" fill="#000000" text-anchor="middle">A: ${n.id}</text>
    <text x="${lineX2 + colW3/2}" y="${y0 + 40}" class="font-main" font-size="20" font-weight="900" fill="#000000" text-anchor="middle">EF: ${n.ef}</text>

    <!-- Bottom Row: LS | Duration | LF (ALL BOLD BLACK) -->
    <text x="${x0 + colW1/2}" y="${y0 + H - 20}" class="font-main" font-size="20" font-weight="900" fill="#000000" text-anchor="middle">LS: ${n.ls}</text>
    <text x="${x0 + colW1 + colW2/2}" y="${y0 + H - 20}" class="font-main" font-size="23" font-weight="900" fill="#000000" text-anchor="middle">D: ${n.dur}</text>
    <text x="${lineX2 + colW3/2}" y="${y0 + H - 20}" class="font-main" font-size="20" font-weight="900" fill="#000000" text-anchor="middle">LF: ${n.lf}</text>
  </g>`;
    }
  }

  // Legend at bottom (Highlighted Red Critical Path Legend with ample width)
  svg += `
  <!-- Legend -->
  <g transform="translate(80, 1530)">
    <rect x="0" y="-18" width="1120" height="54" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="2.4" />
    <text x="22" y="16" class="font-main" font-size="18" font-weight="900" fill="#000000">CPM LEGEND:</text>
    
    <!-- Red Critical Path -->
    <line x1="175" y1="10" x2="255" y2="10" stroke="#D32F2F" stroke-width="4.2" />
    <polygon points="251,6.5 261,10 251,13.5" fill="#D32F2F" />
    <text x="275" y="16" class="font-main" font-size="16.5" font-weight="900" fill="#D32F2F">Critical Path (Zero Float / Slack = 0)</text>
    
    <!-- Black Non-Critical Path -->
    <line x1="720" y1="10" x2="795" y2="10" stroke="#000000" stroke-width="2.4" stroke-dasharray="9,5" />
    <polygon points="791,6.5 801,10 791,13.5" fill="#000000" />
    <text x="815" y="16" class="font-main" font-size="16.5" font-weight="800" fill="#000000">Non-Critical Activity (Slack &gt; 0)</text>
  </g>
</svg>`;

  return svg;
}

// ==============================================================================
// 2. GENERATE PERT SVG (RED CRITICAL PATH & ALL BLACK FONT)
// ==============================================================================
function generatePertSvg() {
  let svg = `<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${canvasW}" height="${canvasH}" viewBox="0 0 ${canvasW} ${canvasH}">
  <defs>
    <style>
      .font-main { font-family: Arial, "Helvetica Neue", Helvetica, sans-serif; }
      .crit-line { stroke: #D32F2F; stroke-width: 3.8; fill: none; }
      .noncrit-line { stroke: #000000; stroke-width: 2.4; stroke-dasharray: 9,5; fill: none; }
    </style>
    <marker id="arrow-crit" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#D32F2F" />
    </marker>
    <marker id="arrow-noncrit" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#000000" />
    </marker>
  </defs>

  <!-- Clean Canvas -->
  <rect width="${canvasW}" height="${canvasH}" fill="#FFFFFF" />

  <!-- Header (All Black) -->
  <text x="70" y="48" class="font-main" font-size="24" font-weight="900" fill="#000000">CARLOS HILADO MEMORIAL STATE UNIVERSITY — COLLEGE OF COMPUTER STUDIES</text>
  <text x="70" y="76" class="font-main" font-size="20" font-weight="800" fill="#000000">PROGRAM EVALUATION AND REVIEW TECHNIQUE (PERT) NETWORK DIAGRAM</text>
  <text x="70" y="102" class="font-main" font-size="16" font-style="italic" font-weight="600" fill="#000000">Integrated POS-Driven Inventory System with Data Analytics | Total Critical Duration: 159 Calendar Days (May 5 – Oct 10, 2026)</text>

  <!-- Connectors -->
`;

  function drawArrow(p1, p2, isCrit, directH = false) {
    const cls = isCrit ? 'crit-line' : 'noncrit-line';
    const marker = isCrit ? 'url(#arrow-crit)' : 'url(#arrow-noncrit)';
    if (Math.abs(p1[1] - p2[1]) < 2 || directH) {
      svg += `  <line x1="${p1[0]}" y1="${p1[1]}" x2="${p2[0]}" y2="${p2[1]}" class="${cls}" marker-end="${marker}" />\n`;
    } else {
      const midX = (p1[0] + p2[0]) / 2;
      svg += `  <path d="M ${p1[0]} ${p1[1]} L ${midX} ${p1[1]} L ${midX} ${p2[1]} L ${p2[0]} ${p2[1]}" class="${cls}" marker-end="${marker}" />\n`;
    }
  }

  // Row 1 Connections
  drawArrow(right("Start"), left("A"), true, true);
  drawArrow(right("A"), left("B"), true, true);
  drawArrow(right("B"), left("C"), true, true);
  drawArrow(right("C"), left("D"), true, true);
  drawArrow(right("D"), left("E"), false);
  drawArrow(right("D"), left("F"), true);
  drawArrow(right("F"), left("G"), true, true);
  drawArrow(right("G"), left("H"), true, true);

  // Turn Row 1 -> Row 2 (H & E to I)
  const hR = right("H");
  const eR = right("E");
  const iR = right("I");
  const turnX1 = hR[0] + 55;
  svg += `  <path d="M ${hR[0]} ${hR[1]} L ${turnX1} ${hR[1]} L ${turnX1} ${iR[1]} L ${iR[0]} ${iR[1]}" class="crit-line" marker-end="url(#arrow-crit)" />\n`;
  svg += `  <path d="M ${eR[0]} ${eR[1]} L ${turnX1} ${eR[1]} L ${turnX1} ${hR[1]}" class="noncrit-line" />\n`;

  // Row 2 Connections
  drawArrow(left("I"), right("J"), false);
  drawArrow(left("I"), right("K"), true);
  drawArrow(left("J"), right("L"), false);
  drawArrow(left("K"), right("L"), true);
  drawArrow(left("L"), right("M"), true);
  drawArrow(left("L"), right("N"), true);

  // J and K to O (Dedicated overhead lane at y = 430, entering top-right of O)
  const jL = left("J");
  const kL = left("K");
  const oTopX = nodes["O"].x + 85;
  const oTopY = nodes["O"].y - H/2;
  svg += `  <path d="M ${jL[0]} ${jL[1]} L ${jL[0] - 25} ${jL[1]} L ${jL[0] - 25} 430 L ${oTopX} 430 L ${oTopX} ${oTopY}" class="noncrit-line" marker-end="url(#arrow-noncrit)" />\n`;
  svg += `  <path d="M ${kL[0]} ${kL[1]} L ${jL[0] - 25} ${kL[1]} L ${jL[0] - 25} ${jL[1]}" class="noncrit-line" />\n`;

  // Turn Row 2 -> Row 3
  const mL = left("M");
  const nL = left("N");
  const oL = left("O");
  const pL = left("P");
  const turnX2 = pL[0] - 55;
  // Critical Path trunk from M down to P
  svg += `  <path d="M ${mL[0]} ${mL[1]} L ${mL[0] - 30} ${mL[1]} L ${mL[0] - 30} 505 L ${turnX2} 505 L ${turnX2} ${pL[1]} L ${pL[0]} ${pL[1]}" class="crit-line" marker-end="url(#arrow-crit)" />\n`;
  // Critical Path merge from N into the trunk
  svg += `  <path d="M ${nL[0]} ${nL[1]} L ${nL[0] - 30} ${nL[1]} L ${nL[0] - 30} 835 L ${turnX2} 835" class="crit-line" />\n`;
  // Non-Critical merge from O into the trunk
  svg += `  <path d="M ${oL[0]} ${oL[1]} L ${turnX2} ${oL[1]}" class="noncrit-line" />\n`;

  // Row 3 Connections
  drawArrow(right("P"), left("Q"), true);
  drawArrow(right("P"), left("R"), false);
  drawArrow(right("Q"), left("S"), true);
  drawArrow(right("R"), left("S"), false);
  drawArrow(right("S"), left("T"), true);
  drawArrow(right("S"), left("U"), true);

  // Turn Row 3 -> Row 4
  const tR = right("T");
  const uR = right("U");
  const vR = right("V");
  const turnX3 = tR[0] + 65;
  svg += `  <path d="M ${tR[0]} ${tR[1]} L ${turnX3} ${tR[1]} L ${turnX3} ${vR[1]} L ${vR[0]} ${vR[1]}" class="crit-line" marker-end="url(#arrow-crit)" />\n`;
  svg += `  <path d="M ${uR[0]} ${uR[1]} L ${turnX3} ${uR[1]}" class="crit-line" />\n`;

  // Row 4 Connections
  drawArrow(left("V"), right("W"), true, true);
  drawArrow(left("W"), right("X"), true, true);
  drawArrow(left("X"), right("Finish"), true, true);

  // Render Nodes
  for (const [key, n] of Object.entries(nodes)) {
    if (n.type === "terminal") {
      const x0 = n.x - n.w/2;
      const y0 = n.y - n.h/2;
      svg += `
  <!-- Terminal: ${n.label} -->
  <g>
    <rect x="${x0}" y="${y0}" width="${n.w}" height="${n.h}" rx="10" ry="10" fill="#FFFFFF" stroke="#000000" stroke-width="2.8" />
    <text x="${n.x}" y="${n.y + 9}" class="font-main" font-size="26" font-weight="900" fill="#000000" text-anchor="middle">${n.label}</text>
  </g>`;
    } else {
      const x0 = n.x - W/2;
      const y0 = n.y - H/2;

      const hTop = 60;
      const hBot = H - hTop;
      const dividerY = y0 + hTop;
      const midX = x0 + W/2;

      const lines = n.name.split('\n');
      let titleSvg = '';
      if (lines.length === 1) {
        titleSvg = `<text x="${n.x}" y="${y0 + 36}" class="font-main" font-size="18" font-weight="900" fill="#000000" text-anchor="middle">${lines[0]}</text>`;
      } else {
        titleSvg = `<text x="${n.x}" y="${y0 + 26}" class="font-main" font-size="16.5" font-weight="900" fill="#000000" text-anchor="middle">${lines[0]}</text>
        <text x="${n.x}" y="${y0 + 49}" class="font-main" font-size="16.5" font-weight="900" fill="#000000" text-anchor="middle">${lines[1]}</text>`;
      }

      svg += `
  <!-- PERT Node ${n.id} -->
  <g>
    <rect x="${x0}" y="${y0}" width="${W}" height="${H}" rx="8" ry="8" fill="#FFFFFF" stroke="#000000" stroke-width="2.8" />
    
    <!-- Grid Dividers -->
    <line x1="${x0}" y1="${dividerY}" x2="${x0 + W}" y2="${dividerY}" stroke="#000000" stroke-width="2.0" />
    <line x1="${midX}" y1="${dividerY}" x2="${midX}" y2="${y0 + H}" stroke="#000000" stroke-width="2.0" />
    <line x1="${x0}" y1="${dividerY + hBot/2}" x2="${x0 + W}" y2="${dividerY + hBot/2}" stroke="#000000" stroke-width="1.6" />

    <!-- Task Name (Bold Black) -->
    ${titleSvg}

    <!-- Bottom Left: Start & Finish (Bold Black) -->
    <text x="${x0 + 14}" y="${dividerY + 23}" class="font-main" font-size="17" font-weight="900" fill="#000000">Start: ${n.es}</text>
    <text x="${x0 + 14}" y="${dividerY + hBot - 10}" class="font-main" font-size="17" font-weight="900" fill="#000000">Finish: ${n.ef}</text>

    <!-- Bottom Right: ID & Duration (Bold Black) -->
    <text x="${midX + 14}" y="${dividerY + 23}" class="font-main" font-size="18" font-weight="900" fill="#000000">ID: ${n.id} (${n.wbs})</text>
    <text x="${midX + 14}" y="${dividerY + hBot - 10}" class="font-main" font-size="17" font-weight="900" fill="#000000">Duration: ${n.dur}</text>
  </g>`;
    }
  }

  // Legend at bottom (Highlighted Red Critical Path Legend with ample width)
  svg += `
  <!-- Legend -->
  <g transform="translate(80, 1530)">
    <rect x="0" y="-18" width="1220" height="54" rx="8" fill="#FFFFFF" stroke="#000000" stroke-width="2.4" />
    <text x="22" y="16" class="font-main" font-size="18" font-weight="900" fill="#000000">PERT LEGEND:</text>
    
    <!-- Red Critical Path -->
    <line x1="175" y1="10" x2="255" y2="10" stroke="#D32F2F" stroke-width="4.2" />
    <polygon points="251,6.5 261,10 251,13.5" fill="#D32F2F" />
    <text x="275" y="16" class="font-main" font-size="16.5" font-weight="900" fill="#D32F2F">Critical Path (Zero Slack / Direct Impact on Closeout)</text>
    
    <!-- Black Non-Critical Path -->
    <line x1="800" y1="10" x2="875" y2="10" stroke="#000000" stroke-width="2.4" stroke-dasharray="9,5" />
    <polygon points="871,6.5 881,10 871,13.5" fill="#000000" />
    <text x="895" y="16" class="font-main" font-size="16.5" font-weight="800" fill="#000000">Non-Critical Activity (Flexible Float)</text>
  </g>
</svg>`;

  return svg;
}

// Generate files
const cpmSvg = generateCpmSvg();
const cpmSvgPath = path.join(outDir, 'MERYL_SHOES_CPM_NETWORK_DIAGRAM.svg');
fs.writeFileSync(cpmSvgPath, cpmSvg, 'utf8');

const pertSvg = generatePertSvg();
const pertSvgPath = path.join(outDir, 'MERYL_SHOES_PERT_CHART.svg');
fs.writeFileSync(pertSvgPath, pertSvg, 'utf8');

// Inline HTML for 100% synchronous rendering in Edge headless
const cpmHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body { margin: 0; padding: 0; background: #ffffff; width: ${canvasW}px; height: ${canvasH}px; overflow: hidden; }
</style>
</head>
<body>
${cpmSvg}
</body>
</html>`;
fs.writeFileSync(path.join(outDir, 'view_cpm_inline.html'), cpmHtml, 'utf8');

const pertHtml = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body { margin: 0; padding: 0; background: #ffffff; width: ${canvasW}px; height: ${canvasH}px; overflow: hidden; }
</style>
</head>
<body>
${pertSvg}
</body>
</html>`;
fs.writeFileSync(path.join(outDir, 'view_pert_inline.html'), pertHtml, 'utf8');

console.log('Successfully generated red critical path SVGs and HTML viewers!');
