import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import os

# Create scratch output directory
out_dir = os.path.abspath("diagrams_output")
os.makedirs(out_dir, exist_ok=True)

# Complete task data from Meryl Shoes Gantt Chart & PERT-CPM Sheet
tasks_data = {
    "A": {
        "id": "A", "wbs": "1.1", "name": "Requirements Elicitation\n& Stakeholder Interviews",
        "short_name": "Requirements Elicitation\n& Interviews",
        "dur": 14, "es": 0, "ef": 14, "ls": 0, "lf": 14, "slack": 0, "crit": True,
        "row": 1, "col": 1
    },
    "B": {
        "id": "B", "wbs": "1.2", "name": "Process Observation &\nInventory Workflow Audit",
        "short_name": "Process Observation &\nInventory Workflow",
        "dur": 16, "es": 5, "ef": 21, "ls": 5, "lf": 21, "slack": 0, "crit": True,
        "row": 1, "col": 2
    },
    "C": {
        "id": "C", "wbs": "2.1", "name": "UI/UX Wireframing, DFDs\n(0-2) & ERD Modeling",
        "short_name": "UI/UX Wireframes,\nDFDs & ERD Modeling",
        "dur": 16, "es": 15, "ef": 31, "ls": 15, "lf": 31, "slack": 0, "crit": True,
        "row": 1, "col": 3
    },
    "D": {
        "id": "D", "wbs": "2.2", "name": "System Architecture &\nSecurity Design (JWT/Crypt)",
        "short_name": "System Architecture &\nSecurity Design",
        "dur": 16, "es": 21, "ef": 37, "ls": 21, "lf": 37, "slack": 0, "crit": True,
        "row": 1, "col": 4
    },
    "E": {
        "id": "E", "wbs": "2.3", "name": "Predictive Analytics &\nPromotions Design",
        "short_name": "Analytics Modeling &\nPromotions Design",
        "dur": 18, "es": 27, "ef": 45, "ls": 29, "lf": 47, "slack": 2, "crit": False,
        "row": 1, "col": 5, "offset_y": 0.8
    },
    "F": {
        "id": "F", "wbs": "3.1", "name": "Master Catalog & Item\nParameters Design",
        "short_name": "Catalog & Inventory\nParameters Design",
        "dur": 14, "es": 38, "ef": 52, "ls": 38, "lf": 52, "slack": 0, "crit": True,
        "row": 1, "col": 5, "offset_y": -0.8
    },
    "G": {
        "id": "G", "wbs": "3.2", "name": "POS Terminal, Multi-Tender\n& Receipt Design",
        "short_name": "POS Terminal, Tender\n& Receipt Design",
        "dur": 14, "es": 41, "ef": 55, "ls": 41, "lf": 55, "slack": 0, "crit": True,
        "row": 1, "col": 6, "offset_y": -0.8
    },
    "H": {
        "id": "H", "wbs": "3.3", "name": "Replacement Intake &\nHardware Camera QR Design",
        "short_name": "Replacement Intake &\nCamera QR Design",
        "dur": 16, "es": 44, "ef": 60, "ls": 44, "lf": 60, "slack": 0, "crit": True,
        "row": 1, "col": 7, "offset_y": -0.8
    },
    
    # ROW 2 (Right to Left)
    "I": {
        "id": "I", "wbs": "4.1", "name": "Database Setup, RLS &\nCloud Storage Buckets",
        "short_name": "Database Setup, RLS\n& Cloud Storage",
        "dur": 15, "es": 54, "ef": 69, "ls": 54, "lf": 69, "slack": 0, "crit": True,
        "row": 2, "col": 7
    },
    "J": {
        "id": "J", "wbs": "4.2", "name": "Front-End UI Development\n(React, TS, Tailwind)",
        "short_name": "Front-End UI Dev\n(React, TypeScript)",
        "dur": 24, "es": 60, "ef": 84, "ls": 62, "lf": 86, "slack": 2, "crit": False,
        "row": 2, "col": 6, "offset_y": 0.8
    },
    "K": {
        "id": "K", "wbs": "4.3", "name": "Back-End API Services &\nSession Cryptography",
        "short_name": "Back-End APIs &\nSession Cryptography",
        "dur": 24, "es": 64, "ef": 88, "ls": 64, "lf": 88, "slack": 0, "crit": True,
        "row": 2, "col": 6, "offset_y": -0.8
    },
    "L": {
        "id": "L", "wbs": "4.4", "name": "Core POS Checkout &\nThermal Receipt Engine",
        "short_name": "Core POS Checkout &\nThermal Receipt Engine",
        "dur": 22, "es": 71, "ef": 93, "ls": 71, "lf": 93, "slack": 0, "crit": True,
        "row": 2, "col": 5
    },
    "M": {
        "id": "M", "wbs": "4.5", "name": "Predictive Sales Forecast\n& Brevo Marketing Blast",
        "short_name": "Predictive Forecast &\nBrevo Email Blast",
        "dur": 22, "es": 76, "ef": 98, "ls": 76, "lf": 98, "slack": 0, "crit": True,
        "row": 2, "col": 4, "offset_y": 0.8
    },
    "N": {
        "id": "N", "wbs": "4.6", "name": "Replacement Intake &\nHardware Camera Scanner",
        "short_name": "Replacement Intake &\nCamera QR Module",
        "dur": 20, "es": 78, "ef": 98, "ls": 78, "lf": 98, "slack": 0, "crit": True,
        "row": 2, "col": 4, "offset_y": -0.8
    },
    "O": {
        "id": "O", "wbs": "5.1", "name": "Module Unit Testing &\nWhite-Box Test Cases",
        "short_name": "Module Unit Testing\n(White-Box Cases)",
        "dur": 22, "es": 84, "ef": 106, "ls": 86, "lf": 108, "slack": 2, "crit": False,
        "row": 2, "col": 3
    },

    # ROW 3 (Left to Right)
    "P": {
        "id": "P", "wbs": "5.2", "name": "Subsystem & Cross-Tab\nIntegration Testing",
        "short_name": "Subsystem Testing &\nRealtime Sync",
        "dur": 21, "es": 95, "ef": 116, "ls": 95, "lf": 116, "slack": 0, "crit": True,
        "row": 3, "col": 3
    },
    "Q": {
        "id": "Q", "wbs": "5.3", "name": "Functional Black-Box\nAlpha Testing (POS/Inv)",
        "short_name": "Functional Alpha\nBlack-Box Testing",
        "dur": 22, "es": 105, "ef": 127, "ls": 105, "lf": 127, "slack": 0, "crit": True,
        "row": 3, "col": 4, "offset_y": 0.8
    },
    "R": {
        "id": "R", "wbs": "5.4", "name": "Security, Pen-Testing &\nRLS Lockout Validation",
        "short_name": "Security, Pen-Test &\nLockout Validation",
        "dur": 21, "es": 112, "ef": 133, "ls": 113, "lf": 134, "slack": 1, "crit": False,
        "row": 3, "col": 4, "offset_y": -0.8
    },
    "S": {
        "id": "S", "wbs": "5.5", "name": "Full System Stress &\nHardware Concurrency",
        "short_name": "Full System, Stress &\nHardware Testing",
        "dur": 20, "es": 119, "ef": 139, "ls": 119, "lf": 139, "slack": 0, "crit": True,
        "row": 3, "col": 5
    },
    "T": {
        "id": "T", "wbs": "5.6", "name": "Bug Resolution, Retesting\n& System Hardening",
        "short_name": "Bug Resolution &\nSystem Hardening",
        "dur": 19, "es": 128, "ef": 147, "ls": 128, "lf": 147, "slack": 0, "crit": True,
        "row": 3, "col": 6, "offset_y": 0.8
    },
    "U": {
        "id": "U", "wbs": "5.7", "name": "ISO/IEC 25010:2011 Product\nQuality Evaluation",
        "short_name": "ISO/IEC 25010:2011\nSoftware Evaluation",
        "dur": 14, "es": 133, "ef": 147, "ls": 133, "lf": 147, "slack": 0, "crit": True,
        "row": 3, "col": 6, "offset_y": -0.8
    },

    # ROW 4 (Right to Left)
    "V": {
        "id": "V", "wbs": "6.1", "name": "Beta Testing & User\nAcceptance Testing (UAT)",
        "short_name": "Beta Testing & Client\nUAT Walkthroughs",
        "dur": 8, "es": 144, "ef": 152, "ls": 144, "lf": 152, "slack": 0, "crit": True,
        "row": 4, "col": 6
    },
    "W": {
        "id": "W", "wbs": "6.2", "name": "Client Feedback &\nUI Final Polish",
        "short_name": "Client Feedback &\nUI Final Polish",
        "dur": 6, "es": 149, "ef": 155, "ls": 149, "lf": 155, "slack": 0, "crit": True,
        "row": 4, "col": 5
    },
    "X": {
        "id": "X", "wbs": "6.3", "name": "Final Documentation &\nSystem Turnover Closeout",
        "short_name": "Documentation &\nSystem Turnover",
        "dur": 7, "es": 152, "ef": 159, "ls": 152, "lf": 159, "slack": 0, "crit": True,
        "row": 4, "col": 4
    }
}

print(f"Loaded {len(tasks_data)} tasks.")

