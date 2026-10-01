# Decorative scene video loops

These MP4s are **AI-generated still images with a 2D camera move added using FFmpeg**. They are not native AI-generated temporal video, physical water/cloud/foliage simulations, photographs of claimed real locations, or project rendering results. No real project screenshot was used or modified to produce them.

The stills were generated with OpenAI `image_gen` on 2026-10-01. Their prompts, origin, and attribution are documented in [`assets/images/scenes/SOURCES.md`](../../../assets/images/scenes/SOURCES.md). No third-party stock image/video or Stillmind CDN resource is included. These generated assets do not carry a claimed stock-photo license or an assertion of exclusive copyright.

| Output files | Source still | Purpose |
| --- | --- | --- |
| `ocean-desktop.mp4`, `ocean-mobile.mp4` | `assets/images/scenes/ocean.webp` | Decorative morning ocean with islands |
| `light-desktop.mp4`, `light-mobile.mp4` | `assets/images/scenes/golden-light.webp` | Decorative golden mountain/lake scene |
| `forest-desktop.mp4`, `forest-mobile.mp4` | `assets/images/scenes/forest.webp` | Decorative forest/lake scene |

Each loop is 12 seconds / 288 frames at 24 fps, encoded as H.264 High profile, level 3.1, `yuv420p`, with no audio track. Desktop outputs are 1280 × 720; mobile outputs are independent centered 540 × 800 crops. `+faststart` places MP4 metadata before the video payload for progressive loading. All video files are served locally by the site.

The camera zoom follows `1 + 0.018 × (1 − cos(2π × frame / 287))`: it starts at the original crop, gently reaches 1.036× at mid-loop, then returns to its initial crop with zero velocity at the boundary. It does not abruptly reset from a maximum zoom. A 4× intermediate working size reduces integer-crop jitter before downsampling to the final dimensions. The imagery itself remains a still; waves, foliage, and clouds do not undergo generated scene motion.

## Rebuild

From the repository root with an FFmpeg executable that includes `libx264`:

```powershell
./scripts/build-scene-videos.ps1 -FFmpegPath 'C:/path/to/ffmpeg.exe'
```

[`scripts/build-scene-videos.ps1`](../../../scripts/build-scene-videos.ps1) accepts source/output directories, an individual scene name, duration, frame rate, CRF, maximum zoom, and working oversampling. Default encoding uses `libx264`, preset `slow`, CRF 27. The script does not download tools or modify original stills.

For this build, FFmpeg 7.1 was extracted locally from the [imageio-ffmpeg 0.6.0 Windows wheel on PyPI](https://pypi.org/project/imageio-ffmpeg/0.6.0/). The wheel's SHA-256 was checked against PyPI's published digest: `02fa47c83703c37df6bfe4896aab339013f62bf02c5ebf2dce6da56af04ffc0a`. The build tool stays outside the site checkout and is not shipped with the website.

## Verified outputs, 2026-10-01

| File | Bytes |
| --- | ---: |
| `ocean-desktop.mp4` | 783,515 |
| `ocean-mobile.mp4` | 318,966 |
| `light-desktop.mp4` | 1,068,177 |
| `light-mobile.mp4` | 343,190 |
| `forest-desktop.mp4` | 1,202,803 |
| `forest-mobile.mp4` | 436,403 |

All six files completed a full FFmpeg decode without errors. Container metadata confirms dimensions, 12-second duration, 24 fps, H.264/yuv420p, no audio, and faststart atom ordering. First-frame desktop/mobile crops were opened and visually inspected. First-versus-last decoded grayscale frames have mean absolute differences below 1 on a 0–255 scale at a 160 × 90 comparison size, while midpoint frames differ clearly; this confirms actual camera movement with a near-matching encoded loop boundary. Page-level playback, pause, scene switching, and reduced-motion behavior are verified separately in the website.
