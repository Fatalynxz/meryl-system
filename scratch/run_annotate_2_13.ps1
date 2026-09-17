. "$PSScriptRoot\annotate_image.ps1"

$callouts = @(
    @{
        Number = 1
        Text = "1. Displays shoe thumbnail photo, Brand, Model Name, Category, and detailed variant classification (Color, Size, Department)."
        BoxX = 20
        BoxY = 80
        BoxW = 325
        BoxH = 85
        TargetX = 425
        TargetY = 200
    },
    @{
        Number = 2
        Text = "2. Displays the unique SKU barcode reference and complete product title."
        BoxX = 20
        BoxY = 240
        BoxW = 325
        BoxH = 75
        TargetX = 400
        TargetY = 275
    },
    @{
        Number = 3
        Text = "3. Two-column specifications grid itemizing complete variant inventory metrics:`n`n- Stock Distribution: Physical count on warehouse shelves (On Hand: 146 units), reservations (Held: 10 units), and POS sellable units (Available: 136 units).`n- Threshold & Pricing: Minimum safety alert level (Reorder: 10) and retail selling price (Price: PHP 2,100).`n- Condition & Status: Live automated health check (Condition: Good) and sellable status (Status: Active).`n- Batch Tracking Dates: Production date (2026-06-05) and shelf-life expiration date (2029-02-27)."
        BoxX = 660
        BoxY = 140
        BoxW = 345
        BoxH = 290
        TargetX = 635
        TargetY = 320
    }
)

$inputImg = "C:\Users\villa\.gemini\antigravity\brain\f7cf3675-46d8-430f-8f91-96a5e3d7a8a2\.user_uploaded\media_1789627188974.png"
$outputImg = "C:\Users\villa\OneDrive\Desktop\meryl-system-main\Section_2_13_Inventory_Details_Annotated.png"

Add-CalloutAnnotation -InputPath $inputImg -OutputPath $outputImg -Callouts $callouts
