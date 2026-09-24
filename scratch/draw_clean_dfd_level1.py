import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

os.makedirs("diagrams_output", exist_ok=True)

def create_dfd_level1_diagram():
    # Setup high-resolution canvas matching the user's uploaded aspect ratio
    fig, ax = plt.subplots(figsize=(19, 21), dpi=300)
    ax.set_xlim(-0.1, 11.6)
    ax.set_ylim(-0.2, 23.0)
    ax.axis("off")

    # Styling constants
    FONT_FAMILY = "sans-serif"
    LINE_COLOR = "#000000"
    TEXT_COLOR = "#000000"
    BOX_BG = "#FFFFFF"
    BORDER_WIDTH = 1.2
    ARROW_WIDTH = 1.0

    def draw_entity(x, y, w, h, text):
        """Draws an External Entity (Rounded Rectangle)"""
        x0, y0 = x - w/2, y - h/2
        box = FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.03,rounding_size=0.14",
                             facecolor=BOX_BG, edgecolor=LINE_COLOR, lw=BORDER_WIDTH, zorder=4)
        ax.add_patch(box)
        ax.text(x, y, text, ha="center", va="center", fontsize=8.5, fontweight="bold",
                fontfamily=FONT_FAMILY, color=TEXT_COLOR, zorder=5)

    def draw_process(x, y, w, h, num_str, title_str):
        """Draws a DFD Process Bubble (Gane-Sarson Rounded Rectangle with header divider)"""
        x0, y0 = x - w/2, y - h/2
        box = FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.03,rounding_size=0.16",
                             facecolor=BOX_BG, edgecolor=LINE_COLOR, lw=BORDER_WIDTH, zorder=4)
        ax.add_patch(box)
        
        # Divider line between ID and Process Title
        h_header = 0.25
        divider_y = y0 + h - h_header
        ax.plot([x0 + 0.03, x0 + w - 0.03], [divider_y, divider_y], color=LINE_COLOR, lw=BORDER_WIDTH, zorder=5)
        
        # Header text (Process Number)
        ax.text(x, divider_y + h_header/2 - 0.01, num_str, ha="center", va="center",
                fontsize=8.5, fontweight="bold", fontfamily=FONT_FAMILY, color=TEXT_COLOR, zorder=6)
        
        # Body text (Process Name)
        body_y = y0 + (h - h_header)/2
        ax.text(x, body_y, title_str, ha="center", va="center",
                fontsize=7.8, fontweight="bold", fontfamily=FONT_FAMILY, color=TEXT_COLOR, zorder=6)

    def draw_datastore(x, y, w, h, id_str, name_str):
        """Draws a DFD Open-Ended Data Store [ D1 | Name ------ ]"""
        x0, y0 = x - w/2, y - h/2
        w_id = 0.44
        
        # Background rectangle to mask lines crossing behind
        bg = patches.Rectangle((x0, y0), w, h, facecolor=BOX_BG, edgecolor="none", zorder=3)
        ax.add_patch(bg)

        # Left vertical line, top line, and bottom line (right side open)
        ax.plot([x0 + w, x0, x0, x0 + w], [y0 + h, y0 + h, y0, y0], color=LINE_COLOR, lw=BORDER_WIDTH, zorder=4)
        # Vertical divider for Store ID
        ax.plot([x0 + w_id, x0 + w_id], [y0, y0 + h], color=LINE_COLOR, lw=BORDER_WIDTH, zorder=4)
        
        # Labels
        ax.text(x0 + w_id/2, y, id_str, ha="center", va="center", fontsize=7.8, fontweight="bold", fontfamily=FONT_FAMILY, zorder=5)
        ax.text(x0 + w_id + (w - w_id)/2, y, name_str, ha="center", va="center", fontsize=8.0, fontweight="bold", fontfamily=FONT_FAMILY, zorder=5)

    def draw_arrow(points, label="", label_pos=None, label_ha="center", label_va="bottom", fontsize=5.8, label_offset=(0, 0.03)):
        """Draws orthogonal connecting lines with arrowhead and text label"""
        arrow_props = dict(arrowstyle="->", color=LINE_COLOR, lw=ARROW_WIDTH, mutation_scale=8, shrinkA=0, shrinkB=0)
        
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        
        # Polyline body
        if len(points) > 2:
            ax.plot(xs[:-1], ys[:-1], color=LINE_COLOR, lw=ARROW_WIDTH, zorder=2)
            
        # Arrowhead segment
        ax.annotate("", xy=points[-1], xytext=points[-2], arrowprops=arrow_props, zorder=2)
        
        # Text label with clean white backing
        if label:
            if label_pos is None:
                lx = (xs[0] + xs[1]) / 2 + label_offset[0]
                ly = (ys[0] + ys[1]) / 2 + label_offset[1]
            else:
                lx, ly = label_pos[0] + label_offset[0], label_pos[1] + label_offset[1]
                
            ax.text(lx, ly, label, ha=label_ha, va=label_va, fontsize=fontsize,
                    fontweight="bold", fontfamily=FONT_FAMILY, color=TEXT_COLOR, zorder=6,
                    bbox=dict(boxstyle="square,pad=0.10", fc="#FFFFFF", ec="none", alpha=0.92))

    # ==========================================================================
    # 1. PLACE NODES
    # ==========================================================================
    PX = 5.3
    PW = 1.95
    PH = 0.82

    # Process locations
    draw_process(PX, 21.6, PW, PH, "1.0", "USER\nMANAGEMENT")
    draw_process(PX, 19.0, PW, PH, "2.0", "INVENTORY\nMANAGEMENT")
    draw_process(PX, 16.0, PW, PH, "3.0", "SALES\nMANAGEMENT")
    draw_process(PX, 12.8, PW, PH, "4.0", "REPLACEMENT\nMANAGEMENT")
    draw_process(PX, 9.5,  PW, PH, "5.0", "SALES\nANALYTICS")
    draw_process(PX, 7.0,  PW, PH, "6.0", "PREDICTIVE\nANALYTICS")
    draw_process(PX, 4.3,  PW, PH, "7.0", "PROMOTION\nMANAGEMENT")
    draw_process(PX, 1.3,  PW, PH, "8.0", "REPORT\nGENERATION")

    # External Entities (Left column)
    draw_entity(1.4, 21.6, 1.45, 0.60, "ADMIN")
    draw_entity(1.4, 19.1, 1.50, 0.60, "INVENTORY STAFF")
    draw_entity(1.0, 16.5, 1.30, 0.56, "CASHIER")
    draw_entity(2.0, 14.6, 1.35, 0.56, "CUSTOMER")
    draw_entity(1.2, 5.5, 1.35, 1.15, "ADMIN")

    # Data Stores (Right column)
    DS_X = 9.0
    DS_W = 1.65
    DS_H = 0.50
    draw_datastore(DS_X, 21.6, DS_W, DS_H, "D1", "Users")
    draw_datastore(DS_X, 19.0, DS_W, DS_H, "D2", "Inventory")
    draw_datastore(8.2,  16.0, DS_W, DS_H, "D3", "Sales")
    draw_datastore(8.5,  12.4, DS_W, DS_H, "D4", "Returns")
    draw_datastore(8.6,  9.5,  DS_W, DS_H, "D5", "Analytics")
    draw_datastore(8.6,  6.8,  DS_W, DS_H, "D6", "Prediction")
    draw_datastore(8.6,  3.7,  DS_W, DS_H, "D7", "Promotion")

    # ==========================================================================
    # 2. CONNECTING DATA FLOW ARROWS
    # ==========================================================================

    # --- ROW 1: USER MANAGEMENT (1.0) ---
    draw_arrow([(2.15, 21.82), (4.3, 21.82)], label="USER ACCOUNT DETAILS AND ROLES", label_pos=(3.2, 21.84))
    draw_arrow([(4.3, 21.58), (2.15, 21.58)], label="PERMISSIONS", label_pos=(3.2, 21.60))
    draw_arrow([(4.3, 21.35), (2.15, 21.35)], label="USER LIST AND ACCOUNT STATUS", label_pos=(3.2, 21.37))
    
    draw_arrow([(6.3, 21.82), (8.15, 21.82)], label="USER CREDENTIALS", label_pos=(7.2, 21.84))
    draw_arrow([(8.15, 21.58), (6.3, 21.58)], label="USER DATA", label_pos=(7.2, 21.60))
    draw_arrow([(6.3, 21.35), (8.15, 21.35)], label="STORED USER DATA\nAND AUTH TOKENS", label_pos=(7.2, 21.30), label_va="top", fontsize=5.5)

    # --- ROW 2: INVENTORY MANAGEMENT (2.0) ---
    draw_arrow([(2.15, 19.30), (4.3, 19.30)], label="PRODUCT SPECIFICATION", label_pos=(3.2, 19.32))
    draw_arrow([(2.15, 18.78), (4.3, 18.78)], label="STOCK-IN AND ADJUSTMENT DETAILS", label_pos=(3.2, 18.80))
    
    # Return confirmation lines into bottom of INVENTORY STAFF
    draw_arrow([(4.3, 18.42), (1.6, 18.42), (1.6, 18.8)], label="PRODUCT REGISTRATION CONFIRMATION", label_pos=(2.7, 18.44))
    draw_arrow([(4.3, 18.15), (1.2, 18.15), (1.2, 18.8)], label="INVENTORY STATUS AND LOW STOCK ALERTS", label_pos=(2.7, 18.17))

    # 2.0 -> D2
    draw_arrow([(5.3, 19.45), (5.3, 20.0), (9.5, 20.0), (9.5, 19.28)], label="INVENTORY MOVEMENT LOG ENTRY", label_pos=(7.4, 20.02))
    draw_arrow([(6.3, 19.30), (8.15, 19.30)], label="PRODUCT MASTER RECORD", label_pos=(7.2, 19.32))
    draw_arrow([(8.15, 19.00), (6.3, 19.00)], label="INVENTORY DATA", label_pos=(7.2, 19.02))
    draw_arrow([(6.3, 18.70), (8.15, 18.70)], label="UPDATED STOCK BALANCE AND SRP", label_pos=(7.2, 18.72), fontsize=5.6)
    draw_arrow([(8.15, 18.40), (5.8, 18.40), (5.8, 18.6)], label="CURRENT STOCK QUANTITY AND THRESHOLD", label_pos=(7.0, 18.42), fontsize=5.6)

    # --- ROW 3: SALES MANAGEMENT (3.0) ---
    draw_arrow([(1.65, 16.65), (4.3, 16.65)], label="SELECTED PRODUCT AND QUANTITY", label_pos=(3.0, 16.67))
    draw_arrow([(1.65, 16.35), (4.3, 16.35)], label="PAYMENT TENDER DETAILS", label_pos=(3.0, 16.37))
    draw_arrow([(4.3, 16.05), (1.65, 16.05)], label="TRANSACTION CONFIRMATION", label_pos=(3.0, 16.07))

    # 3.0 -> D2 (Product info & stock check)
    draw_arrow([(6.3, 16.50), (9.3, 16.50), (9.3, 18.73)], label="PRODUCT INFO / STOCK CHECK", label_pos=(7.7, 16.52), fontsize=5.6)
    draw_arrow([(6.3, 16.20), (9.5, 16.20), (9.5, 18.73)], label="STOCK DEDUCTION", label_pos=(7.7, 16.22), fontsize=5.6)

    # 3.0 <-> D3 (Sales record)
    draw_arrow([(6.3, 15.80), (7.8, 15.80)], label="SALES RECORD", label_pos=(7.0, 15.82))
    draw_arrow([(7.8, 15.55), (6.3, 15.55)], label="SALES RECORD", label_pos=(7.0, 15.57))

    # Customer <-> 3.0
    draw_arrow([(2.7, 14.85), (4.6, 14.85), (4.6, 15.6)], label="PAYMENT INFO", label_pos=(3.6, 14.87))
    draw_arrow([(4.3, 15.35), (2.7, 15.35)], label="RECEIPT", label_pos=(3.5, 15.37))
    draw_arrow([(4.3, 15.10), (2.7, 15.10)], label="PURCHASED PRODUCT", label_pos=(3.5, 15.12))

    # --- ROW 4: REPLACEMENT MANAGEMENT (4.0) ---
    # Cashier down to 4.0
    draw_arrow([(0.65, 16.2), (0.65, 12.8), (4.3, 12.8)], label="")
    
    # Customer -> 4.0
    draw_arrow([(2.7, 14.35), (4.3, 14.35), (4.3, 13.25)], label="RETURN REQUEST", label_pos=(3.5, 14.37))
    draw_arrow([(2.2, 14.3), (2.2, 13.9), (4.3, 13.9), (4.3, 13.25)], label="ITEM", label_pos=(3.2, 13.92))
    draw_arrow([(4.3, 12.55), (1.9, 12.55), (1.9, 14.3)], label="EXCHANGE CONFIRMATION", label_pos=(3.0, 12.57), fontsize=5.5)
    draw_arrow([(2.5, 14.3), (2.5, 12.3), (4.3, 12.3)], label="RETURN DETAILS", label_pos=(3.4, 12.32))
    draw_arrow([(4.3, 12.05), (1.6, 12.05), (1.6, 14.3)], label="RETURN STATUS", label_pos=(2.8, 12.07))

    # 4.0 -> D3 (Transaction reference)
    draw_arrow([(6.3, 13.15), (7.6, 13.15), (7.6, 15.73)], label="TRANSACTION REFERENCE", label_pos=(7.0, 13.17), fontsize=5.5)
    # 4.0 -> D2 (Stock update)
    draw_arrow([(6.3, 12.85), (9.7, 12.85), (9.7, 18.73)], label="STOCK UPDATE", label_pos=(8.0, 12.87), fontsize=5.6)
    # 4.0 -> D4 (Return record)
    draw_arrow([(6.3, 12.4), (7.7, 12.4)], label="RETURN RECORD", label_pos=(7.0, 12.42))

    # --- ROW 5: SALES ANALYTICS (5.0) ---
    draw_arrow([(1.9, 6.0), (1.9, 9.85), (4.3, 9.85)], label="ANALYTICS REQUEST", label_pos=(3.1, 9.87))
    draw_arrow([(4.3, 9.55), (1.6, 9.55), (1.6, 6.1)], label="TOP SELLING PRODUCTS", label_pos=(3.0, 9.57))
    draw_arrow([(4.3, 9.25), (1.3, 9.25), (1.3, 6.1)], label="FAST / SLOW MOVING ITEMS", label_pos=(2.8, 9.27), fontsize=5.6)
    draw_arrow([(4.3, 8.95), (1.0, 8.95), (1.0, 6.1)], label="SALES TREND", label_pos=(2.6, 8.97))
    
    # D3 -> 5.0 (Historical sales data line)
    draw_arrow([(8.2, 15.73), (8.2, 10.1), (6.3, 10.1)], label="")
    # 5.0 -> D5
    draw_arrow([(6.3, 9.5), (7.8, 9.5)], label="PROCESSED ANALYTICS", label_pos=(7.0, 9.52), fontsize=5.5)

    # --- ROW 6: PREDICTIVE ANALYTICS (6.0) ---
    draw_arrow([(1.9, 5.8), (1.9, 7.25), (4.3, 7.25)], label="FORECAST REQUEST", label_pos=(3.1, 7.27))
    draw_arrow([(4.3, 6.95), (1.5, 6.95), (1.5, 5.9)], label="DEMAND PREDICTION", label_pos=(2.9, 6.97))
    # D3 -> 6.0
    draw_arrow([(8.4, 15.73), (8.4, 7.25), (6.3, 7.25)], label="HISTORICAL SALES DATA", label_pos=(7.4, 7.27), fontsize=5.5)
    # 6.0 -> D6
    draw_arrow([(6.3, 6.75), (7.8, 6.75)], label="PREDICTION RESULTS", label_pos=(7.0, 6.77), fontsize=5.5)

    # --- ROW 7: PROMOTION MANAGEMENT (7.0) ---
    draw_arrow([(1.9, 5.2), (1.9, 4.55), (4.3, 4.55)], label="PROMOTION DETAILS", label_pos=(3.1, 4.57))
    draw_arrow([(4.3, 4.25), (1.6, 4.25), (1.6, 5.1)], label="DISCOUNTS", label_pos=(2.9, 4.27))
    draw_arrow([(4.3, 3.95), (1.3, 3.95), (1.3, 5.0)], label="RECOMMENDED PROMOTIONS", label_pos=(2.8, 3.97), fontsize=5.5)
    
    # 7.0 -> D3 (Active discounts going up)
    draw_arrow([(6.3, 4.55), (8.9, 4.55), (8.9, 15.73)], label="ACTIVE DISCOUNTS", label_pos=(7.6, 4.57), fontsize=5.6)
    # 7.0 -> D7
    draw_arrow([(6.3, 4.2), (7.8, 4.2)], label="PROMOTION RECORD", label_pos=(7.0, 4.22), fontsize=5.5)
    # D5 -> 7.0
    draw_arrow([(8.6, 9.23), (8.6, 3.75), (6.3, 3.75)], label="PRODUCT PERFORMANCE DATA", label_pos=(7.5, 3.77), fontsize=5.5)

    # --- ROW 8: REPORT GENERATION (8.0) ---
    draw_arrow([(1.9, 4.9), (1.9, 1.85), (4.3, 1.85)], label="REPORT REQUEST", label_pos=(3.1, 1.87))
    draw_arrow([(4.3, 1.55), (1.6, 1.55), (1.6, 4.9)], label="SALES REPORT", label_pos=(2.9, 1.57))
    draw_arrow([(4.3, 1.25), (1.3, 1.25), (1.3, 4.9)], label="INVENTORY REPORT", label_pos=(2.8, 1.27))
    draw_arrow([(4.3, 0.95), (1.0, 0.95), (1.0, 4.9)], label="ANALYTICS REPORT", label_pos=(2.7, 0.97))
    draw_arrow([(4.3, 0.65), (0.7, 0.65), (0.7, 4.9)], label="FORECAST REPORT", label_pos=(2.6, 0.67))

    # Data stores entering 8.0 on the right
    draw_arrow([(10.0, 18.73), (10.0, 1.7), (6.3, 1.7)], label="INVENTORY DATA", label_pos=(7.7, 1.72), fontsize=5.5)
    draw_arrow([(10.2, 15.73), (10.2, 1.4), (6.3, 1.4)], label="SALES DATA", label_pos=(7.7, 1.42), fontsize=5.5)
    draw_arrow([(9.1, 9.23), (9.1, 1.1), (6.3, 1.1)], label="ANALYTICS DATA", label_pos=(7.7, 1.12), fontsize=5.5)
    draw_arrow([(9.3, 6.53), (9.3, 0.8), (6.3, 0.8)], label="FORECAST DATA", label_pos=(7.7, 0.82), fontsize=5.5)

    plt.tight_layout()
    png_path = os.path.join("diagrams_output", "MERYL_SHOES_DFD_LEVEL_1_UPDATED.png")
    svg_path = os.path.join("diagrams_output", "MERYL_SHOES_DFD_LEVEL_1_UPDATED.svg")
    plt.savefig(png_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig(svg_path, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Clean updated DFD Level 1 generated successfully.")

if __name__ == "__main__":
    create_dfd_level1_diagram()

