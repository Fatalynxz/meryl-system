import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import datetime

wb = openpyxl.Workbook()

# Setup styles
font_family = "Calibri"

title_font = Font(name=font_family, size=16, bold=True, color="FFFFFF")
subtitle_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
meta_font = Font(name=font_family, size=10, italic=True, color="FFFFFF")
section_header_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
col_header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
data_font = Font(name=font_family, size=10, color="000000")
data_bold_font = Font(name=font_family, size=10, bold=True, color="000000")
critical_font = Font(name=font_family, size=10, bold=True, color="B71C1C")
non_critical_font = Font(name=font_family, size=10, color="1565C0")

# Fills
chmsu_green = PatternFill(start_color="1B5E20", end_color="1B5E20", fill_type="solid") # Dark Forest Green
chmsu_gold = PatternFill(start_color="F57F17", end_color="F57F17", fill_type="solid")  # Deep Amber/Gold
phase_fill = PatternFill(start_color="2E7D32", end_color="2E7D32", fill_type="solid")  # Medium Green
col_header_fill = PatternFill(start_color="263238", end_color="263238", fill_type="solid") # Blue-Gray Dark
month_fill_1 = PatternFill(start_color="37474F", end_color="37474F", fill_type="solid")
month_fill_2 = PatternFill(start_color="455A64", end_color="455A64", fill_type="solid")
week_header_fill = PatternFill(start_color="546E7A", end_color="546E7A", fill_type="solid")

critical_bar_fill = PatternFill(start_color="D32F2F", end_color="D32F2F", fill_type="solid") # Red
float_bar_fill = PatternFill(start_color="1976D2", end_color="1976D2", fill_type="solid")    # Blue
phase_bar_fill = PatternFill(start_color="81C784", end_color="81C784", fill_type="solid")    # Light Green

zebra_fill = PatternFill(start_color="F1F8E9", end_color="F1F8E9", fill_type="solid") # Soft light green tint
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
total_fill = PatternFill(start_color="FFF9C4", end_color="FFF9C4", fill_type="solid") # Soft Yellow

# Borders
thin_border_side = Side(border_style="thin", color="CCCCCC")
thick_bottom_side = Side(border_style="medium", color="1B5E20")
double_bottom_side = Side(border_style="double", color="1B5E20")

border_cell = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
border_header = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thick_bottom_side)
border_total = Border(top=thin_border_side, bottom=double_bottom_side)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

# ==============================================================================
# SHEET 1: GANTT CHART
# ==============================================================================
ws1 = wb.active
ws1.title = "Gantt Chart (Master Schedule)"
ws1.views.sheetView[0].showGridLines = True

# Title Header
ws1.merge_cells("A1:AE1")
ws1["A1"] = "CARLOS HILADO MEMORIAL STATE UNIVERSITY — COLLEGE OF COMPUTER STUDIES"
ws1["A1"].font = title_font
ws1["A1"].fill = chmsu_green
ws1["A1"].alignment = align_center

ws1.merge_cells("A2:AE2")
ws1["A2"] = "CAPSTONE PROJECT GANTT CHART: INTEGRATED POS-DRIVEN INVENTORY WITH DATA ANALYTICS FOR TARGETING SALES MARKETING"
ws1["A2"].font = subtitle_font
ws1["A2"].fill = chmsu_green
ws1["A2"].alignment = align_center

ws1.merge_cells("A3:AE3")
ws1["A3"] = "Timeline: May 5, 2026 to October 10, 2026 (159 Calendar Days / 23 Weeks) | SDLC: V-Model | Directive: Testing Phase has the Highest Work Allocation"
ws1["A3"].font = meta_font
ws1["A3"].fill = chmsu_gold
ws1["A3"].alignment = align_center

# Column Headers at Row 5 & 6
# Static columns: A (ID), B (Task Description), C (Lead), D (Start Date), E (End Date), F (Days), G (Predecessors), H (Critical Path)
static_cols = [
    ("A", "WBS / ID", 10),
    ("B", "Task Description & Activity Milestones", 42),
    ("C", "Lead Role", 18),
    ("D", "Start Date", 12),
    ("E", "End Date", 12),
    ("F", "Days", 8),
    ("G", "Predecessor", 12),
    ("H", "Critical?", 10)
]

for col_letter, header_text, width in static_cols:
    ws1.merge_cells(f"{col_letter}5:{col_letter}6")
    cell = ws1[f"{col_letter}5"]
    cell.value = header_text
    cell.font = col_header_font
    cell.fill = col_header_fill
    cell.alignment = align_center
    cell.border = border_header
    ws1.column_dimensions[col_letter].width = width

# Month definitions for columns I to AE (23 Weeks total)
# May (4 wks: I-L), Jun (4 wks: M-P), Jul (4 wks: Q-T), Aug (4 wks: U-X), Sep (4 wks: Y-AB), Oct (2 wks: AC-AD), AE (Margin/Total)
month_ranges = [
    ("May 2026 (May 5-31)", "I", "L", month_fill_1),
    ("June 2026 (Jun 1-30)", "M", "P", month_fill_2),
    ("July 2026 (Jul 1-31)", "Q", "T", month_fill_1),
    ("August 2026 (Aug 1-31)", "U", "X", month_fill_2),
    ("September 2026 (Sep 1-30)", "Y", "AB", month_fill_1),
    ("October 2026 (Oct 1-10)", "AC", "AD", month_fill_2),
]

for m_title, start_col, end_col, fill in month_ranges:
    ws1.merge_cells(f"{start_col}5:{end_col}5")
    cell = ws1[f"{start_col}5"]
    cell.value = m_title
    cell.font = col_header_font
    cell.fill = fill
    cell.alignment = align_center
    cell.border = border_header

# Week labels in row 6
week_cols = [
    ("I", "W1"), ("J", "W2"), ("K", "W3"), ("L", "W4"),
    ("M", "W1"), ("N", "W2"), ("O", "W3"), ("P", "W4"),
    ("Q", "W1"), ("R", "W2"), ("S", "W3"), ("T", "W4"),
    ("U", "W1"), ("V", "W2"), ("W", "W3"), ("X", "W4"),
    ("Y", "W1"), ("Z", "W2"), ("AA", "W3"), ("AB", "W4"),
    ("AC", "W1"), ("AD", "W2")
]

for col_letter, w_label in week_cols:
    cell = ws1[f"{col_letter}6"]
    cell.value = w_label
    cell.font = Font(name=font_family, size=9, bold=True, color="FFFFFF")
    cell.fill = week_header_fill
    cell.alignment = align_center
    cell.border = border_header
    ws1.column_dimensions[col_letter].width = 4.2

# Legend column
ws1["AE5"].value = "Legend"
ws1["AE5"].font = col_header_font
ws1["AE5"].fill = col_header_fill
ws1["AE5"].alignment = align_center
ws1.merge_cells("AE5:AE6")
ws1.column_dimensions["AE"].width = 12

# Task items data
# (Type: 'PHASE' or 'TASK', ID, Title, Lead, Start, End, Days, Pred, Critical, [active week indices 0..21])
# Week indices:
# May: 0=w1 (5-11), 1=w2 (12-18), 2=w3 (19-25), 3=w4 (26-31)
# Jun: 4=w1 (1-7), 5=w2 (8-14), 6=w3 (15-21), 7=w4 (22-30)
# Jul: 8=w1 (1-7), 9=w2 (8-14), 10=w3 (15-21), 11=w4 (22-31)
# Aug: 12=w1 (1-7), 13=w2 (8-14), 14=w3 (15-21), 15=w4 (22-31)
# Sep: 16=w1 (1-7), 17=w2 (8-14), 18=w3 (15-21), 19=w4 (22-30)
# Oct: 20=w1 (1-7), 21=w2 (8-10)

schedule_data = [
    # PHASE 1
    ("PHASE", "1.0", "PHASE I: PLANNING & REQUIREMENTS ANALYSIS", "Team / Analyst", "2026-05-05", "2026-05-25", 21, "", "YES", [0, 1, 2]),
    ("TASK", "A", "Requirements Elicitation & Stakeholder Interviews", "Team / PM", "2026-05-05", "2026-05-18", 14, "-", "YES", [0, 1]),
    ("TASK", "B", "Process Observation & Inventory Workflow Audit", "System Analyst", "2026-05-10", "2026-05-25", 16, "A (SS+5d)", "YES", [1, 2]),
    
    # PHASE 2
    ("PHASE", "2.0", "PHASE II: SYSTEM & ARCHITECTURAL DESIGN", "System Analyst", "2026-05-20", "2026-06-18", 30, "", "YES", [2, 3, 4, 5, 6]),
    ("TASK", "C", "UI/UX Wireframing, DFDs (Levels 0-2) & ERD Modeling", "System Analyst", "2026-05-20", "2026-06-04", 16, "B", "YES", [2, 3, 4]),
    ("TASK", "D", "System Architecture & Security Design (JWT, pgcrypto)", "System Analyst", "2026-05-26", "2026-06-10", 16, "C", "YES", [3, 4, 5]),
    ("TASK", "E", "Predictive Analytics Ensemble & Promotions Design", "System Analyst", "2026-06-01", "2026-06-18", 18, "D", "NO", [4, 5, 6]),
    
    # PHASE 3
    ("PHASE", "3.0", "PHASE III: DETAILED MODULE SPECIFICATIONS", "System Analyst", "2026-06-12", "2026-07-03", 22, "", "YES", [5, 6, 7, 8]),
    ("TASK", "F", "Master Footwear Catalog & Inventory Parameters Design", "System Analyst", "2026-06-12", "2026-06-25", 14, "D", "YES", [5, 6]),
    ("TASK", "G", "POS Terminal, Multi-Tender & Receipt Design", "System Analyst", "2026-06-15", "2026-06-28", 14, "F", "YES", [6, 7]),
    ("TASK", "H", "Replacement Intake, Camera QR & Audit Trail Design", "System Analyst", "2026-06-18", "2026-07-03", 16, "G", "YES", [6, 7, 8]),
    
    # PHASE 4
    ("PHASE", "4.0", "PHASE IV: CODING & IMPLEMENTATION", "Programmer", "2026-06-28", "2026-08-10", 44, "", "YES", [7, 8, 9, 10, 11, 12, 13]),
    ("TASK", "I", "Database Setup, RLS Policies & Cloud Storage Buckets", "Programmer", "2026-06-28", "2026-07-12", 15, "F, G, H", "YES", [7, 8, 9]),
    ("TASK", "J", "Front-End UI Development (React, TypeScript, Tailwind)", "Programmer", "2026-07-04", "2026-07-27", 24, "I", "NO", [8, 9, 10, 11]),
    ("TASK", "K", "Back-End API Services & Session Cryptography", "Programmer", "2026-07-08", "2026-07-31", 24, "I", "YES", [9, 10, 11]),
    ("TASK", "L", "Core POS Checkout, Barcode & Thermal Receipt Engine", "Programmer", "2026-07-15", "2026-08-05", 22, "J, K", "YES", [10, 11, 12]),
    ("TASK", "M", "Predictive Sales Forecasting & Brevo Marketing Blast", "Programmer", "2026-07-20", "2026-08-10", 22, "L", "YES", [10, 11, 12, 13]),
    ("TASK", "N", "Replacement Intake & Hardware Camera QR Scanner", "Programmer", "2026-07-22", "2026-08-10", 20, "L", "YES", [11, 12, 13]),
    
    # PHASE 5: HIGHEST TIME OF WORK
    ("PHASE", "5.0", "PHASE V: TESTING & QUALITY ASSURANCE (HIGHEST DURATION)", "Quality Assurance", "2026-07-28", "2026-09-28", 63, "", "YES", [11, 12, 13, 14, 15, 16, 17, 18, 19]),
    ("TASK", "O", "Module Unit Testing & Bug Fixes (White-Box Test Cases)", "QA / Programmer", "2026-07-28", "2026-08-18", 22, "J, K", "NO", [11, 12, 13, 14]),
    ("TASK", "P", "Subsystem & Integration Testing (Realtime Sync & Broadcast)", "Quality Assurance", "2026-08-08", "2026-08-28", 21, "M, N, O", "YES", [13, 14, 15]),
    ("TASK", "Q", "Functional Black-Box Testing (Alpha POS, Inventory, Returns)", "Quality Assurance", "2026-08-18", "2026-09-08", 22, "P", "YES", [14, 15, 16, 17]),
    ("TASK", "R", "Security, Penetration & Vulnerability Testing (Lockout, RLS)", "Quality Assurance", "2026-08-25", "2026-09-14", 21, "P", "NO", [15, 16, 17, 18]),
    ("TASK", "S", "Full System, Performance & Hardware Stress Testing", "Quality Assurance", "2026-09-01", "2026-09-20", 20, "Q, R", "YES", [16, 17, 18]),
    ("TASK", "T", "Bug Resolution, Retesting & System Hardening", "Programmer / QA", "2026-09-10", "2026-09-28", 19, "S", "YES", [17, 18, 19]),
    ("TASK", "U", "ISO/IEC 25010:2011 Software Evaluation (Experts & Users)", "Team / QA", "2026-09-15", "2026-09-28", 14, "S", "YES", [18, 19]),
    
    # PHASE 6
    ("PHASE", "6.0", "PHASE VI: USER ACCEPTANCE, DEPLOYMENT & TURNOVER", "Team / PM", "2026-09-26", "2026-10-10", 15, "", "YES", [19, 20, 21]),
    ("TASK", "V", "Beta Testing & User Acceptance Testing (UAT with Client)", "Team / PM", "2026-09-26", "2026-10-03", 8, "T, U", "YES", [19, 20]),
    ("TASK", "W", "Client Feedback Integration & UI Final Polish", "Programmer", "2026-10-01", "2026-10-06", 6, "V", "YES", [20, 21]),
    ("TASK", "X", "Final Documentation, User Manual & Project Turnover", "Team", "2026-10-04", "2026-10-10", 7, "W", "YES", [20, 21])
]

current_row = 7
for item in schedule_data:
    item_type, tid, title, lead, start, end, days, pred, crit, active_wks = item
    
    ws1.cell(row=current_row, column=1, value=tid).border = border_cell
    ws1.cell(row=current_row, column=2, value=title).border = border_cell
    ws1.cell(row=current_row, column=3, value=lead).border = border_cell
    ws1.cell(row=current_row, column=4, value=start).border = border_cell
    ws1.cell(row=current_row, column=5, value=end).border = border_cell
    ws1.cell(row=current_row, column=6, value=days).border = border_cell
    ws1.cell(row=current_row, column=7, value=pred).border = border_cell
    ws1.cell(row=current_row, column=8, value=crit).border = border_cell
    
    # Formatting
    ws1.cell(row=current_row, column=1).alignment = align_center
    ws1.cell(row=current_row, column=2).alignment = align_left
    ws1.cell(row=current_row, column=3).alignment = align_left
    ws1.cell(row=current_row, column=4).alignment = align_center
    ws1.cell(row=current_row, column=5).alignment = align_center
    ws1.cell(row=current_row, column=6).alignment = align_center
    ws1.cell(row=current_row, column=7).alignment = align_center
    ws1.cell(row=current_row, column=8).alignment = align_center
    
    if item_type == "PHASE":
        for c in range(1, 9):
            ws1.cell(row=current_row, column=c).font = section_header_font
            ws1.cell(row=current_row, column=c).fill = phase_fill
    else:
        is_zebra = (current_row % 2 == 0)
        row_fill = zebra_fill if is_zebra else white_fill
        for c in range(1, 9):
            ws1.cell(row=current_row, column=c).font = data_bold_font if c in [1, 2, 8] else data_font
            ws1.cell(row=current_row, column=c).fill = row_fill
        if crit == "YES":
            ws1.cell(row=current_row, column=8).font = critical_font
        else:
            ws1.cell(row=current_row, column=8).font = non_critical_font

    # Bar fills for columns I to AD (indices 0 to 21)
    for w_idx in range(22):
        col_idx = 9 + w_idx
        cell = ws1.cell(row=current_row, column=col_idx)
        cell.border = border_cell
        if w_idx in active_wks:
            if item_type == "PHASE":
                cell.fill = phase_bar_fill
            elif crit == "YES":
                cell.fill = critical_bar_fill
            else:
                cell.fill = float_bar_fill
        else:
            cell.fill = white_fill
            
    # Legend tag in col AE
    leg_cell = ws1.cell(row=current_row, column=31)
    leg_cell.border = border_cell
    leg_cell.alignment = align_center
    if item_type == "PHASE":
        leg_cell.value = "PHASE"
        leg_cell.font = Font(name=font_family, size=9, bold=True, color="1B5E20")
    elif crit == "YES":
        leg_cell.value = "CRITICAL"
        leg_cell.font = Font(name=font_family, size=9, bold=True, color="B71C1C")
    else:
        leg_cell.value = "FLOAT"
        leg_cell.font = Font(name=font_family, size=9, bold=True, color="1565C0")

    current_row += 1

# Total Project Row
ws1.merge_cells(f"A{current_row}:E{current_row}")
tot_cell = ws1[f"A{current_row}"]
tot_cell.value = "TOTAL PROJECT DURATION (MAY 5 TO OCTOBER 10, 2026)"
tot_cell.font = Font(name=font_family, size=11, bold=True, color="1B5E20")
tot_cell.alignment = align_right

ws1.cell(row=current_row, column=6, value="159 Days").font = Font(name=font_family, size=11, bold=True, color="1B5E20")
ws1.cell(row=current_row, column=6).alignment = align_center

for c in range(1, 32):
    ws1.cell(row=current_row, column=c).fill = total_fill
    ws1.cell(row=current_row, column=c).border = border_total

# Legend explanation below
leg_start = current_row + 2
ws1.cell(row=leg_start, column=2, value="GANTT CHART COLOR LEGEND:").font = Font(name=font_family, size=10, bold=True)
ws1.cell(row=leg_start+1, column=2, value="■ Red Bars = Critical Path Activities (Zero Float - Direct Impact on Project Delivery)").font = Font(name=font_family, size=10, bold=True, color="D32F2F")
ws1.cell(row=leg_start+2, column=2, value="■ Blue Bars = Non-Critical / Flexible Float Activities").font = Font(name=font_family, size=10, bold=True, color="1976D2")
ws1.cell(row=leg_start+3, column=2, value="■ Dark Green = SDLC Phase Summary Bars").font = Font(name=font_family, size=10, bold=True, color="2E7D32")
ws1.cell(row=leg_start+4, column=2, value="★ HIGHEST WORK ALLOCATION: Phase 5 Testing & Quality Assurance spans 63 calendar days (39.6% of project).").font = Font(name=font_family, size=10, bold=True, color="1B5E20")

# Freeze panes
ws1.freeze_panes = "I7"


# ==============================================================================
# SHEET 2: PERT - CPM ANALYSIS
# ==============================================================================
ws2 = wb.create_sheet(title="PERT-CPM (Critical Path)")
ws2.views.sheetView[0].showGridLines = True

# Title Header
ws2.merge_cells("A1:K1")
ws2["A1"] = "CARLOS HILADO MEMORIAL STATE UNIVERSITY — COLLEGE OF COMPUTER STUDIES"
ws2["A1"].font = title_font
ws2["A1"].fill = chmsu_green
ws2["A1"].alignment = align_center

ws2.merge_cells("A2:K2")
ws2["A2"] = "APPENDIX I: PROGRAM EVALUATION REVIEW TECHNIQUE - CRITICAL PATH METHOD (PERT-CPM)"
ws2["A2"].font = subtitle_font
ws2["A2"].fill = chmsu_green
ws2["A2"].alignment = align_center

ws2.merge_cells("A3:K3")
ws2["A3"] = "Meryl Shoes Enterprise System | Critical Path: A → B → C → D → F → G → H → I → K → L → M/N → P → Q → S → T/U → V → W → X (159 Days)"
ws2["A3"].font = meta_font
ws2["A3"].fill = chmsu_gold
ws2["A3"].alignment = align_center

pert_headers = [
    ("A", "Activity ID", 11),
    ("B", "Task / Milestone Name", 42),
    ("C", "Lead Role", 18),
    ("D", "Predecessors", 14),
    ("E", "Duration (D)", 13),
    ("F", "Early Start (ES)", 14),
    ("G", "Early Finish (EF)", 14),
    ("H", "Late Start (LS)", 14),
    ("I", "Late Finish (LF)", 14),
    ("J", "Slack / Float (S)", 14),
    ("K", "Critical Path?", 14)
]

for col_letter, h_text, width in pert_headers:
    cell = ws2[f"{col_letter}5"]
    cell.value = h_text
    cell.font = col_header_font
    cell.fill = col_header_fill
    cell.alignment = align_center
    cell.border = border_header
    ws2.column_dimensions[col_letter].width = width

pert_data = [
    ("A", "Requirements Elicitation & Interviews", "Team / PM", "None", 14, "Day 0 (May 05)", "Day 14 (May 18)", "Day 0 (May 05)", "Day 14 (May 18)", 0, "CRITICAL"),
    ("B", "Process Observation & Inventory Workflow", "System Analyst", "A (SS+5d)", 16, "Day 5 (May 10)", "Day 21 (May 25)", "Day 5 (May 10)", "Day 21 (May 25)", 0, "CRITICAL"),
    ("C", "UI/UX Wireframes, DFD (0-2) & ERD", "System Analyst", "B", 16, "Day 15 (May 20)", "Day 31 (Jun 04)", "Day 15 (May 20)", "Day 31 (Jun 04)", 0, "CRITICAL"),
    ("D", "System Architecture & Security Design", "System Analyst", "C", 16, "Day 21 (May 26)", "Day 37 (Jun 10)", "Day 21 (May 26)", "Day 37 (Jun 10)", 0, "CRITICAL"),
    ("E", "Analytics Modeling & Promotions Design", "System Analyst", "D", 18, "Day 27 (Jun 01)", "Day 45 (Jun 18)", "Day 29 (Jun 03)", "Day 47 (Jun 20)", 2, "FLOAT"),
    ("F", "Catalog & Inventory Parameters Design", "System Analyst", "D", 14, "Day 38 (Jun 12)", "Day 52 (Jun 25)", "Day 38 (Jun 12)", "Day 52 (Jun 25)", 0, "CRITICAL"),
    ("G", "POS Terminal, Multi-Tender & Receipt Design", "System Analyst", "F", 14, "Day 41 (Jun 15)", "Day 55 (Jun 28)", "Day 41 (Jun 15)", "Day 55 (Jun 28)", 0, "CRITICAL"),
    ("H", "Replacement Intake & Camera QR Design", "System Analyst", "G", 16, "Day 44 (Jun 18)", "Day 60 (Jul 03)", "Day 44 (Jun 18)", "Day 60 (Jul 03)", 0, "CRITICAL"),
    ("I", "DB Setup, RLS Policies & Cloud Buckets", "Programmer", "F, G, H", 15, "Day 54 (Jun 28)", "Day 69 (Jul 12)", "Day 54 (Jun 28)", "Day 69 (Jul 12)", 0, "CRITICAL"),
    ("J", "Front-End UI Development (React/TS)", "Programmer", "I", 24, "Day 60 (Jul 04)", "Day 84 (Jul 27)", "Day 62 (Jul 06)", "Day 86 (Jul 29)", 2, "FLOAT"),
    ("K", "Back-End APIs & Session Cryptography", "Programmer", "I", 24, "Day 64 (Jul 08)", "Day 88 (Jul 31)", "Day 64 (Jul 08)", "Day 88 (Jul 31)", 0, "CRITICAL"),
    ("L", "Core POS Checkout & Thermal Receipt Engine", "Programmer", "J, K", 22, "Day 71 (Jul 15)", "Day 93 (Aug 05)", "Day 71 (Jul 15)", "Day 93 (Aug 05)", 0, "CRITICAL"),
    ("M", "Predictive Analytics & Brevo Email Blast", "Programmer", "L", 22, "Day 76 (Jul 20)", "Day 98 (Aug 10)", "Day 76 (Jul 20)", "Day 98 (Aug 10)", 0, "CRITICAL"),
    ("N", "Replacement Intake & Camera QR Module", "Programmer", "L", 20, "Day 78 (Jul 22)", "Day 98 (Aug 10)", "Day 78 (Jul 22)", "Day 98 (Aug 10)", 0, "CRITICAL"),
    ("O", "Module Unit Testing (White-Box Test Cases)", "QA / Dev", "J, K", 22, "Day 84 (Jul 28)", "Day 106 (Aug 18)", "Day 86 (Jul 30)", "Day 108 (Aug 20)", 2, "FLOAT"),
    ("P", "Integration Testing & Realtime Sync", "Quality Assurance", "M, N, O", 21, "Day 95 (Aug 08)", "Day 116 (Aug 28)", "Day 95 (Aug 08)", "Day 116 (Aug 28)", 0, "CRITICAL"),
    ("Q", "Functional Black-Box Alpha Testing", "Quality Assurance", "P", 22, "Day 105 (Aug 18)", "Day 127 (Sep 08)", "Day 105 (Aug 18)", "Day 127 (Sep 08)", 0, "CRITICAL"),
    ("R", "Security, Penetration & Vulnerability Tests", "Quality Assurance", "P", 21, "Day 112 (Aug 25)", "Day 133 (Sep 14)", "Day 113 (Aug 26)", "Day 134 (Sep 15)", 1, "FLOAT"),
    ("S", "Full System & Stress/Hardware Tests", "Quality Assurance", "Q, R", 20, "Day 119 (Sep 01)", "Day 139 (Sep 20)", "Day 119 (Sep 01)", "Day 139 (Sep 20)", 0, "CRITICAL"),
    ("T", "Bug Resolution & System Hardening", "Programmer / QA", "S", 19, "Day 128 (Sep 10)", "Day 147 (Sep 28)", "Day 128 (Sep 10)", "Day 147 (Sep 28)", 0, "CRITICAL"),
    ("U", "ISO/IEC 25010:2011 Software Evaluation", "Team / QA", "S", 14, "Day 133 (Sep 15)", "Day 147 (Sep 28)", "Day 133 (Sep 15)", "Day 147 (Sep 28)", 0, "CRITICAL"),
    ("V", "User Acceptance Testing (UAT with Client)", "Team / PM", "T, U", 8, "Day 144 (Sep 26)", "Day 152 (Oct 03)", "Day 144 (Sep 26)", "Day 152 (Oct 03)", 0, "CRITICAL"),
    ("W", "User Feedback Integration & UI Polish", "Programmer", "V", 6, "Day 149 (Oct 01)", "Day 155 (Oct 06)", "Day 149 (Oct 01)", "Day 155 (Oct 06)", 0, "CRITICAL"),
    ("X", "Final Documentation & System Turnover", "Team", "W", 7, "Day 152 (Oct 04)", "Day 159 (Oct 10)", "Day 152 (Oct 04)", "Day 159 (Oct 10)", 0, "CRITICAL")
]

p_row = 6
for item in pert_data:
    aid, aname, lead, pred, dur, es, ef, ls, lf, slack, crit = item
    ws2.cell(row=p_row, column=1, value=aid).alignment = align_center
    ws2.cell(row=p_row, column=2, value=aname).alignment = align_left
    ws2.cell(row=p_row, column=3, value=lead).alignment = align_left
    ws2.cell(row=p_row, column=4, value=pred).alignment = align_center
    ws2.cell(row=p_row, column=5, value=dur).alignment = align_center
    ws2.cell(row=p_row, column=6, value=es).alignment = align_center
    ws2.cell(row=p_row, column=7, value=ef).alignment = align_center
    ws2.cell(row=p_row, column=8, value=ls).alignment = align_center
    ws2.cell(row=p_row, column=9, value=lf).alignment = align_center
    ws2.cell(row=p_row, column=10, value=slack).alignment = align_center
    ws2.cell(row=p_row, column=11, value=crit).alignment = align_center
    
    is_zebra = (p_row % 2 == 0)
    row_fill = zebra_fill if is_zebra else white_fill
    for c in range(1, 12):
        ws2.cell(row=p_row, column=c).border = border_cell
        ws2.cell(row=p_row, column=c).fill = row_fill
        ws2.cell(row=p_row, column=c).font = data_bold_font if c in [1, 5, 10, 11] else data_font
        
    if crit == "CRITICAL":
        ws2.cell(row=p_row, column=11).font = critical_font
    else:
        ws2.cell(row=p_row, column=11).font = non_critical_font
        
    p_row += 1

# PERT Total Row
ws2.merge_cells(f"A{p_row}:D{p_row}")
ws2[f"A{p_row}"] = "TOTAL CRITICAL PATH DURATION"
ws2[f"A{p_row}"].font = Font(name=font_family, size=11, bold=True, color="1B5E20")
ws2[f"A{p_row}"].alignment = align_right

ws2.cell(row=p_row, column=5, value="159 Days").font = Font(name=font_family, size=11, bold=True, color="1B5E20")
ws2.cell(row=p_row, column=5).alignment = align_center

ws2.merge_cells(f"F{p_row}:K{p_row}")
ws2[f"F{p_row}"] = "Zero Float (S = 0) Chain Controls Project Turnover Date (October 10, 2026)"
ws2[f"F{p_row}"].font = Font(name=font_family, size=10, italic=True, color="1B5E20")
ws2[f"F{p_row}"].alignment = align_center

for c in range(1, 12):
    ws2.cell(row=p_row, column=c).fill = total_fill
    ws2.cell(row=p_row, column=c).border = border_total


# ==============================================================================
# SHEET 3: PHASE ALLOCATION & TESTING VERIFICATION
# ==============================================================================
ws3 = wb.create_sheet(title="Phase Allocation & Testing Time")
ws3.views.sheetView[0].showGridLines = True

# Title Header
ws3.merge_cells("A1:G1")
ws3["A1"] = "CARLOS HILADO MEMORIAL STATE UNIVERSITY — COLLEGE OF COMPUTER STUDIES"
ws3["A1"].font = title_font
ws3["A1"].fill = chmsu_green
ws3["A1"].alignment = align_center

ws3.merge_cells("A2:G2")
ws3["A2"] = "SDLC PHASE ALLOCATION ANALYSIS & PROFESSOR'S DIRECTIVE VERIFICATION"
ws3["A2"].font = subtitle_font
ws3["A2"].fill = chmsu_green
ws3["A2"].alignment = align_center

ws3.merge_cells("A3:G3")
ws3["A3"] = "Verification that the Testing & Quality Assurance Phase has the HIGHEST Duration and Work Effort"
ws3["A3"].font = meta_font
ws3["A3"].fill = chmsu_gold
ws3["A3"].alignment = align_center

audit_headers = [
    ("A", "SDLC Phase", 12),
    ("B", "Phase Description", 38),
    ("C", "Calendar Date Range", 26),
    ("D", "Elapsed Days", 14),
    ("E", "Cumulative Task-Days", 20),
    ("F", "% of Calendar Span", 18),
    ("G", "Work Allocation Rank", 20)
]

for col_letter, h_text, width in audit_headers:
    cell = ws3[f"{col_letter}5"]
    cell.value = h_text
    cell.font = col_header_font
    cell.fill = col_header_fill
    cell.alignment = align_center
    cell.border = border_header
    ws3.column_dimensions[col_letter].width = width

phase_summary_data = [
    ("Phase 1", "Planning & Requirements Elicitation", "May 05, 2026 – May 25, 2026", 21, 30, "13.2%", "Rank 5"),
    ("Phase 2", "System & Architectural Design", "May 20, 2026 – June 18, 2026", 30, 50, "18.9%", "Rank 3"),
    ("Phase 3", "Module Detailed Specifications", "June 12, 2026 – July 03, 2026", 22, 44, "13.8%", "Rank 4"),
    ("Phase 4", "Coding & System Implementation", "June 28, 2026 – August 10, 2026", 44, 127, "27.7%", "Rank 2"),
    ("Phase 5", "Testing & Quality Assurance", "July 28, 2026 – September 28, 2026", 63, 139, "39.6%", "RANK 1 (HIGHEST WORK)"),
    ("Phase 6", "Acceptance, Deployment & Closeout", "September 26, 2026 – October 10, 2026", 15, 21, "9.4%", "Rank 6")
]

a_row = 6
for item in phase_summary_data:
    pid, pdesc, prange, edays, tdays, pcent, rank = item
    ws3.cell(row=a_row, column=1, value=pid).alignment = align_center
    ws3.cell(row=a_row, column=2, value=pdesc).alignment = align_left
    ws3.cell(row=a_row, column=3, value=prange).alignment = align_center
    ws3.cell(row=a_row, column=4, value=edays).alignment = align_center
    ws3.cell(row=a_row, column=5, value=tdays).alignment = align_center
    ws3.cell(row=a_row, column=6, value=pcent).alignment = align_center
    ws3.cell(row=a_row, column=7, value=rank).alignment = align_center
    
    is_testing = (pid == "Phase 5")
    row_fill = PatternFill(start_color="FFCDD2", end_color="FFCDD2", fill_type="solid") if is_testing else white_fill
    
    for c in range(1, 8):
        cell = ws3.cell(row=a_row, column=c)
        cell.border = border_cell
        cell.fill = row_fill
        if is_testing:
            cell.font = Font(name=font_family, size=10, bold=True, color="B71C1C")
        else:
            cell.font = data_bold_font if c in [1, 4, 7] else data_font
            
    a_row += 1

# Total Row
ws3.merge_cells(f"A{a_row}:C{a_row}")
ws3[f"A{a_row}"] = "TOTAL ENTIRE PROJECT LIFECYCLE"
ws3[f"A{a_row}"].font = Font(name=font_family, size=11, bold=True, color="1B5E20")
ws3[f"A{a_row}"].alignment = align_right

ws3.cell(row=a_row, column=4, value="159 Days").font = Font(name=font_family, size=11, bold=True, color="1B5E20")
ws3.cell(row=a_row, column=4).alignment = align_center

ws3.cell(row=a_row, column=5, value="411 Task-Days").font = Font(name=font_family, size=11, bold=True, color="1B5E20")
ws3.cell(row=a_row, column=5).alignment = align_center

ws3.cell(row=a_row, column=6, value="100.0%").font = Font(name=font_family, size=11, bold=True, color="1B5E20")
ws3.cell(row=a_row, column=6).alignment = align_center

ws3.cell(row=a_row, column=7, value="23 Calendar Weeks").font = Font(name=font_family, size=11, bold=True, color="1B5E20")
ws3.cell(row=a_row, column=7).alignment = align_center

for c in range(1, 8):
    ws3.cell(row=a_row, column=c).fill = total_fill
    ws3.cell(row=a_row, column=c).border = border_total

# Testing breakdown details table below
t_detail_start = a_row + 3
ws3.merge_cells(f"A{t_detail_start}:G{t_detail_start}")
ws3[f"A{t_detail_start}"] = "DETAILED BREAKDOWN OF TESTING & QUALITY ASSURANCE ACTIVITIES (PHASE 5)"
ws3[f"A{t_detail_start}"].font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
ws3[f"A{t_detail_start}"].fill = chmsu_green
ws3[f"A{t_detail_start}"].alignment = align_center

t_sub_headers = [
    ("A", "Test ID", 10),
    ("B", "Testing Activity & Scope", 38),
    ("C", "Testing Method / Tool", 24),
    ("D", "Start Date", 14),
    ("E", "End Date", 14),
    ("F", "Days", 10),
    ("G", "Evaluators / Lead", 20)
]

for col_letter, h_text, width in t_sub_headers:
    cell = ws3[f"{col_letter}{t_detail_start+1}"]
    cell.value = h_text
    cell.font = col_header_font
    cell.fill = col_header_fill
    cell.alignment = align_center
    cell.border = border_header

testing_items = [
    ("Task O", "Module-Based Unit Testing & Cryptography Validation", "White-Box / Pest PHP & pytest", "2026-07-28", "2026-08-18", 22, "QA / Programmer"),
    ("Task P", "Subsystem & Cross-Tab Integration Testing", "BroadcastChannel & Supabase Realtime", "2026-08-08", "2026-08-28", 21, "Quality Assurance"),
    ("Task Q", "Functional Black-Box Alpha Testing (POS, Sizing, Returns)", "Cypress / Black-Box Test Cases", "2026-08-18", "2026-09-08", 22, "Quality Assurance"),
    ("Task R", "Security, Brute-Force & Vulnerability Testing", "Penetration Testing / RLS Check", "2026-08-25", "2026-09-14", 21, "Quality Assurance"),
    ("Task S", "Full System, Performance & Hardware Stress Testing", "Concurrency & Hardware Scanners", "2026-09-01", "2026-09-20", 20, "Quality Assurance"),
    ("Task T", "Bug Resolution, Retesting & System Hardening", "Regression Test Cycles", "2026-09-10", "2026-09-28", 19, "Programmer / QA"),
    ("Task U", "ISO/IEC 25010:2011 Software Product Quality Evaluation", "5-Point Likert Questionnaire", "2026-09-15", "2026-09-28", 14, "5 IT Experts + 20 Users")
]

sub_r = t_detail_start + 2
for tid, tscope, ttool, tstart, tend, tdays, teval in testing_items:
    ws3.cell(row=sub_r, column=1, value=tid).alignment = align_center
    ws3.cell(row=sub_r, column=2, value=tscope).alignment = align_left
    ws3.cell(row=sub_r, column=3, value=ttool).alignment = align_left
    ws3.cell(row=sub_r, column=4, value=tstart).alignment = align_center
    ws3.cell(row=sub_r, column=5, value=tend).alignment = align_center
    ws3.cell(row=sub_r, column=6, value=tdays).alignment = align_center
    ws3.cell(row=sub_r, column=7, value=teval).alignment = align_left
    
    is_z = (sub_r % 2 == 0)
    for c in range(1, 8):
        cell = ws3.cell(row=sub_r, column=c)
        cell.border = border_cell
        cell.fill = zebra_fill if is_z else white_fill
        cell.font = data_bold_font if c in [1, 6] else data_font
    sub_r += 1

# Output file path
output_path = r"c:\Users\villa\OneDrive\Desktop\meryl-system-main\MERYL_SHOES_GANTT_CHART_AND_PERT_CPM.xlsx"
wb.save(output_path)
print(f"Workbook successfully saved to: {output_path}")

