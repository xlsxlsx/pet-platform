$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

$assetDir = Join-Path $PSScriptRoot "..\web\assets"
New-Item -ItemType Directory -Path $assetDir -Force | Out-Null

function New-Brush($hex) {
    return New-Object System.Drawing.SolidBrush ([System.Drawing.ColorTranslator]::FromHtml($hex))
}

function New-Pen($hex, $width) {
    return New-Object System.Drawing.Pen ([System.Drawing.ColorTranslator]::FromHtml($hex)), $width
}

function Save-Asset($name, $bg, $accent, $kind) {
    $bmp = New-Object System.Drawing.Bitmap 900, 600
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.Clear([System.Drawing.ColorTranslator]::FromHtml($bg))

    $white = New-Brush "#ffffff"
    $muted = New-Brush "#e8f1fb"
    $accentBrush = New-Brush $accent
    $dark = New-Brush "#1f2933"
    $linePen = New-Object System.Drawing.Pen ([System.Drawing.ColorTranslator]::FromHtml("#ffffff"), 14)
    $accentPen = New-Object System.Drawing.Pen ([System.Drawing.ColorTranslator]::FromHtml($accent), 16)
    $thinPen = New-Object System.Drawing.Pen ([System.Drawing.ColorTranslator]::FromHtml("#1f2933"), 8)

    $g.FillEllipse($muted, 610, -80, 360, 360)
    $g.FillEllipse($muted, -120, 360, 320, 320)
    $g.FillRectangle($white, 90, 360, 720, 86)

    if ($kind -eq "feeding") {
        $g.FillEllipse($accentBrush, 220, 190, 220, 220)
        $g.FillEllipse($white, 260, 248, 140, 92)
        $g.DrawArc($thinPen, 245, 252, 170, 120, 0, 180)
        $g.DrawLine($accentPen, 510, 180, 580, 325)
        $g.DrawLine($linePen, 535, 235, 595, 208)
        $g.FillEllipse($dark, 318, 180, 22, 22)
        $g.FillEllipse($dark, 370, 180, 22, 22)
    }
    elseif ($kind -eq "walking") {
        $g.FillEllipse($accentBrush, 210, 220, 230, 150)
        $g.FillEllipse($accentBrush, 400, 180, 120, 120)
        $g.FillEllipse($white, 432, 220, 18, 18)
        $g.DrawLine($thinPen, 506, 234, 640, 180)
        $g.DrawArc($thinPen, 620, 146, 80, 70, 190, 250)
        $g.FillRectangle($dark, 260, 345, 36, 82)
        $g.FillRectangle($dark, 360, 345, 36, 82)
    }
    elseif ($kind -eq "boarding") {
        $g.FillRectangle($accentBrush, 220, 210, 310, 190)
        $roof = New-Object System.Drawing.Drawing2D.GraphicsPath
        $roof.AddPolygon([System.Drawing.Point[]]@(
            [System.Drawing.Point]::new(190, 230),
            [System.Drawing.Point]::new(375, 110),
            [System.Drawing.Point]::new(560, 230)
        ))
        $g.FillPath($dark, $roof)
        $g.FillRectangle($white, 330, 300, 90, 100)
        $g.FillEllipse($white, 450, 255, 38, 38)
    }
    elseif ($kind -eq "food") {
        $g.FillRectangle($accentBrush, 250, 150, 250, 280)
        $g.FillRectangle($white, 285, 210, 180, 110)
        $g.FillEllipse($dark, 320, 245, 32, 32)
        $g.FillEllipse($dark, 395, 245, 32, 32)
        $g.FillRectangle($dark, 286, 150, 178, 42)
    }
    elseif ($kind -eq "care") {
        $g.FillEllipse($accentBrush, 260, 170, 240, 240)
        $g.FillRectangle($white, 344, 220, 74, 140)
        $g.FillRectangle($white, 310, 253, 140, 74)
        $g.DrawEllipse($thinPen, 570, 200, 90, 90)
        $g.DrawLine($thinPen, 635, 265, 700, 330)
    }
    else {
        $g.FillRectangle($accentBrush, 230, 170, 300, 220)
        $g.FillRectangle($white, 360, 210, 44, 130)
        $g.FillRectangle($white, 317, 253, 130, 44)
        $g.FillRectangle($dark, 260, 390, 240, 44)
        $g.FillEllipse($white, 610, 230, 90, 90)
    }

    $font = New-Object System.Drawing.Font "Segoe UI", 34, ([System.Drawing.FontStyle]::Bold)
    $smallFont = New-Object System.Drawing.Font "Segoe UI", 18, ([System.Drawing.FontStyle]::Regular)
    $g.DrawString("PetCare Hub", $font, $dark, 92, 475)
    $g.DrawString($name, $smallFont, $dark, 96, 525)

    $path = Join-Path $assetDir "$name.png"
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)

    $font.Dispose()
    $smallFont.Dispose()
    $linePen.Dispose()
    $accentPen.Dispose()
    $thinPen.Dispose()
    $white.Dispose()
    $muted.Dispose()
    $accentBrush.Dispose()
    $dark.Dispose()
    $g.Dispose()
    $bmp.Dispose()
}

Save-Asset "service-feeding" "#dff3ff" "#2f80ed" "feeding"
Save-Asset "service-walking" "#e8f7ed" "#27ae60" "walking"
Save-Asset "service-boarding" "#fff2dc" "#f2994a" "boarding"
Save-Asset "product-food" "#edf5ff" "#2f80ed" "food"
Save-Asset "product-care" "#f0fbf4" "#27ae60" "care"
Save-Asset "hospital-care" "#fff4f4" "#eb5757" "hospital"

