# Homepage background photographs

Selected on 2026-10-02. These are decorative photographs, separate from the actual project screenshots in `assets/images/projects/`.

The earlier reference was [Stillmind / awesome-web-prompts](https://github.com/DexZane/awesome-web-prompts/tree/main/prompts/sections/hero/stillmind). Its external video links do not establish a reusable photo license. The same repository's [scroll-expansion-hero prompt](https://github.com/DexZane/awesome-web-prompts/blob/main/prompts/components/scroll-expansion-hero/prompt.md) directly references the valley and underwater photographs below. Three additional Unsplash photographs supply orange, green and purple scenes.

All five images are used under the [Unsplash License](https://unsplash.com/license), which permits downloading, modifying and using photographs on a website without mandatory on-image attribution. Source and photographer records are retained here. This site does not use the Unsplash API, hotlink its backgrounds or present these photographs as personal rendering work.

| Local asset | Source | Selection |
| --- | --- | --- |
| `valley.webp` | [Bailey Zindel on Unsplash](https://unsplash.com/photos/river-in-yosemite-valley-at-low-light-NRQV-hBF10M) · [image](https://images.unsplash.com/photo-1506744038136-46273834b3fb) | Blue mountain valley and peach sunset; directly referenced by scroll-expansion-hero |
| `dunes.webp` | [Zuyet Awarmatik on Unsplash](https://unsplash.com/photos/vibrant-orange-sand-dunes-under-a-soft-sky-7_qz7SWCSVg) · [image](https://images.unsplash.com/photo-1751817617405-fa66da15276b) | Orange sand dunes |
| `woodland.webp` | [Sebastian Unrau on Unsplash](https://unsplash.com/photos/trees-on-forest-with-sun-rays-sp-p7uuT0tw) · [image](https://images.unsplash.com/photo-1448375240586-882707db888b) | Green woodland with sunlight |
| `underwater.webp` | [Unsplash original image](https://images.unsplash.com/photo-1682687982501-1e58ab814714) | Blue water and coral; directly referenced by scroll-expansion-hero |
| `lavender.webp` | [Héctor J. Rivas on Unsplash](https://unsplash.com/photos/a-beautiful-lavender-field-at-sunset-with-distant-mountains-vRLz5so6Zok) · [image](https://images.unsplash.com/photo-1784105992783-a48345381a78) | Purple lavender field at sunset |

The local source copies were downloaded at 2560px width in WebP quality 84. Hugo generates 1920×1080 and 1280×720 desktop crops, plus 750×1100 and 480×704 mobile crops. Only the initial scene is loaded at page entry; subsequent pictures remain in inert templates until requested. Switching is manual, with a 300ms fade that respects reduced motion.

The former three generated backgrounds, their MP4 derivatives and the video-generation script have been removed from the site.
