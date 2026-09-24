import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("diagrams_output", exist_ok=True)

# Node definitions with coordinates
# W = 1.9, H = 0.85
nodes = {
    # ROW 1 (Left to Right)
    "Start": {"label": "Start", "type": "terminal", "x": 0.5, "y": 11.5, "w": 1.0, "h": 0.5},
    "A": {
        "id": "A", "wbs": "1.1", "name": "Requirements Elicitation\n& Stakeholder Interviews",
        "dur": 14, "es": 0, "ef": 14, "ls": 0, "lf": 14, "slack": 0, "crit": True,
        "x": 2.2, "y": 11.5, "w": 2.0, "h": 0.85
    },
    "B": {
        "id": "B", "wbs": "1.2", "name": "Process Observation &\nInventory Workflow Audit",
        "dur": 16, "es": 5, "ef": 21, "ls": 5, "lf": 21, "slack": 0, "crit": True,
        "x": 4.9, "y": 11.5, "w": 2.0, "h": 0.85
    },
    "C": {
        "id": "C", "wbs": "2.1", "name": "UI/UX Wireframing, DFDs\n(0-2) & ERD Modeling",
        "dur": 16, "es": 15, "ef": 31, "ls": 15, "lf": 31, "slack": 0, "crit": True,
        "x": 7.6, "y": 11.5, "w": 2.0, "h": 0.85
    },
    "D": {
        "id": "D", "wbs": "2.2", "name": "System Architecture &\nSecurity Design (JWT/Crypt)",
        "dur": 16, "es": 21, "ef": 37, "ls": 21, "lf": 37, "slack": 0, "crit": True,
        "x": 10.3, "y": 11.5, "w": 2.0, "h": 0.85
    },
    "E": {
        "id": "E", "wbs": "2.3", "name": "Predictive Analytics &\nPromotions Design",
        "dur": 18, "es": 27, "ef": 45, "ls": 29, "lf": 47, "slack": 2, "crit": False,
        "x": 13.0, "y": 12.3, "w": 2.0, "h": 0.85
    },
    "F": {
        "id": "F", "wbs": "3.1", "name": "Master Catalog & Item\nParameters Design",
        "dur": 14, "es": 38, "ef": 52, "ls": 38, "lf": 52, "slack": 0, "crit": True,
        "x": 13.0, "y": 10.7, "w": 2.0, "h": 0.85
    },
    "G": {
        "id": "G", "wbs": "3.2", "name": "POS Terminal, Multi-Tender\n& Receipt Design",
        "dur": 14, "es": 41, "ef": 55, "ls": 41, "lf": 55, "slack": 0, "crit": True,
        "x": 15.7, "y": 10.7, "w": 2.0, "h": 0.85
    },
    "H": {
        "id": "H", "wbs": "3.3", "name": "Replacement Intake &\nHardware Camera QR Design",
        "dur": 16, "es": 44, "ef": 60, "ls": 44, "lf": 60, "slack": 0, "crit": True,
        "x": 18.4, "y": 10.7, "w": 2.0, "h": 0.85
    },

    # ROW 2 (Right to Left)
    "I": {
        "id": "I", "wbs": "4.1", "name": "Database Setup, RLS &\nCloud Storage Buckets",
        "dur": 15, "es": 54, "ef": 69, "ls": 54, "lf": 69, "slack": 0, "crit": True,
        "x": 18.4, "y": 8.0, "w": 2.0, "h": 0.85
    },
    "J": {
        "id": "J", "wbs": "4.2", "name": "Front-End UI Development\n(React, TS, Tailwind)",
        "dur": 24, "es": 60, "ef": 84, "ls": 62, "lf": 86, "slack": 2, "crit": False,
        "x": 15.7, "y": 8.8, "w": 2.0, "h": 0.85
    },
    "K": {
        "id": "K", "wbs": "4.3", "name": "Back-End API Services &\nSession Cryptography",
        "dur": 24, "es": 64, "ef": 88, "ls": 64, "lf": 88, "slack": 0, "crit": True,
        "x": 15.7, "y": 7.2, "w": 2.0, "h": 0.85
    },
    "L": {
        "id": "L", "wbs": "4.4", "name": "Core POS Checkout &\nThermal Receipt Engine",
        "dur": 22, "es": 71, "ef": 93, "ls": 71, "lf": 93, "slack": 0, "crit": True,
        "x": 13.0, "y": 8.0, "w": 2.0, "h": 0.85
    },
    "M": {
        "id": "M", "wbs": "4.5", "name": "Predictive Sales Forecast\n& Brevo Marketing Blast",
        "dur": 22, "es": 76, "ef": 98, "ls": 76, "lf": 98, "slack": 0, "crit": True,
        "x": 10.3, "y": 8.8, "w": 2.0, "h": 0.85
    },
    "N": {
        "id": "N", "wbs": "4.6", "name": "Replacement Intake &\nHardware Camera Scanner",
        "dur": 20, "es": 78, "ef": 98, "ls": 78, "lf": 98, "slack": 0, "crit": True,
        "x": 10.3, "y": 7.2, "w": 2.0, "h": 0.85
    },
    "O": {
        "id": "O", "wbs": "5.1", "name": "Module Unit Testing &\nWhite-Box Test Cases",
        "dur": 22, "es": 84, "ef": 106, "ls": 86, "lf": 108, "slack": 2, "crit": False,
        "x": 7.6, "y": 8.0, "w": 2.0, "h": 0.85
    },

    # ROW 3 (Left to Right)
    "P": {
        "id": "P", "wbs": "5.2", "name": "Subsystem & Cross-Tab\nIntegration Testing",
        "dur": 21, "es": 95, "ef": 116, "ls": 95, "lf": 116, "slack": 0, "crit": True,
        "x": 4.9, "y": 4.5, "w": 2.0, "h": 0.85
    },
    "Q": {
        "id": "Q", "wbs": "5.3", "name": "Functional Black-Box\nAlpha Testing (POS/Inv)",
        "dur": 22, "es": 105, "ef": 127, "ls": 105, "lf": 127, "slack": 0, "crit": True,
        "x": 7.6, "y": 5.3, "w": 2.0, "h": 0.85
    },
    "R": {
        "id": "R", "wbs": "5.4", "name": "Security, Pen-Testing &\nRLS Lockout Validation",
        "dur": 21, "es": 112, "ef": 133, "ls": 113, "lf": 134, "slack": 1, "crit": False,
        "x": 7.6, "y": 3.7, "w": 2.0, "h": 0.85
    },
    "S": {
        "id": "S", "wbs": "5.5", "name": "Full System Stress &\nHardware Concurrency",
        "dur": 20, "es": 119, "ef": 139, "ls": 119, "lf": 139, "slack": 0, "crit": True,
        "x": 10.3, "y": 4.5, "w": 2.0, "h": 0.85
    },
    "T": {
        "id": "T", "wbs": "5.6", "name": "Bug Resolution, Retesting\n& System Hardening",
        "dur": 19, "es": 128, "ef": 147, "ls": 128, "lf": 147, "slack": 0, "crit": True,
        "x": 13.0, "y": 5.3, "w": 2.0, "h": 0.85
    },
    "U": {
        "id": "U", "wbs": "5.7", "name": "ISO/IEC 25010:2011 Product\nQuality Evaluation",
        "dur": 14, "es": 133, "ef": 147, "ls": 133, "lf": 147, "slack": 0, "crit": True,
        "x": 13.0, "y": 3.7, "w": 2.0, "h": 0.85
    },

    # ROW 4 (Right to Left)
    "V": {
        "id": "V", "wbs": "6.1", "name": "Beta Testing & User\nAcceptance Testing (UAT)",
        "dur": 8, "es": 144, "ef": 152, "ls": 144, "lf": 152, "slack": 0, "crit": True,
        "x": 13.0, "y": 1.2, "w": 2.0, "h": 0.85
    },
    "W": {
        "id": "W", "wbs": "6.2", "name": "Client Feedback &\nUI Final Polish",
        "dur": 6, "es": 149, "ef": 155, "ls": 149, "lf": 155, "slack": 0, "crit": True,
        "x": 10.3, "y": 1.2, "w": 2.0, "h": 0.85
    },
    "X": {
        "id": "X", "wbs": "6.3", "name": "Final Documentation &\nSystem Turnover Closeout",
        "dur": 7, "es": 152, "ef": 159, "ls": 152, "lf": 159, "slack": 0, "crit": True,
        "x": 7.6, "y": 1.2, "w": 2.0, "h": 0.85
    },
    "Finish": {"label": "Finish", "type": "terminal", "x": 4.9, "y": 1.2, "w": 1.0, "h": 0.5}
}

# ==============================================================================
# DRAW PERT NETWORK DIAGRAM (Image 1 style)
# ==============================================================================
def draw_pert_diagram():
    fig, ax = plt.subplots(figsize=(23, 14), dpi=300)
    ax.set_xlim(0, 21.0)
    ax.set_ylim(0, 13.5)
    ax.axis("off")

    # Header / Title
    ax.text(10.5, 13.0, "CARLOS HILADO MEMORIAL STATE UNIVERSITY — COLLEGE OF COMPUTER STUDIES", 
            ha="center", va="center", fontsize=14, fontweight="bold", color="#1B5E20")
    ax.text(10.5, 12.65, "PROGRAM EVALUATION AND REVIEW TECHNIQUE (PERT) NETWORK DIAGRAM", 
            ha="center", va="center", fontsize=12, fontweight="bold", color="#263238")
    ax.text(10.5, 12.35, "Meryl Shoes Enterprise System | Critical Path Duration: 159 Calendar Days (May 5 – Oct 10, 2026)", 
            ha="center", va="center", fontsize=10, fontstyle="italic", color="#546E7A")

    # Draw Nodes
    for k, n in nodes.items():
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        x0 = x - w / 2
        y0 = y - h / 2

        if n.get("type") == "terminal":
            # Terminal box (Start / Finish)
            rect = patches.Rectangle((x0, y0), w, h, linewidth=1.8, edgecolor="#1B5E20", facecolor="#E8F5E9", zorder=3)
            ax.add_patch(rect)
            ax.text(x, y, n["label"], ha="center", va="center", fontsize=11, fontweight="bold", color="#1B5E20", zorder=4)
        else:
            # Standard PERT node: Box with Title and 4 metrics
            is_crit = n["crit"]
            border_color = "#B71C1C" if is_crit else "#1565C0"
            fill_color = "#FFF5F5" if is_crit else "#F3F8FF"
            line_w = 1.6 if is_crit else 1.2
            
            rect = patches.Rectangle((x0, y0), w, h, linewidth=line_w, edgecolor=border_color, facecolor=fill_color, zorder=3)
            ax.add_patch(rect)

            h_top = 0.44
            h_bot = h - h_top
            
            # Divider lines
            ax.plot([x0, x0 + w], [y0 + h_bot, y0 + h_bot], color=border_color, lw=1.0, zorder=4) # horizontal
            ax.plot([x0 + w/2, x0 + w/2], [y0, y0 + h_bot], color=border_color, lw=1.0, zorder=4) # vertical bottom divider
            ax.plot([x0, x0 + w], [y0 + h_bot/2, y0 + h_bot/2], color=border_color, lw=0.8, zorder=4) # mid bottom horizontal

            # Top Text (Task Name)
            ax.text(x, y0 + h_bot + h_top/2, n["name"], ha="center", va="center", fontsize=7.2, fontweight="bold", color="#1A1A1A", zorder=5)

            # Bottom Left: Start & Finish
            ax.text(x0 + 0.1, y0 + h_bot * 0.75, f"Start: {n['es']}", ha="left", va="center", fontsize=7.0, color="#333333", zorder=5)
            ax.text(x0 + 0.1, y0 + h_bot * 0.25, f"Finish: {n['ef']}", ha="left", va="center", fontsize=7.0, color="#333333", zorder=5)

            # Bottom Right: ID & Duration
            ax.text(x0 + w/2 + 0.1, y0 + h_bot * 0.75, f"ID: {n['id']} ({n['wbs']})", ha="left", va="center", fontsize=7.0, fontweight="bold", color=border_color, zorder=5)
            ax.text(x0 + w/2 + 0.1, y0 + h_bot * 0.25, f"Duration: {n['dur']}", ha="left", va="center", fontsize=7.0, color="#333333", zorder=5)

    # Function to draw orthogonal elbow arrow
    def draw_arrow(x1, y1, x2, y2, color="#263238", lw=1.4, style="->"):
        arrow_props = dict(arrowstyle=style, color=color, lw=lw, shrinkA=0, shrinkB=0, mutation_scale=12)
        if abs(y1 - y2) < 0.05:
            # Straight horizontal
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props, zorder=2)
        elif abs(x1 - x2) < 0.05:
            # Straight vertical
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props, zorder=2)
        else:
            # Orthogonal step
            x_mid = (x1 + x2) / 2
            ax.plot([x1, x_mid, x_mid, x2], [y1, y1, y2, y2], color=color, lw=lw, zorder=2)
            # small arrow pointing into x2, y2
            dx = 0.05 if x2 > x_mid else -0.05
            ax.annotate("", xy=(x2, y2), xytext=(x2 - dx, y2), arrowprops=arrow_props, zorder=2)

    # Helper to get edge attachment points
    def get_right(key): return nodes[key]["x"] + nodes[key]["w"]/2, nodes[key]["y"]
    def get_left(key): return nodes[key]["x"] - nodes[key]["w"]/2, nodes[key]["y"]
    def get_top(key): return nodes[key]["x"], nodes[key]["y"] + nodes[key]["h"]/2
    def get_bottom(key): return nodes[key]["x"], nodes[key]["y"] - nodes[key]["h"]/2

    # Draw Connections Row 1 (Left to Right)
    draw_arrow(*get_right("Start"), *get_left("A"))
    draw_arrow(*get_right("A"), *get_left("B"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("B"), *get_left("C"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("C"), *get_left("D"), color="#B71C1C", lw=1.8)

    # D -> E (Float) and D -> F (Critical)
    draw_arrow(*get_right("D"), *get_left("E"), color="#1565C0", lw=1.4)
    draw_arrow(*get_right("D"), *get_left("F"), color="#B71C1C", lw=1.8)

    # F -> G -> H (Critical)
    draw_arrow(*get_right("F"), *get_left("G"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("G"), *get_left("H"), color="#B71C1C", lw=1.8)

    # Row 1 -> Row 2 Turn (H and E -> I)
    h_r = get_right("H")
    i_r = get_right("I")
    ax.plot([h_r[0], h_r[0] + 0.4, h_r[0] + 0.4, i_r[0] + 0.4, i_r[0] + 0.4, i_r[0]], 
            [h_r[1], h_r[1], (h_r[1] + i_r[1])/2, (h_r[1] + i_r[1])/2, i_r[1], i_r[1]], color="#B71C1C", lw=1.8, zorder=2)
    ax.annotate("", xy=(i_r[0], i_r[1]), xytext=(i_r[0] + 0.05, i_r[1]), arrowprops=dict(arrowstyle="->", color="#B71C1C", lw=1.8, mutation_scale=12), zorder=2)

    e_r = get_right("E")
    ax.plot([e_r[0], h_r[0] + 0.4], [e_r[1], e_r[1]], color="#1565C0", lw=1.2, zorder=2)

    # Row 2 (Right to Left): I -> J (Float), I -> K (Critical)
    draw_arrow(*get_left("I"), *get_right("J"), color="#1565C0", lw=1.4)
    draw_arrow(*get_left("I"), *get_right("K"), color="#B71C1C", lw=1.8)

    # J & K -> L (Core POS)
    draw_arrow(*get_left("J"), *get_right("L"), color="#1565C0", lw=1.4)
    draw_arrow(*get_left("K"), *get_right("L"), color="#B71C1C", lw=1.8)

    # L -> M (Critical Forecast) & N (Critical Replacement QR)
    draw_arrow(*get_left("L"), *get_right("M"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_left("L"), *get_right("N"), color="#B71C1C", lw=1.8)

    # J & K -> O (Unit Testing)
    draw_arrow(nodes["J"]["x"] - nodes["J"]["w"]/2, nodes["J"]["y"], nodes["O"]["x"] + nodes["O"]["w"]/2, nodes["O"]["y"] + 0.2, color="#1565C0", lw=1.2)

    # Row 2 -> Row 3 Turn: M, N, O -> P
    o_l = get_left("O")
    m_l = get_left("M")
    n_l = get_left("N")
    p_l = get_left("P")

    # M & N connect to P
    ax.plot([m_l[0], o_l[0] - 0.4, o_l[0] - 0.4, p_l[0] - 0.4, p_l[0] - 0.4, p_l[0]], 
            [m_l[1], m_l[1], (m_l[1] + p_l[1])/2, (m_l[1] + p_l[1])/2, p_l[1], p_l[1]], color="#B71C1C", lw=1.8, zorder=2)
    ax.annotate("", xy=(p_l[0], p_l[1]), xytext=(p_l[0] - 0.05, p_l[1]), arrowprops=dict(arrowstyle="->", color="#B71C1C", lw=1.8, mutation_scale=12), zorder=2)
    ax.plot([n_l[0], o_l[0] - 0.4], [n_l[1], n_l[1]], color="#B71C1C", lw=1.8, zorder=2)
    ax.plot([o_l[0], o_l[0] - 0.4], [o_l[1], o_l[1]], color="#1565C0", lw=1.2, zorder=2)

    # Row 3 (Left to Right): P -> Q (Critical) & R (Float)
    draw_arrow(*get_right("P"), *get_left("Q"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("P"), *get_left("R"), color="#1565C0", lw=1.4)

    # Q & R -> S (Full System Stress)
    draw_arrow(*get_right("Q"), *get_left("S"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("R"), *get_left("S"), color="#1565C0", lw=1.4)

    # S -> T (Bug Resolution) & U (ISO 25010)
    draw_arrow(*get_right("S"), *get_left("T"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("S"), *get_left("U"), color="#B71C1C", lw=1.8)

    # Row 3 -> Row 4 Turn: T & U -> V
    t_r = get_right("T")
    u_r = get_right("U")
    v_r = get_right("V")

    ax.plot([t_r[0], t_r[0] + 0.4, t_r[0] + 0.4, v_r[0] + 0.4, v_r[0] + 0.4, v_r[0]], 
            [t_r[1], t_r[1], (t_r[1] + v_r[1])/2, (t_r[1] + v_r[1])/2, v_r[1], v_r[1]], color="#B71C1C", lw=1.8, zorder=2)
    ax.annotate("", xy=(v_r[0], v_r[1]), xytext=(v_r[0] + 0.05, v_r[1]), arrowprops=dict(arrowstyle="->", color="#B71C1C", lw=1.8, mutation_scale=12), zorder=2)
    ax.plot([u_r[0], t_r[0] + 0.4], [u_r[1], u_r[1]], color="#B71C1C", lw=1.8, zorder=2)

    # Row 4 (Right to Left): V -> W -> X -> Finish
    draw_arrow(*get_left("V"), *get_right("W"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_left("W"), *get_right("X"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_left("X"), *get_right("Finish"), color="#B71C1C", lw=1.8)

    # Legend at bottom left
    leg_x, leg_y = 0.6, 0.4
    ax.text(leg_x, leg_y + 0.35, "PERT LEGEND:", fontsize=9, fontweight="bold", color="#263238")
    ax.plot([leg_x, leg_x + 0.8], [leg_y + 0.15, leg_y + 0.15], color="#B71C1C", lw=2.5)
    ax.text(leg_x + 0.9, leg_y + 0.15, "Critical Path (Zero Float, Direct Impact on October 10 Turnover)", fontsize=8, color="#B71C1C", va="center", fontweight="bold")
    ax.plot([leg_x, leg_x + 0.8], [leg_y - 0.05, leg_y - 0.05], color="#1565C0", lw=1.5)
    ax.text(leg_x + 0.9, leg_y - 0.05, "Non-Critical Activity (Flexible Float / Parallel Path)", fontsize=8, color="#1565C0", va="center")

    plt.tight_layout()
    png_path = os.path.join("diagrams_output", "MERYL_SHOES_PERT_CHART.png")
    svg_path = os.path.join("diagrams_output", "MERYL_SHOES_PERT_CHART.svg")
    plt.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig(svg_path, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Saved PERT:", png_path, svg_path)


# ==============================================================================
# DRAW CPM NETWORK DIAGRAM (Image 2 style)
# ==============================================================================
def draw_cpm_diagram():
    fig, ax = plt.subplots(figsize=(23, 14), dpi=300)
    ax.set_xlim(0, 21.0)
    ax.set_ylim(0, 13.5)
    ax.axis("off")

    # Title "CPM" at top left exactly as in Image 2
    ax.text(0.5, 12.8, "CPM", fontsize=26, fontweight="black", color="#111827")
    ax.text(1.8, 12.8, "CRITICAL PATH METHOD NETWORK DIAGRAM", fontsize=13, fontweight="bold", color="#1B5E20", va="center")
    ax.text(1.8, 12.45, "Meryl Shoes System | Early/Late Schedule, Duration (D), and Float [Slack] Analysis", fontsize=10, fontstyle="italic", color="#546E7A", va="center")

    # Draw Nodes
    for k, n in nodes.items():
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        x0 = x - w / 2
        y0 = y - h / 2

        if n.get("type") == "terminal":
            # Terminal box (Start / Finish)
            rect = patches.Rectangle((x0, y0), w, h, linewidth=1.8, edgecolor="#111827", facecolor="#F3F4F6", zorder=3)
            ax.add_patch(rect)
            ax.text(x, y, n["label"], ha="center", va="center", fontsize=11, fontweight="bold", color="#111827", zorder=4)
        else:
            is_crit = n["crit"]
            border_color = "#B71C1C" if is_crit else "#1565C0"
            fill_color = "#FFF8F8" if is_crit else "#F8FAFC"
            line_w = 1.5 if is_crit else 1.1

            # 1. Top Slack / Float floating box: [ Slack ]
            slack_w = 0.55
            slack_h = 0.28
            slack_x0 = x - slack_w / 2
            slack_y0 = y0 + h + 0.08
            slack_rect = patches.Rectangle((slack_x0, slack_y0), slack_w, slack_h, linewidth=1.0, edgecolor="#374151", facecolor="#FFFFFF", zorder=3)
            ax.add_patch(slack_rect)
            ax.text(x, slack_y0 + slack_h / 2, str(n["slack"]), ha="center", va="center", fontsize=8.5, fontweight="bold", color="#B71C1C" if n["slack"] == 0 else "#1565C0", zorder=4)

            # 2. Main 6-box cell (2 rows, 3 cols)
            # Row 1: ES: {es} | A: {id} | EF: {ef}
            # Row 2: LS: {ls} | D: {dur}| LF: {lf}
            main_rect = patches.Rectangle((x0, y0), w, h, linewidth=line_w, edgecolor=border_color, facecolor=fill_color, zorder=3)
            ax.add_patch(main_rect)

            # Dividing lines
            w_col1 = w * 0.32
            w_col2 = w * 0.36
            w_col3 = w * 0.32
            x_line1 = x0 + w_col1
            x_line2 = x0 + w_col1 + w_col2
            y_mid = y0 + h / 2

            ax.plot([x0, x0 + w], [y_mid, y_mid], color=border_color, lw=1.0, zorder=4) # Horizontal mid line
            ax.plot([x_line1, x_line1], [y0, y0 + h], color=border_color, lw=1.0, zorder=4) # Col 1-2 line
            ax.plot([x_line2, x_line2], [y0, y0 + h], color=border_color, lw=1.0, zorder=4) # Col 2-3 line

            # Row 1 Values (ES, Activity ID, EF)
            y_r1 = y0 + h * 0.75
            ax.text(x0 + w_col1 / 2, y_r1, f"ES: {n['es']}", ha="center", va="center", fontsize=7.2, color="#374151", zorder=5)
            ax.text(x0 + w_col1 + w_col2 / 2, y_r1, f"A: {n['id']}", ha="center", va="center", fontsize=7.8, fontweight="bold", color=border_color, zorder=5)
            ax.text(x0 + w_col1 + w_col2 + w_col3 / 2, y_r1, f"EF: {n['ef']}", ha="center", va="center", fontsize=7.2, color="#374151", zorder=5)

            # Row 2 Values (LS, Duration, LF)
            y_r2 = y0 + h * 0.25
            ax.text(x0 + w_col1 / 2, y_r2, f"LS: {n['ls']}", ha="center", va="center", fontsize=7.2, color="#374151", zorder=5)
            ax.text(x0 + w_col1 + w_col2 / 2, y_r2, f"D: {n['dur']}", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#1F2937", zorder=5)
            ax.text(x0 + w_col1 + w_col2 + w_col3 / 2, y_r2, f"LF: {n['lf']}", ha="center", va="center", fontsize=7.2, color="#374151", zorder=5)

    # Function to draw orthogonal elbow arrow
    def draw_arrow(x1, y1, x2, y2, color="#374151", lw=1.4, style="->"):
        arrow_props = dict(arrowstyle=style, color=color, lw=lw, shrinkA=0, shrinkB=0, mutation_scale=12)
        if abs(y1 - y2) < 0.05:
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props, zorder=2)
        elif abs(x1 - x2) < 0.05:
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props, zorder=2)
        else:
            x_mid = (x1 + x2) / 2
            ax.plot([x1, x_mid, x_mid, x2], [y1, y1, y2, y2], color=color, lw=lw, zorder=2)
            dx = 0.05 if x2 > x_mid else -0.05
            ax.annotate("", xy=(x2, y2), xytext=(x2 - dx, y2), arrowprops=arrow_props, zorder=2)

    def get_right(key): return nodes[key]["x"] + nodes[key]["w"]/2, nodes[key]["y"]
    def get_left(key): return nodes[key]["x"] - nodes[key]["w"]/2, nodes[key]["y"]

    # Connect nodes
    draw_arrow(*get_right("Start"), *get_left("A"))
    draw_arrow(*get_right("A"), *get_left("B"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("B"), *get_left("C"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("C"), *get_left("D"), color="#B71C1C", lw=1.8)

    draw_arrow(*get_right("D"), *get_left("E"), color="#1565C0", lw=1.4)
    draw_arrow(*get_right("D"), *get_left("F"), color="#B71C1C", lw=1.8)

    draw_arrow(*get_right("F"), *get_left("G"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("G"), *get_left("H"), color="#B71C1C", lw=1.8)

    # Row 1 -> Row 2 Turn
    h_r = get_right("H")
    i_r = get_right("I")
    ax.plot([h_r[0], h_r[0] + 0.4, h_r[0] + 0.4, i_r[0] + 0.4, i_r[0] + 0.4, i_r[0]], 
            [h_r[1], h_r[1], (h_r[1] + i_r[1])/2, (h_r[1] + i_r[1])/2, i_r[1], i_r[1]], color="#B71C1C", lw=1.8, zorder=2)
    ax.annotate("", xy=(i_r[0], i_r[1]), xytext=(i_r[0] + 0.05, i_r[1]), arrowprops=dict(arrowstyle="->", color="#B71C1C", lw=1.8, mutation_scale=12), zorder=2)

    e_r = get_right("E")
    ax.plot([e_r[0], h_r[0] + 0.4], [e_r[1], e_r[1]], color="#1565C0", lw=1.2, zorder=2)

    # Row 2 (Right to Left)
    draw_arrow(*get_left("I"), *get_right("J"), color="#1565C0", lw=1.4)
    draw_arrow(*get_left("I"), *get_right("K"), color="#B71C1C", lw=1.8)

    draw_arrow(*get_left("J"), *get_right("L"), color="#1565C0", lw=1.4)
    draw_arrow(*get_left("K"), *get_right("L"), color="#B71C1C", lw=1.8)

    draw_arrow(*get_left("L"), *get_right("M"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_left("L"), *get_right("N"), color="#B71C1C", lw=1.8)

    draw_arrow(nodes["J"]["x"] - nodes["J"]["w"]/2, nodes["J"]["y"], nodes["O"]["x"] + nodes["O"]["w"]/2, nodes["O"]["y"] + 0.2, color="#1565C0", lw=1.2)

    # Row 2 -> Row 3 Turn
    o_l = get_left("O")
    m_l = get_left("M")
    n_l = get_left("N")
    p_l = get_left("P")

    ax.plot([m_l[0], o_l[0] - 0.4, o_l[0] - 0.4, p_l[0] - 0.4, p_l[0] - 0.4, p_l[0]], 
            [m_l[1], m_l[1], (m_l[1] + p_l[1])/2, (m_l[1] + p_l[1])/2, p_l[1], p_l[1]], color="#B71C1C", lw=1.8, zorder=2)
    ax.annotate("", xy=(p_l[0], p_l[1]), xytext=(p_l[0] - 0.05, p_l[1]), arrowprops=dict(arrowstyle="->", color="#B71C1C", lw=1.8, mutation_scale=12), zorder=2)
    ax.plot([n_l[0], o_l[0] - 0.4], [n_l[1], n_l[1]], color="#B71C1C", lw=1.8, zorder=2)
    ax.plot([o_l[0], o_l[0] - 0.4], [o_l[1], o_l[1]], color="#1565C0", lw=1.2, zorder=2)

    # Row 3 (Left to Right)
    draw_arrow(*get_right("P"), *get_left("Q"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("P"), *get_left("R"), color="#1565C0", lw=1.4)

    draw_arrow(*get_right("Q"), *get_left("S"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("R"), *get_left("S"), color="#1565C0", lw=1.4)

    draw_arrow(*get_right("S"), *get_left("T"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_right("S"), *get_left("U"), color="#B71C1C", lw=1.8)

    # Row 3 -> Row 4 Turn
    t_r = get_right("T")
    u_r = get_right("U")
    v_r = get_right("V")

    ax.plot([t_r[0], t_r[0] + 0.4, t_r[0] + 0.4, v_r[0] + 0.4, v_r[0] + 0.4, v_r[0]], 
            [t_r[1], t_r[1], (t_r[1] + v_r[1])/2, (t_r[1] + v_r[1])/2, v_r[1], v_r[1]], color="#B71C1C", lw=1.8, zorder=2)
    ax.annotate("", xy=(v_r[0], v_r[1]), xytext=(v_r[0] + 0.05, v_r[1]), arrowprops=dict(arrowstyle="->", color="#B71C1C", lw=1.8, mutation_scale=12), zorder=2)
    ax.plot([u_r[0], t_r[0] + 0.4], [u_r[1], u_r[1]], color="#B71C1C", lw=1.8, zorder=2)

    # Row 4 (Right to Left)
    draw_arrow(*get_left("V"), *get_right("W"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_left("W"), *get_right("X"), color="#B71C1C", lw=1.8)
    draw_arrow(*get_left("X"), *get_right("Finish"), color="#B71C1C", lw=1.8)

    # Node structure legend at bottom left
    leg_x, leg_y = 0.6, 0.4
    ax.text(leg_x, leg_y + 0.4, "CPM NODE NOTATION:", fontsize=9, fontweight="bold", color="#1F2937")
    ax.text(leg_x, leg_y + 0.15, "• Upper Box: Slack / Float = LS - ES (0 = Critical Path)", fontsize=8, color="#B71C1C", fontweight="bold")
    ax.text(leg_x, leg_y - 0.08, "• Grid: ES = Early Start | A = Activity ID | EF = Early Finish", fontsize=8, color="#374151")
    ax.text(leg_x, leg_y - 0.30, "        LS = Late Start  | D = Duration (Days) | LF = Late Finish", fontsize=8, color="#374151")

    plt.tight_layout()
    png_path = os.path.join("diagrams_output", "MERYL_SHOES_CPM_NETWORK_DIAGRAM.png")
    svg_path = os.path.join("diagrams_output", "MERYL_SHOES_CPM_NETWORK_DIAGRAM.svg")
    plt.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig(svg_path, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Saved CPM:", png_path, svg_path)


if __name__ == "__main__":
    draw_pert_diagram()
    draw_cpm_diagram()

