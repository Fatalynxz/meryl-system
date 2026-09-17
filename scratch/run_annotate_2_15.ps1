. "$PSScriptRoot\annotate_image.ps1"

$callouts = @(
    @{
        Number = 1
        Text = "1. Summary KPI cards tracking overall inventory flow: Stock In (total received pairs), Stock Out (sales & deductions), and Net Movement."
        BoxX = 15
        BoxY = 18
        BoxW = 260
        BoxH = 75
        TargetX = 230
        TargetY = 120
    },
    @{
        Number = 2
        Text = "2. Real-time search field filtering logs by shoe model, brand, SKU, movement type, or transaction reference."
        BoxX = 15
        BoxY = 145
        BoxW = 205
        BoxH = 80
        TargetX = 260
        TargetY = 240
    },
    @{
        Number = 3
        Text = "3. Filter logs by movement category (Sales, Restocks, Holds, Adjustments) and click Refresh to pull live updates."
        BoxX = 740
        BoxY = 145
        BoxW = 270
        BoxH = 65
        TargetX = 890
        TargetY = 235
    },
    @{
        Number = 4
        Text = "4. Chronological audit ledger recording timestamp, shoe model, EU size, colorway, and SKU barcode for each stock event."
        BoxX = 15
        BoxY = 280
        BoxW = 205
        BoxH = 95
        TargetX = 350
        TargetY = 320
    },
    @{
        Number = 5
        Text = "5. Color-coded classification pills (Restock, Sale, Reserved/Hold, Adjustment) with signed inventory deltas (+50, -1)."
        BoxX = 490
        BoxY = 478
        BoxW = 260
        BoxH = 75
        TargetX = 615
        TargetY = 380
    },
    @{
        Number = 6
        Text = "6. System transaction UUID or delivery reference linking the stock movement directly to sales receipts or restocks."
        BoxX = 770
        BoxY = 478
        BoxW = 240
        BoxH = 75
        TargetX = 875
        TargetY = 380
    }
)

$inputImg = "C:\Users\villa\.gemini\antigravity\brain\f7cf3675-46d8-430f-8f91-96a5e3d7a8a2\.user_uploaded\media_1789628169838.png"
$outputImg = "C:\Users\villa\OneDrive\Desktop\meryl-system-main\Section_2_15_Inventory_Movement_Log_Annotated.png"

Add-CalloutAnnotation -InputPath $inputImg -OutputPath $outputImg -Callouts $callouts
Copy-Item $outputImg "C:\Users\villa\.gemini\antigravity\brain\f7cf3675-46d8-430f-8f91-96a5e3d7a8a2\Section_2_15_Inventory_Movement_Log_Annotated.png" -Force
