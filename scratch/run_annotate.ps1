. "$PSScriptRoot\annotate_image.ps1"

$callouts = @(
    @{ Number=1; Text="1. Real-time search input (Search by SKU, product, brand, category, or variant...) that immediately filters table rows as characters are typed."; BoxX=15; BoxY=30; BoxW=145; BoxH=80; TargetX=220; TargetY=145 },
    @{ Number=2; Text="2. Header banner showing the yellow Warehouse icon, Sellable Inventory title, and a golden pill displaying total active inventory records (e.g., 8 records)."; BoxX=740; BoxY=15; BoxW=160; BoxH=75; TargetX=935; TargetY=115 },
    @{ Number=3; Text="3. Quick classification selector (All Categories) located in the upper-right corner of the inventory card."; BoxX=720; BoxY=230; BoxW=150; BoxH=65; TargetX=860; TargetY=150 },
    @{ Number=4; Text="4. Horizontal row of filter pills showing live quantities per footwear category"; BoxX=15; BoxY=195; BoxW=150; BoxH=55; TargetX=200; TargetY=175 },
    @{ Number=5; Text="5. High-contrast data table displaying seven core columns"; BoxX=200; BoxY=220; BoxW=160; BoxH=75; TargetX=200; TargetY=220 },
    @{ Number=6; Text="6. Use the Eye icon to view detailed inventory audits, and the Gear icon to configure product settings."; BoxX=850; BoxY=310; BoxW=160; BoxH=65; TargetX=920; TargetY=260 }
)

$inputImg = "C:\Users\villa\.gemini\antigravity\brain\f7cf3675-46d8-430f-8f91-96a5e3d7a8a2\.user_uploaded\media_1789573979183.png"
$outputImg = "C:\Users\villa\OneDrive\Desktop\meryl-system-main\Section_2_12_Sellable_Inventory_Annotated.png"

Add-CalloutAnnotation -InputPath $inputImg -OutputPath $outputImg -Callouts $callouts

