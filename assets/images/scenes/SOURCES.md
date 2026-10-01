# Hero scene assets

These three images are **AI-generated decorative atmosphere imagery**, not JiaT-T project screenshots, real project rendering results, or photographs of a claimed real location. Do not label them as portfolio work.

Generated on 2026-10-01 (Asia/Shanghai) using the built-in OpenAI `image_gen` tool through the `imagegen` skill. No external stock image, Stillmind CDN video, or Figma overlay was used as an input. Generated source PNG files are preserved outside the site checkout in `work/generated-scenes/` within the current task workspace. WebP files are compressed local derivatives used by Hugo resources.

| File | Use | Origin / attribution |
| --- | --- | --- |
| `ocean.webp` | Default home hero, 海面 scene | Original AI-generated decorative ocean/island morning; no third-party stock license claimed |
| `golden-light.webp` | Home hero, 光影 scene | Original AI-generated decorative mountain/lake sunrise; no third-party stock license claimed |
| `forest.webp` | Home hero, 森野 scene | Original AI-generated decorative forest/lake; no third-party stock license claimed |

These are generated assets rather than third-party licensed photographs. No claim of exclusive copyright or of a stock-photo license is made. Website use must identify the scenes as AI decorative imagery.

All three source images are 1672 × 941 pixels. Hugo Extended 0.167.0 encoded the local derivatives as WebP at quality 84 without upscaling: `ocean.webp` is 212,178 bytes, `golden-light.webp` is 269,080 bytes, and `forest.webp` is 338,170 bytes. The source PNGs and final WebP images were opened and visually inspected after generation and compression.

The ocean was generated as a separate decorative background from its text prompt; no FFT project screenshot was provided as an input or modified. Existing real project screenshots remain distinct portfolio assets.

## Full generation prompt: ocean.webp

```text
Use case: photorealistic-natural
Asset type: cinematic developer portfolio website hero background, original AI-generated decorative atmosphere image, wide 16:9 composition, at least 1672 pixels wide if possible.
Primary request: A cinematic ocean landscape viewed from a low but natural camera angle near the water. Rich deep blue-teal sea with sculptural translucent wave crests and clearly resolved white foam. Layered distant mountains and small rocky islands sit on the low horizon. Restrained soft morning light, finely textured water and subtle atmospheric mist. This is an independent decorative image, not a screenshot or reconstruction of any software project.
Style/medium: cinematic fine landscape photography aesthetic, physically believable natural water, realistic foam texture, refined color grading, continuous with natural forest lake and golden mountain lake imagery.
Composition/framing: full-bleed 16:9 landscape, no frame. Dynamic richly textured waves across the lower half and lower corners; a clear depth from near wave crests to distant islands. The upper middle and upper-left-center contain quiet uncluttered blue-grey sky and mist with moderately dark values suitable for a white website headline; avoid a bright sun or white cloud behind this region. Keep the central view recognizable in a narrow mobile crop.
Lighting/mood: subtle early morning directional light from the right, luminous turquoise translucency on select wave edges, carefully retained highlights and readable midtones. Saturated and dimensional but never neon, never uniformly dark, no overexposed patches, no heavy black vignette.
Color palette: deep navy and teal water, blue-grey atmospheric sky and distant islands, restrained soft warm light at the far right.
Constraints: no text, no letters, no typography, no logo, no watermark, no interface, no axes, no diagrams, no people, no ships, no buildings. No fantasy structures, no excessive lens flare, no artificial black gradient painted over the image. Generate an actual natural image, not a webpage mockup.
```

## Full generation prompt: golden-light.webp

```text
Use case: photorealistic-natural
Asset type: cinematic developer portfolio website hero background, decorative AI atmosphere image, 16:9 wide landscape composition.
Primary request: A richly textured and believable natural golden sunrise landscape. Deep blue-teal still lake water, layered distant mountains, amber sunlight entering from the right, foreground rocks and a few natural plants providing convincing spatial depth. Quiet open center and upper-left-center sky area suitable for overlaying a website headline. The lake and mountain silhouettes must remain recognizable in a narrow mobile center crop.
Style/medium: cinematic fine landscape photography aesthetic, physically believable natural light and surface texture, refined color grading, realistic rather than fantasy.
Lighting/mood: luminous warm sunlight at the right side and soft cool shadows, moderate contrast, detailed readable midtones, visible scenery, not darkened.
Color palette: deep blue, teal lake, restrained amber light, natural muted green vegetation.
Composition/framing: full-bleed image without a frame, wide 16:9; layered foreground at edges and lower corners; spacious calm center and upper-left; no text area rectangle baked into image.
Constraints: no text, no letters, no typography, no logo, no watermark, no UI, no people, no buildings; no fantasy structures, no neon, no excessive lens flare, no artificial black vignette. Generate an actual image, not a mockup of a webpage.
```

## Full generation prompt: forest.webp

```text
Use case: photorealistic-natural
Asset type: cinematic developer portfolio website hero background, decorative AI atmosphere image, 16:9 wide landscape composition.
Primary request: A lush blue-green and deep green forest around a small quiet lake, fine soft mist in distant trees, natural shafts of sunlight passing through the canopy, dark foreground ferns at the lower edges creating real depth. In the center distance there is open luminous air and calm lake reflections. Keep the left-middle and center relatively quiet and readable for website headline overlay while maintaining clear natural image content.
Style/medium: cinematic fine landscape photography aesthetic, believable tree bark, fern fronds, moist earth and water reflections, realistic natural proportions.
Lighting/mood: fresh atmospheric soft daylight, subtle sun rays, luminous translucent depth; readable details and midtones; richly green but not dark or fluorescent.
Color palette: natural blue-green, moss green, deep teal water, small warm sun highlights.
Composition/framing: full-bleed image without frame, wide 16:9; layered near ferns, middle water, distant misty forest; central lake and open clearing remain recognizable in a narrow mobile crop.
Constraints: no text, no letters, no typography, no logo, no watermark, no UI, no people, no buildings; no fantasy elements, no neon green, no heavy black vignette. Generate an actual image, not a mockup of a webpage.
```

