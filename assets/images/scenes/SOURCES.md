# Homepage animation backgrounds

Created on 2026-10-02 with the built-in OpenAI `image_gen` tool. These five images are generated decorative 2D animation-style environments, separate from the actual project screenshots in `assets/images/projects/`. No external photographs, animation frames or reference images were used.

## Generation briefs

The descriptions below summarize the generation prompts; they are not verbatim prompt transcripts.

| Local asset | Scene brief |
| --- | --- |
| `anime-coast.webp` | Summer coast in Japanese 2D animation background art. |
| `anime-autumn.webp` | Autumn mountain valley in Japanese 2D animation background art. |
| `anime-forest.webp` | Forest lake in Japanese 2D animation background art. |
| `anime-night.webp` | Blue-violet starry sky, a faint Milky Way, layered mountains and their reflection in a lake, with blue-violet flowers and grasses along the shore. |
| `anime-spring.webp` | Pink and white cherry blossom branches frame a spring riverside; scattered petals, shallow cyan water, distant hills and soft clouds, with an uncluttered center. |

The shared brief requested refined hand-painted digital backgrounds with simplified shapes and soft lighting, rather than photographs or realistic 3D. Each scene is one wide composition that remains coherent in a central mobile crop. The prompts exclude people, humanoids, silhouettes, faces, animals, statues, mecha, text, logos, watermarks and UI. No black overlay was baked into the source artwork; the website applies its own CSS shading for title readability.

## Image processing

The generated source PNGs are 1672×941 pixels, approximately 16:9. Repository assets are WebP conversions at quality 86. Hugo produces a desktop image at the original size and quality 82, plus a 1280px-wide version at quality 80. Mobile images use centered 640×940 and 480×704 crops at quality 80. The desktop pipeline does not upscale the source images.

Page entry chooses a random background; other pictures remain in inert templates until requested. The arrows and an eight-second automatic rotation use a random queue without consecutive repeats. Switching waits for decoding, keeps the current picture underneath a 400ms fade, and retains it on failure. A pause control is available. Automatic rotation pauses offscreen, in hidden tabs, and while keyboard focus is on an arrow. Reduced motion disables automatic rotation and fades. With JavaScript disabled, a noscript fallback displays the first image.
