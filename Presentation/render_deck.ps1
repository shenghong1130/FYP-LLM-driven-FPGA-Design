$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$file = Join-Path $root '本科毕设_目标计划进展.pptx'
$preview = Join-Path $root 'Preview'
$app = New-Object -ComObject PowerPoint.Application
$deck = $null
try {
 $deck = $app.Presentations.Open($file, $true, $false, $false)
 for ($i=1; $i -le $deck.Slides.Count; $i++) {
  $deck.Slides.Item($i).Export((Join-Path $preview "slide_$i.png"), 'PNG', 1920, 1080)
 }
 Write-Output "Rendered $($deck.Slides.Count) slides."
} finally {
 if ($deck) { $deck.Close() }
 [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($app)
}
