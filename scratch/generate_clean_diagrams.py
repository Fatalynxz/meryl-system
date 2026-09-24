import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs("diagrams_output", exist_ok=True)

# Node dimensions
W = 2.15
H = 0.94

nodes = {
    # ================= ROW 1 (Left to Right) =================
    "Start": {"label": "Start", "type": "terminal", "x": 0.6, "y": 11.8, "w": 1.25, "h": 0.60},
    "A": {
        "id": "A", "wbs": "1.1", "name": "Requirements Elicitation\n& Stakeholder Interviews",
        "dur": 14, "es": 0, "ef": 14, "ls": 0, "lf": 14, "slack": 0, "crit": True,
        "x": 2.8, "y": 11.8, "w": W, "h": H
    },
    "B": {
        "id": "B", "wbs": "1.2", "name": "Process Observation &\nInventory Workflow Audit",
        "dur": 16, "es": 5, "ef": 21, "ls": 5, "lf": 21, "slack": 0, "crit": True,
        "x": 5.4, "y": 11.8, "w": W, "h": H
    },
    "C": {
        "id": "C", "wbs": "2.1", "name": "UI/UX Wireframing, DFDs\n(0-2) & ERD Modeling",
        "dur": 16, "es": 15, "ef": 31, "ls": 15, "lf": 31, "slack": 0, "crit": True,
        "x": 8.0, "y": 11.8, "w": W, "h": H
    },
    "D": {
        "id": "D", "wbs": "2.2", "name": "System Architecture &\nSecurity Design (JWT/Crypt)",
        "dur": 16, "es": 21, "ef": 37, "ls": 21, "lf": 37, "slack": 0, "crit": True,
        "x": 10.6, "y": 11.8, "w": W, "h": H
    },
    "E": {
        "id": "E", "wbs": "2.3", "name": "Analytics Modeling &\nPromotions Design",
        "dur": 18, "es": 27, "ef": 45, "ls": 29, "lf": 47, "slack": 2, "crit": False,
        "x": 13.2, "y": 12.6, "w": W, "h": H
    },
    "F": {
        "id": "F", "wbs": "3.1", "name": "Master Catalog & Item\nParameters Design",
        "dur": 14, "es": 38, "ef": 52, "ls": 38, "lf": 52, "slack": 0, "crit": True,
        "x": 13.2, "y": 11.0, "w": W, "h": H
    },
    "G": {
        "id": "G", "wbs": "3.2", "name": "POS Terminal, Multi-Tender\n& Receipt Design",
        "dur": 14, "es": 41, "ef": 55, "ls": 41, "lf": 55, "slack": 0, "crit": True,
        "x": 15.8, "y": 11.8, "w": W, "h": H
    },
    "H": {
        "id": "H", "wbs": "3.3", "name": "Replacement Intake &\nHardware Camera QR Design",
        "dur": 16, "es": 44, "ef": 60, "ls": 44, "lf": 60, "slack": 0, "crit": True,
        "x": 18.4, "y": 11.8, "w": W, "h": H
    },

    # ================= ROW 2 (Right to Left) =================
    "I": {
        "id": "I", "wbs": "4.1", "name": "Database Setup, RLS &\nCloud Storage Buckets",
        "dur": 15, "es": 54, "ef": 69, "ls": 54, "lf": 69, "slack": 0, "crit": True,
        "x": 18.4, "y": 8.8, "w": W, "h": H
    },
    "J": {
        "id": "J", "wbs": "4.2", "name": "Front-End UI Development\n(React, TS, Tailwind)",
        "dur": 24, "es": 60, "ef": 84, "ls": 62, "lf": 86, "slack": 2, "crit": False,
        "x": 15.6, "y": 9.6, "w": W, "h": H
    },
    "K": {
        "id": "K", "wbs": "4.3", "name": "Back-End API Services &\nSession Cryptography",
        "dur": 24, "es": 64, "ef": 88, "ls": 64, "lf": 88, "slack": 0, "crit": True,
        "x": 15.6, "y": 8.0, "w": W, "h": H
    },
    "L": {
        "id": "L", "wbs": "4.4", "name": "Core POS Checkout &\nThermal Receipt Engine",
        "dur": 22, "es": 71, "ef": 93, "ls": 71, "lf": 93, "slack": 0, "crit": True,
        "x": 12.8, "y": 8.8, "w": W, "h": H
    },
    "M": {
        "id": "M", "wbs": "4.5", "name": "Predictive Sales Forecast\n& Brevo Marketing Blast",
        "dur": 22, "es": 76, "ef": 98, "ls": 76, "lf": 98, "slack": 0, "crit": True,
        "x": 10.0, "y": 9.6, "w": W, "h": H
    },
    "N": {
        "id": "N", "wbs": "4.6", "name": "Replacement Intake &\nHardware Camera Scanner",
        "dur": 20, "es": 78, "ef": 98, "ls": 78, "lf": 98, "slack": 0, "crit": True,
        "x": 10.0, "y": 8.0, "w": W, "h": H
    },
    "O": {
        "id": "O", "wbs": "5.1", "name": "Module Unit Testing &\nWhite-Box Test Cases",
        "dur": 22, "es": 84, "ef": 106, "ls": 86, "lf": 108, "slack": 2, "crit": False,
        "x": 6.8, "y": 8.8, "w": W, "h": H
    },

    # ================= ROW 3 (Left to Right) =================
    "P": {
        "id": "P", "wbs": "5.2", "name": "Subsystem & Cross-Tab\nIntegration Testing",
        "dur": 21, "es": 95, "ef": 116, "ls": 95, "lf": 116, "slack": 0, "crit": True,
        "x": 2.8, "y": 5.8, "w": W, "h": H
    },
    "Q": {
        "id": "Q", "wbs": "5.3", "name": "Functional Black-Box\nAlpha Testing (POS/Inv)",
        "dur": 22, "es": 105, "ef": 127, "ls": 105, "lf": 127, "slack": 0, "crit": True,
        "x": 8.0, "y": 6.6, "w": W, "h": H
    },
    "R": {
        "id": "R", "wbs": "5.4", "name": "Security, Pen-Testing &\nRLS Lockout Validation",
        "dur": 21, "es": 112, "ef": 133, "ls": 113, "lf": 134, "slack": 1, "crit": False,
        "x": 8.0, "y": 5.0, "w": W, "h": H
    },
    "S": {
        "id": "S", "wbs": "5.5", "name": "Full System Stress &\nHardware Concurrency",
        "dur": 20, "es": 119, "ef": 139, "ls": 119, "lf": 139, "slack": 0, "crit": True,
        "x": 13.2, "y": 5.8, "w": W, "h": H
    },
    "T": {
        "id": "T", "wbs": "5.6", "name": "Bug Resolution, Retesting\n& System Hardening",
        "dur": 19, "es": 128, "ef": 147, "ls": 128, "lf": 147, "slack": 0, "crit": True,
        "x": 18.4, "y": 6.6, "w": W, "h": H
    },
    "U": {
        "id": "U", "wbs": "5.7", "name": "ISO/IEC 25010:2011 Product\nQuality Evaluation",
        "dur": 14, "es": 133, "ef": 147, "ls": 133, "lf": 147, "slack": 0, "crit": True,
        "x": 18.4, "y": 5.0, "w": W, "h": H
    },

    # ================= ROW 4 (Right to Left) =================
    "V": {
        "id": "V", "wbs": "6.1", "name": "Beta Testing & User\nAcceptance Testing (UAT)",
        "dur": 8, "es": 144, "ef": 152, "ls": 144, "lf": 152, "slack": 0, "crit": True,
        "x": 18.4, "y": 2.6, "w": W, "h": H
    },
    "W": {
        "id": "W", "wbs": "6.2", "name": "Client Feedback &\nUI Final Polish",
        "dur": 6, "es": 149, "ef": 155, "ls": 149, "lf": 155, "slack": 0, "crit": True,
        "x": 13.2, "y": 2.6, "w": W, "h": H
    },
    "X": {
        "id": "X", "wbs": "6.3", "name": "Final Documentation &\nSystem Turnover Closeout",
        "dur": 7, "es": 152, "ef": 159, "ls": 152, "lf": 159, "slack": 0, "crit": True,
        "x": 8.0, "y": 2.6, "w": W, "h": H
    },
    "Finish": {"label": "Finish", "type": "terminal", "x": 2.8, "y": 2.6, "w": 1.25, "h": 0.60}
}


def get_edge(k, side):
    n = nodes[k]
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    if side == "right": return x + w/2, y
    if side == "left": return x - w/2, y
    if side == "top": return x, y + h/2
    if side == "bottom": return x, y - h/2
    return x, y


def draw_orthogonal_arrow(ax, x1, y1, x2, y2, color="#B71C1C", lw=1.8, style="->", mid_x=None, mid_y=None):
    arrow_props = dict(arrowstyle=style, color=color, lw=lw, shrinkA=0, shrinkB=0, mutation_scale=12)
    if abs(y1 - y2) < 0.05:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props, zorder=2)
    elif abs(x1 - x2) < 0.05:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props, zorder=2)
    else:
        if mid_x is not None:
            ax.plot([x1, mid_x, mid_x, x2], [y1, y1, y2, y2], color=color, lw=lw, zorder=2)
            dx = 0.05 if x2 > mid_x else -0.05
            ax.annotate("", xy=(x2, y2), xytext=(x2 - dx, y2), arrowprops=arrow_props, zorder=2)
        elif mid_y is not None:
            ax.plot([x1, x1, x2, x2], [y1, mid_y, mid_y, y2], color=color, lw=lw, zorder=2)
            dy = 0.05 if y2 > mid_y else -0.05
            ax.annotate("", xy=(x2, y2), xytext=(x2, y2 - dy), arrowprops=arrow_props, zorder=2)
        else:
            mx = (x1 + x2) / 2
            ax.plot([x1, mx, mx, x2], [y1, y1, y2, y2], color=color, lw=lw, zorder=2)
            dx = 0.05 if x2 > mx else -0.05
            ax.annotate("", xy=(x2, y2), xytext=(x2 - dx, y2), arrowprops=arrow_props, zorder=2)


# ==============================================================================
# DRAW PERT NETWORK DIAGRAM
# ==============================================================================
def draw_pert_diagram(bw=False):
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 21.0)
    ax.set_ylim(0, 15.0)
    ax.axis("off")

    if not bw:
        # Header / Academic Titles
        ax.text(10.5, 14.45, "CARLOS HILADO MEMORIAL STATE UNIVERSITY — COLLEGE OF COMPUTER STUDIES", 
                ha="center", va="center", fontsize=14, fontweight="bold", color="#1B5E20")
        ax.text(10.5, 14.1, "PROGRAM EVALUATION AND REVIEW TECHNIQUE (PERT) NETWORK DIAGRAM", 
                ha="center", va="center", fontsize=12.5, fontweight="bold", color="#111827")
        ax.text(10.5, 13.78, "Meryl Shoes System | Critical Path: A → B → C → D → F → G → H → I → K → L → M/N → P → Q → S → T/U → V → W → X (159 Days)", 
                ha="center", va="center", fontsize=9.8, fontstyle="italic", color="#4B5563")

    # Draw Nodes
    for k, n in nodes.items():
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        x0 = x - w / 2
        y0 = y - h / 2

        if n.get("type") == "terminal":
            edge_c = "#000000" if bw else "#1B5E20"
            fill_c = "#FFFFFF" if bw else "#E8F5E9"
            text_c = "#000000" if bw else "#1B5E20"
            rect = patches.Rectangle((x0, y0), w, h, linewidth=1.5, edgecolor=edge_c, facecolor=fill_c, zorder=3)
            ax.add_patch(rect)
            ax.text(x, y, n["label"], ha="center", va="center", fontsize=13, fontweight="bold", color=text_c, zorder=4)
        else:
            is_crit = n["crit"]
            border_color = "#000000" if bw else ("#B71C1C" if is_crit else "#1565C0")
            fill_color = "#FFFFFF" if bw else ("#FFF8F8" if is_crit else "#F4F8FD")
            line_w = 1.2 if bw else (1.6 if is_crit else 1.2)
            
            rect = patches.Rectangle((x0, y0), w, h, linewidth=line_w, edgecolor=border_color, facecolor=fill_color, zorder=3)
            ax.add_patch(rect)

            h_top = 0.48
            h_bot = h - h_top
            
            # Divider lines
            ax.plot([x0, x0 + w], [y0 + h_bot, y0 + h_bot], color=border_color, lw=1.0, zorder=4)
            ax.plot([x0 + w/2, x0 + w/2], [y0, y0 + h_bot], color=border_color, lw=1.0, zorder=4)
            ax.plot([x0, x0 + w], [y0 + h_bot/2, y0 + h_bot/2], color=border_color, lw=0.8, zorder=4)

            # Top Text (Task Name) - larger & bold
            ax.text(x, y0 + h_bot + h_top/2, n["name"], ha="center", va="center", fontsize=8.2, fontweight="bold", color="#000000" if bw else "#111827", zorder=5)

            # Bottom Left: Start & Finish - larger & bold
            ax.text(x0 + 0.08, y0 + h_bot * 0.75, f"Start: {n['es']}", ha="left", va="center", fontsize=7.8, fontweight="bold", color="#000000" if bw else "#374151", zorder=5)
            ax.text(x0 + 0.08, y0 + h_bot * 0.25, f"Finish: {n['ef']}", ha="left", va="center", fontsize=7.8, fontweight="bold", color="#000000" if bw else "#374151", zorder=5)

            # Bottom Right: ID & Duration - larger & bold
            ax.text(x0 + w/2 + 0.08, y0 + h_bot * 0.75, f"ID: {n['id']} ({n['wbs']})", ha="left", va="center", fontsize=7.8, fontweight="bold", color="#000000" if bw else border_color, zorder=5)
            ax.text(x0 + w/2 + 0.08, y0 + h_bot * 0.25, f"Duration: {n['dur']}", ha="left", va="center", fontsize=7.8, fontweight="bold", color="#000000" if bw else "#374151", zorder=5)

    crit_color = "#000000" if bw else "#B71C1C"
    float_color = "#000000" if bw else "#1565C0"
    base_color = "#000000" if bw else "#374151"
    line_w = 1.3 if bw else 1.8
    float_lw = 1.3 if bw else 1.3

    # ================= CONNECTIONS =================
    # Row 1 (Left to Right)
    draw_orthogonal_arrow(ax, *get_edge("Start", "right"), *get_edge("A", "left"), color=base_color, lw=1.3)
    draw_orthogonal_arrow(ax, *get_edge("A", "right"), *get_edge("B", "left"), color=crit_color, lw=line_w)
    draw_orthogonal_arrow(ax, *get_edge("B", "right"), *get_edge("C", "left"), color=crit_color, lw=line_w)
    draw_orthogonal_arrow(ax, *get_edge("C", "right"), *get_edge("D", "left"), color=crit_color, lw=line_w)

    # D -> E (Float) and D -> F (Critical)
    draw_orthogonal_arrow(ax, *get_edge("D", "right"), *get_edge("E", "left"), color=float_color, lw=float_lw, mid_x=11.9)
    draw_orthogonal_arrow(ax, *get_edge("D", "right"), *get_edge("F", "left"), color=crit_color, lw=line_w, mid_x=11.9)

    # E & F -> G
    draw_orthogonal_arrow(ax, *get_edge("E", "right"), *get_edge("G", "left"), color=float_color, lw=float_lw, mid_x=14.5)
    draw_orthogonal_arrow(ax, *get_edge("F", "right"), *get_edge("G", "left"), color=crit_color, lw=line_w, mid_x=14.5)

    # G -> H
    draw_orthogonal_arrow(ax, *get_edge("G", "right"), *get_edge("H", "left"), color=crit_color, lw=line_w)

    # Row 1 -> Row 2 Turn: H right edge -> x=19.9 -> down to y=8.8 -> into I right edge
    h_r = get_edge("H", "right")
    i_r = get_edge("I", "right")
    ax.plot([h_r[0], 19.85, 19.85, i_r[0]], [h_r[1], h_r[1], i_r[1], i_r[1]], color=crit_color, lw=line_w, zorder=2)
    ax.annotate("", xy=(i_r[0], i_r[1]), xytext=(i_r[0] + 0.05, i_r[1]), 
                arrowprops=dict(arrowstyle="->", color=crit_color, lw=line_w, mutation_scale=12), zorder=2)

    # Row 2 (Right to Left)
    # I -> J (Float) and I -> K (Critical)
    draw_orthogonal_arrow(ax, *get_edge("I", "left"), *get_edge("J", "right"), color=float_color, lw=float_lw, mid_x=17.0)
    draw_orthogonal_arrow(ax, *get_edge("I", "left"), *get_edge("K", "right"), color=crit_color, lw=line_w, mid_x=17.0)

    # J & K -> L
    draw_orthogonal_arrow(ax, *get_edge("J", "left"), *get_edge("L", "right"), color=float_color, lw=float_lw, mid_x=14.2)
    draw_orthogonal_arrow(ax, *get_edge("K", "left"), *get_edge("L", "right"), color=crit_color, lw=line_w, mid_x=14.2)

    # L -> M & N
    draw_orthogonal_arrow(ax, *get_edge("L", "left"), *get_edge("M", "right"), color=crit_color, lw=line_w, mid_x=11.4)
    draw_orthogonal_arrow(ax, *get_edge("L", "left"), *get_edge("N", "right"), color=crit_color, lw=line_w, mid_x=11.4)

    # J -> O (Unit testing path over the top at y=10.8)
    j_r = get_edge("J", "left")
    o_t = get_edge("O", "top")
    ax.plot([j_r[0], 14.3, 14.3, o_t[0], o_t[0]], [j_r[1], j_r[1], 10.8, 10.8, o_t[1]], color=float_color, lw=float_lw, zorder=2)
    ax.annotate("", xy=(o_t[0], o_t[1]), xytext=(o_t[0], o_t[1] + 0.05), arrowprops=dict(arrowstyle="->", color=float_color, lw=float_lw, mutation_scale=10), zorder=2)

    # M, N, O converge into P (Dedicated parallel tiers, drop straight into P top)
    m_l = get_edge("M", "left")
    n_l = get_edge("N", "left")
    o_l = get_edge("O", "left")
    p_t = get_edge("P", "top")

    # M runs at y=10.15, N runs at y=7.85 (clear of Q slack box), O runs at y=8.8 to x=2.8
    ax.plot([m_l[0], 8.4, 8.4, p_t[0], p_t[0]], [m_l[1], m_l[1], 10.15, 10.15, p_t[1]], color=crit_color, lw=line_w, zorder=2)
    ax.plot([n_l[0], 8.4, 8.4, p_t[0]], [n_l[1], n_l[1], 7.85, 7.85], color=crit_color, lw=line_w, zorder=2)
    ax.plot([o_l[0], p_t[0]], [o_l[1], o_l[1]], color=float_color, lw=float_lw, zorder=2)
    ax.annotate("", xy=(p_t[0], p_t[1]), xytext=(p_t[0], p_t[1] + 0.05), 
                arrowprops=dict(arrowstyle="->", color=crit_color, lw=line_w, mutation_scale=12), zorder=2)

    # Row 3 (Left to Right)
    # P -> Q (Critical) & R (Float)
    draw_orthogonal_arrow(ax, *get_edge("P", "right"), *get_edge("Q", "left"), color=crit_color, lw=line_w, mid_x=5.4)
    draw_orthogonal_arrow(ax, *get_edge("P", "right"), *get_edge("R", "left"), color=float_color, lw=float_lw, mid_x=5.4)

    # Q & R -> S
    draw_orthogonal_arrow(ax, *get_edge("Q", "right"), *get_edge("S", "left"), color=crit_color, lw=line_w, mid_x=10.6)
    draw_orthogonal_arrow(ax, *get_edge("R", "right"), *get_edge("S", "left"), color=float_color, lw=float_lw, mid_x=10.6)

    # S -> T (Critical) & U (Critical)
    draw_orthogonal_arrow(ax, *get_edge("S", "right"), *get_edge("T", "left"), color=crit_color, lw=line_w, mid_x=15.8)
    draw_orthogonal_arrow(ax, *get_edge("S", "right"), *get_edge("U", "left"), color=crit_color, lw=line_w, mid_x=15.8)

    # Row 3 -> Row 4 Turn: T & U right edge -> x=19.85 -> down to y=2.6 -> into V right edge
    t_r = get_edge("T", "right")
    u_r = get_edge("U", "right")
    v_r = get_edge("V", "right")

    ax.plot([t_r[0], 19.85, 19.85, v_r[0]], [t_r[1], t_r[1], v_r[1], v_r[1]], color=crit_color, lw=line_w, zorder=2)
    ax.plot([u_r[0], 19.85], [u_r[1], u_r[1]], color=crit_color, lw=line_w, zorder=2)
    ax.annotate("", xy=(v_r[0], v_r[1]), xytext=(v_r[0] + 0.05, v_r[1]), 
                arrowprops=dict(arrowstyle="->", color=crit_color, lw=line_w, mutation_scale=12), zorder=2)

    # Row 4 (Right to Left)
    draw_orthogonal_arrow(ax, *get_edge("V", "left"), *get_edge("W", "right"), color=crit_color, lw=line_w)
    draw_orthogonal_arrow(ax, *get_edge("W", "left"), *get_edge("X", "right"), color=crit_color, lw=line_w)
    draw_orthogonal_arrow(ax, *get_edge("X", "left"), *get_edge("Finish", "right"), color=crit_color, lw=line_w)

    if not bw:
        # Legend at bottom left
        leg_x, leg_y = 0.8, 0.7
        ax.text(leg_x, leg_y + 0.38, "PERT LEGEND & SPECIFICATIONS:", fontsize=9.5, fontweight="bold", color="#111827")
        ax.plot([leg_x, leg_x + 0.8], [leg_y + 0.15, leg_y + 0.15], color="#B71C1C", lw=2.5)
        ax.text(leg_x + 0.9, leg_y + 0.15, "Critical Path (Zero Float, Direct Impact on October 10 System Turnover)", fontsize=8.5, color="#B71C1C", va="center", fontweight="bold")
        ax.plot([leg_x, leg_x + 0.8], [leg_y - 0.08, leg_y - 0.08], color="#1565C0", lw=1.5)
        ax.text(leg_x + 0.9, leg_y - 0.08, "Non-Critical Activity (Parallel Path with Float / Schedule Buffer)", fontsize=8.5, color="#1565C0", va="center")

    plt.tight_layout()
    suffix = "_BW" if bw else ""
    png_path = os.path.join("diagrams_output", f"MERYL_SHOES_PERT_CHART{suffix}.png")
    svg_path = os.path.join("diagrams_output", f"MERYL_SHOES_PERT_CHART{suffix}.svg")
    plt.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig(svg_path, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Clean PERT (BW={bw}) generated successfully.")


# ==============================================================================
# DRAW CPM NETWORK DIAGRAM
# ==============================================================================
# DRAW CPM NETWORK DIAGRAM (Pure Black & White, No Legend/Header text)
# ==============================================================================
def draw_cpm_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 21.0)
    ax.set_ylim(0, 15.0)
    ax.axis("off")

    # Title "CPM" in bold black sans-serif at top left (matches reference Image 2)
    ax.text(0.6, 14.2, "CPM", fontsize=36, fontweight="black", color="#000000")

    # Draw Nodes in pure black & white
    for k, n in nodes.items():
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        x0 = x - w / 2
        y0 = y - h / 2

        if n.get("type") == "terminal":
            rect = patches.Rectangle((x0, y0), w, h, linewidth=1.5, edgecolor="#000000", facecolor="#FFFFFF", zorder=3)
            ax.add_patch(rect)
            ax.text(x, y, n["label"], ha="center", va="center", fontsize=13, fontweight="bold", color="#000000", zorder=4)
        else:
            line_w = 1.2

            # 1. Floating Slack / Float box at the top (enlarged & prominent)
            slack_w = 0.65
            slack_h = 0.32
            slack_x0 = x - slack_w / 2
            slack_y0 = y0 + h + 0.08
            slack_rect = patches.Rectangle((slack_x0, slack_y0), slack_w, slack_h, linewidth=1.1, edgecolor="#000000", facecolor="#FFFFFF", zorder=3)
            ax.add_patch(slack_rect)
            ax.text(x, slack_y0 + slack_h / 2, str(n["slack"]), ha="center", va="center", fontsize=11.5, fontweight="bold", color="#000000", zorder=4)

            # 2. Main 6-box cell (2 rows, 3 cols) in pure black & white
            main_rect = patches.Rectangle((x0, y0), w, h, linewidth=line_w, edgecolor="#000000", facecolor="#FFFFFF", zorder=3)
            ax.add_patch(main_rect)

            w_col1 = w * 0.33
            w_col2 = w * 0.34
            w_col3 = w * 0.33
            x_line1 = x0 + w_col1
            x_line2 = x0 + w_col1 + w_col2
            y_mid = y0 + h / 2

            ax.plot([x0, x0 + w], [y_mid, y_mid], color="#000000", lw=0.9, zorder=4)
            ax.plot([x_line1, x_line1], [y0, y0 + h], color="#000000", lw=0.9, zorder=4)
            ax.plot([x_line2, x_line2], [y0, y0 + h], color="#000000", lw=0.9, zorder=4)

            # Row 1: ES, Activity ID, EF (Clear, bold, high-contrast)
            y_r1 = y0 + h * 0.75
            ax.text(x0 + w_col1 / 2, y_r1, f"ES: {n['es']}", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#000000", zorder=5)
            ax.text(x0 + w_col1 + w_col2 / 2, y_r1, f"A: {n['id']}", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#000000", zorder=5)
            ax.text(x0 + w_col1 + w_col2 + w_col3 / 2, y_r1, f"EF: {n['ef']}", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#000000", zorder=5)

            # Row 2: LS, Duration, LF (Clear, bold, high-contrast)
            y_r2 = y0 + h * 0.25
            ax.text(x0 + w_col1 / 2, y_r2, f"LS: {n['ls']}", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#000000", zorder=5)
            ax.text(x0 + w_col1 + w_col2 / 2, y_r2, f"D: {n['dur']}", ha="center", va="center", fontsize=10.2, fontweight="bold", color="#000000", zorder=5)
            ax.text(x0 + w_col1 + w_col2 + w_col3 / 2, y_r2, f"LF: {n['lf']}", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#000000", zorder=5)

    # Connections - all pure black lines and arrows
    # Row 1 (Left to Right)
    draw_orthogonal_arrow(ax, *get_edge("Start", "right"), *get_edge("A", "left"), color="#000000", lw=1.3)
    draw_orthogonal_arrow(ax, *get_edge("A", "right"), *get_edge("B", "left"), color="#000000", lw=1.3)
    draw_orthogonal_arrow(ax, *get_edge("B", "right"), *get_edge("C", "left"), color="#000000", lw=1.3)
    draw_orthogonal_arrow(ax, *get_edge("C", "right"), *get_edge("D", "left"), color="#000000", lw=1.3)

    # D -> E and D -> F
    draw_orthogonal_arrow(ax, *get_edge("D", "right"), *get_edge("E", "left"), color="#000000", lw=1.3, mid_x=11.9)
    draw_orthogonal_arrow(ax, *get_edge("D", "right"), *get_edge("F", "left"), color="#000000", lw=1.3, mid_x=11.9)

    # E & F -> G
    draw_orthogonal_arrow(ax, *get_edge("E", "right"), *get_edge("G", "left"), color="#000000", lw=1.3, mid_x=14.5)
    draw_orthogonal_arrow(ax, *get_edge("F", "right"), *get_edge("G", "left"), color="#000000", lw=1.3, mid_x=14.5)

    # G -> H
    draw_orthogonal_arrow(ax, *get_edge("G", "right"), *get_edge("H", "left"), color="#000000", lw=1.3)

    # Row 1 -> Row 2 Turn: H right edge -> x=19.85 -> down to y=8.8 -> into I right edge
    h_r = get_edge("H", "right")
    i_r = get_edge("I", "right")
    ax.plot([h_r[0], 19.85, 19.85, i_r[0]], [h_r[1], h_r[1], i_r[1], i_r[1]], color="#000000", lw=1.3, zorder=2)
    ax.annotate("", xy=(i_r[0], i_r[1]), xytext=(i_r[0] + 0.05, i_r[1]), 
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.3, mutation_scale=12), zorder=2)

    # Row 2 (Right to Left)
    draw_orthogonal_arrow(ax, *get_edge("I", "left"), *get_edge("J", "right"), color="#000000", lw=1.3, mid_x=17.0)
    draw_orthogonal_arrow(ax, *get_edge("I", "left"), *get_edge("K", "right"), color="#000000", lw=1.3, mid_x=17.0)

    draw_orthogonal_arrow(ax, *get_edge("J", "left"), *get_edge("L", "right"), color="#000000", lw=1.3, mid_x=14.2)
    draw_orthogonal_arrow(ax, *get_edge("K", "left"), *get_edge("L", "right"), color="#000000", lw=1.3, mid_x=14.2)

    draw_orthogonal_arrow(ax, *get_edge("L", "left"), *get_edge("M", "right"), color="#000000", lw=1.3, mid_x=11.4)
    draw_orthogonal_arrow(ax, *get_edge("L", "left"), *get_edge("N", "right"), color="#000000", lw=1.3, mid_x=11.4)

    # J -> O (Unit testing path over the top of M's slack box at y=10.8)
    j_r = get_edge("J", "left")
    o_slack_top = (nodes["O"]["x"], nodes["O"]["y"] + nodes["O"]["h"]/2 + 0.36)
    ax.plot([j_r[0], 14.3, 14.3, o_slack_top[0], o_slack_top[0]], [j_r[1], j_r[1], 10.8, 10.8, o_slack_top[1]], color="#000000", lw=1.3, zorder=2)
    ax.annotate("", xy=o_slack_top, xytext=(o_slack_top[0], o_slack_top[1] + 0.05), arrowprops=dict(arrowstyle="->", color="#000000", lw=1.3, mutation_scale=10), zorder=2)

    # M, N, O converge into P
    m_l = get_edge("M", "left")
    n_l = get_edge("N", "left")
    o_l = get_edge("O", "left")
    p_slack_top = (nodes["P"]["x"], nodes["P"]["y"] + nodes["P"]["h"]/2 + 0.36)

    ax.plot([m_l[0], 8.4, 8.4, p_slack_top[0], p_slack_top[0]], [m_l[1], m_l[1], 10.15, 10.15, p_slack_top[1]], color="#000000", lw=1.3, zorder=2)
    ax.plot([n_l[0], 8.4, 8.4, p_slack_top[0]], [n_l[1], n_l[1], 7.85, 7.85], color="#000000", lw=1.3, zorder=2)
    ax.plot([o_l[0], p_slack_top[0]], [o_l[1], o_l[1]], color="#000000", lw=1.3, zorder=2)
    ax.annotate("", xy=p_slack_top, xytext=(p_slack_top[0], p_slack_top[1] + 0.05), 
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.3, mutation_scale=12), zorder=2)

    # Row 3 (Left to Right)
    draw_orthogonal_arrow(ax, *get_edge("P", "right"), *get_edge("Q", "left"), color="#000000", lw=1.3, mid_x=5.4)
    draw_orthogonal_arrow(ax, *get_edge("P", "right"), *get_edge("R", "left"), color="#000000", lw=1.3, mid_x=5.4)

    draw_orthogonal_arrow(ax, *get_edge("Q", "right"), *get_edge("S", "left"), color="#000000", lw=1.3, mid_x=10.6)
    draw_orthogonal_arrow(ax, *get_edge("R", "right"), *get_edge("S", "left"), color="#000000", lw=1.3, mid_x=10.6)

    draw_orthogonal_arrow(ax, *get_edge("S", "right"), *get_edge("T", "left"), color="#000000", lw=1.3, mid_x=15.8)
    draw_orthogonal_arrow(ax, *get_edge("S", "right"), *get_edge("U", "left"), color="#000000", lw=1.3, mid_x=15.8)

    # Row 3 -> Row 4 Turn: T & U right edge -> x=19.85 -> down to y=2.6 -> into V right edge
    t_r = get_edge("T", "right")
    u_r = get_edge("U", "right")
    v_r = get_edge("V", "right")

    ax.plot([t_r[0], 19.85, 19.85, v_r[0]], [t_r[1], t_r[1], v_r[1], v_r[1]], color="#000000", lw=1.3, zorder=2)
    ax.plot([u_r[0], 19.85], [u_r[1], u_r[1]], color="#000000", lw=1.3, zorder=2)
    ax.annotate("", xy=(v_r[0], v_r[1]), xytext=(v_r[0] + 0.05, v_r[1]), 
                arrowprops=dict(arrowstyle="->", color="#000000", lw=1.3, mutation_scale=12), zorder=2)

    # Row 4 (Right to Left)
    draw_orthogonal_arrow(ax, *get_edge("V", "left"), *get_edge("W", "right"), color="#000000", lw=1.3)
    draw_orthogonal_arrow(ax, *get_edge("W", "left"), *get_edge("X", "right"), color="#000000", lw=1.3)
    draw_orthogonal_arrow(ax, *get_edge("X", "left"), *get_edge("Finish", "right"), color="#000000", lw=1.3)

    plt.tight_layout()
    png_path = os.path.join("diagrams_output", "MERYL_SHOES_CPM_NETWORK_DIAGRAM.png")
    svg_path = os.path.join("diagrams_output", "MERYL_SHOES_CPM_NETWORK_DIAGRAM.svg")
    plt.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig(svg_path, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Clean CPM (Black & White, No Legend/Header text) generated successfully.")


if __name__ == "__main__":
    draw_pert_diagram(bw=False)
    draw_pert_diagram(bw=True)
    draw_cpm_diagram()
