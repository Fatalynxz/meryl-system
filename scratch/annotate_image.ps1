Add-Type -AssemblyName System.Drawing

function Add-CalloutAnnotation {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [array]$Callouts, 
        [int]$TargetWidth = 1024,
        [int]$TargetHeight = 576
    )

    $src = [System.Drawing.Image]::FromFile($InputPath)
    $bmp = [System.Drawing.Bitmap]::new($TargetWidth, $TargetHeight)
    $g = [System.Drawing.Graphics]::FromImage($bmp)

    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic

    # Draw dark background
    $bgBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(15, 15, 20))
    $g.FillRectangle($bgBrush, 0, 0, $TargetWidth, $TargetHeight)
    $bgBrush.Dispose()

    # Center source image
    $scale = [Math]::Min($TargetWidth / $src.Width, $TargetHeight / $src.Height)
    $drawW = [int]($src.Width * $scale)
    $drawH = [int]($src.Height * $scale)
    $offsetX = [int](($TargetWidth - $drawW) / 2)
    $offsetY = [int](($TargetHeight - $drawH) / 2)

    $g.DrawImage($src, $offsetX, $offsetY, $drawW, $drawH)
    $src.Dispose()

    # Pens and Brushes
    $boxBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
    $boxPen = [System.Drawing.Pen]::new([System.Drawing.Color]::Black, 1.5)
    $textBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::Black)
    $font = [System.Drawing.Font]::new("Arial", 8.2, [System.Drawing.FontStyle]::Regular)
    $boldFont = [System.Drawing.Font]::new("Arial", 8.2, [System.Drawing.FontStyle]::Bold)

    $arrowBrush = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::White)
    $arrowPen = [System.Drawing.Pen]::new([System.Drawing.Color]::Black, 1.5)

    foreach ($c in $Callouts) {
        $bx = [int]$c.BoxX
        $by = [int]$c.BoxY
        $bw = [int]$c.BoxW
        $bh = [int]$c.BoxH
        $tx = [int]$c.TargetX
        $ty = [int]$c.TargetY

        # Smart arrow start position on box border
        $boxCenterX = $bx + ($bw / 2)
        $boxCenterY = $by + ($bh / 2)

        if ($tx -gt ($bx + $bw)) {
            $startX = $bx + $bw
            $startY = [Math]::Max($by + 10, [Math]::Min($by + $bh - 10, $ty))
        } elseif ($tx -lt $bx) {
            $startX = $bx
            $startY = [Math]::Max($by + 10, [Math]::Min($by + $bh - 10, $ty))
        } elseif ($ty -lt $by) {
            $startX = [Math]::Max($bx + 10, [Math]::Min($bx + $bw - 10, $tx))
            $startY = $by
        } else {
            $startX = [Math]::Max($bx + 10, [Math]::Min($bx + $bw - 10, $tx))
            $startY = $by + $bh
        }

        # Draw Arrowhead
        $angle = [Math]::Atan2($ty - $startY, $tx - $startX)
        $arrowLen = 15
        $arrowAngle = [Math]::PI / 6

        $p1 = [System.Drawing.Point]::new($tx, $ty)
        $p2 = [System.Drawing.Point]::new([int]($tx - $arrowLen * [Math]::Cos($angle - $arrowAngle)), [int]($ty - $arrowLen * [Math]::Sin($angle - $arrowAngle)))
        $p3 = [System.Drawing.Point]::new([int]($tx - $arrowLen * [Math]::Cos($angle + $arrowAngle)), [int]($ty - $arrowLen * [Math]::Sin($angle + $arrowAngle)))

        $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
        $path.AddLine($p1, $p2)
        $path.AddLine($p2, $p3)
        $path.CloseFigure()

        $g.DrawLine($arrowPen, [int]$startX, [int]$startY, [int]$tx, [int]$ty)
        $g.FillPath($arrowBrush, $path)
        $g.DrawPath($arrowPen, $path)
        $path.Dispose()

        # Draw Callout Box
        $g.FillRectangle($boxBrush, $bx, $by, $bw, $bh)
        $g.DrawRectangle($boxPen, $bx, $by, $bw, $bh)

        # Draw Text
        $strFormat = [System.Drawing.StringFormat]::new()
        $strFormat.Alignment = [System.Drawing.StringAlignment]::Near
        $strFormat.LineAlignment = [System.Drawing.StringAlignment]::Near
        $strFormat.Trimming = [System.Drawing.StringTrimming]::Word

        $textRect = [System.Drawing.RectangleF]::new($bx + 6, $by + 6, $bw - 12, $bh - 12)
        $g.DrawString($c.Text, $font, $textBrush, $textRect, $strFormat)
        $strFormat.Dispose()
    }

    # Dispose
    $boxBrush.Dispose()
    $boxPen.Dispose()
    $textBrush.Dispose()
    $font.Dispose()
    $boldFont.Dispose()
    $arrowBrush.Dispose()
    $arrowPen.Dispose()

    $bmp.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
    Write-Host "Generated annotated image saved to: $OutputPath"
}
