[CmdletBinding()]
param(
    [string]$FFmpegPath = 'ffmpeg',
    [string]$SourceDirectory = (Join-Path $PSScriptRoot '../assets/images/scenes'),
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '../static/media/scenes'),
    [ValidateSet('all', 'ocean', 'light', 'forest')]
    [string]$Scene = 'all',
    [ValidateRange(2, 60)]
    [double]$Duration = 12,
    [ValidateRange(1, 60)]
    [int]$Fps = 24,
    [ValidateRange(0, 51)]
    [int]$Crf = 27,
    [ValidateRange(0, 0.2)]
    [double]$MaxZoom = 0.036,
    [ValidateRange(2, 4)]
    [int]$Oversample = 4
)

$ErrorActionPreference = 'Stop'
$encoder = (Get-Command $FFmpegPath -ErrorAction Stop).Source
$sourceRoot = (Resolve-Path -LiteralPath $SourceDirectory).Path
$outputRoot = [IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null

# These are AI stills with a 2D camera move, not generated temporal video or
# physical water/cloud/foliage simulation. Keep real project screenshots separate.
$scenes = @(
    @{ Name = 'ocean'; Image = 'ocean.webp' },
    @{ Name = 'light'; Image = 'golden-light.webp' },
    @{ Name = 'forest'; Image = 'forest.webp' }
)
$sizes = @(
    @{ Name = 'desktop'; Width = 1280; Height = 720 },
    @{ Name = 'mobile'; Width = 540; Height = 800 }
)
$frameCount = [int][Math]::Round($Duration * $Fps)
$lastFrame = $frameCount - 1
$halfZoom = ($MaxZoom / 2).ToString('0.######', [Globalization.CultureInfo]::InvariantCulture)

foreach ($item in $scenes) {
    if ($Scene -ne 'all' -and $item.Name -ne $Scene) { continue }
    $sourceFile = Join-Path $sourceRoot $item.Image
    if (-not (Test-Path -LiteralPath $sourceFile -PathType Leaf)) {
        throw "Missing source image: $sourceFile"
    }

    foreach ($size in $sizes) {
        $workWidth = $size.Width * $Oversample
        $workHeight = $size.Height * $Oversample
        $outputFile = Join-Path $outputRoot ($item.Name + '-' + $size.Name + '.mp4')

        # Separate centered cover crops keep the image undistorted on each format.
        # Oversampling makes zoompan's integer crop positions subpixel at output.
        # cos() returns to the initial crop on the final frame, with zero velocity
        # at both endpoints. There is no hard jump from a maximum zoom to the start.
        $filter = "scale=${workWidth}:${workHeight}:force_original_aspect_ratio=increase:flags=lanczos," +
            "crop=${workWidth}:${workHeight},format=yuv444p," +
            "zoompan=z='1+$halfZoom*(1-cos(2*PI*on/$lastFrame))':" +
            "x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':" +
            "d=${frameCount}:s=$($size.Width)x$($size.Height):fps=${Fps}," +
            'setsar=1,format=yuv420p'

        $arguments = @(
            '-hide_banner', '-loglevel', 'error', '-y',
            '-i', $sourceFile, '-vf', $filter,
            '-frames:v', $frameCount, '-an', '-sn', '-dn',
            '-c:v', 'libx264', '-preset', 'slow', '-crf', $Crf,
            '-profile:v', 'high', '-level:v', '3.1', '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart', '-map_metadata', '-1',
            '-metadata', 'comment=AI-generated decorative still; seamless 2D camera movement; not a project rendering or native AI-generated video.',
            $outputFile
        )
        & $encoder @arguments
        if ($LASTEXITCODE -ne 0) { throw "FFmpeg failed for $outputFile (exit $LASTEXITCODE)" }

        $result = Get-Item -LiteralPath $outputFile
        [PSCustomObject]@{
            File = $result.Name
            Size = "$($size.Width)x$($size.Height)"
            Duration = $frameCount / $Fps
            Fps = $Fps
            Bytes = $result.Length
        }
        if ($result.Length -gt 2000000) {
            Write-Warning "$($result.Name) exceeds 2 MB; consider a higher -Crf or shorter -Duration."
        }
    }
}
