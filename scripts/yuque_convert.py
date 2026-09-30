#!/usr/bin/env python3
"""Read a Yuque .lakebook tar without extraction and convert Lake/ASL to Markdown.

No rewriting, technical corrections, downloads, or repository writes are done here.
Dependencies: beautifulsoup4 (see requirements.txt).
API: convert_doc(doc, source_base=...) -> {body_markdown, markdown, quality}.
CLI: python yuque_convert.py Programming.lakebook --output converted
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import tarfile
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup, Comment, Doctype, NavigableString, Tag

SOURCE_BASE = "https://www.yuque.com/u62694975/iaaa"
KNOWN_CARDS = {"codeblock", "math", "image", "hr", "bookmarkInline", "bookmarklink"}
BLOCK_TAGS = {"p", "div", "blockquote", "ul", "ol", "table", "pre", "hr", "h1", "h2", "h3", "h4", "h5", "h6"}
EMPTY_FORMAT_TAGS = {"p", "span", "strong", "b", "em", "i", "u", "s", "del", "sub", "sup"}
PROSE_BOLD_RE = re.compile(r"(?<!\\)\*\*(?=\S)([^\n]+?)(?<=\S)\*\*")


def has_visible_text(value: str) -> bool:
    """Ignore editor-only whitespace/zero-width markers, never code payloads."""
    return bool(re.sub(r"[\s\u200b\u200c\u200d\ufeff]", "", value))


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def decode_card(node: Tag) -> dict:
    value = node.get("value", "")
    if not value.startswith("data:"):
        raise ValueError("Lake card value is not a data: value")
    payload = value[5:]
    if ";base64," in payload:
        payload = base64.b64decode(payload.split(";base64,", 1)[1]).decode("utf-8")
    elif payload.startswith("application/json,"):
        payload = unquote(payload.split(",", 1)[1])
    else:
        payload = unquote(payload)
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("Lake card payload must be an object")
    return data


def escape_text(value: str) -> str:
    # Code and math payloads never go through this function.
    value = html.escape(value, quote=False).replace("\xa0", "&nbsp;")
    value = value.replace("\\", "\\\\")
    # Goldmark's LaTeX passthrough treats \\[...\\] as display math. Literal
    # array/index brackets in prose must remain brackets, without those escapes.
    value = value.replace("[", "&#91;").replace("]", "&#93;")
    return re.sub(r"([`*_$])", r"\\\1", value)


def link_url(value: str) -> str:
    # Angle-bracket Markdown destinations handle parentheses in URLs.
    return value.replace(" ", "%20").replace("<", "%3C").replace(">", "%3E").replace("\n", "%0A")


def fenced(code: str, language: str = "") -> str:
    runs = [len(m.group()) for m in re.finditer(r"`+", code)]
    fence = "`" * max(3, max(runs, default=0) + 1)
    language = re.sub(r"[\r\n`\s]", "", language)
    return f"{fence}{language}\n{code}" + ("" if code.endswith("\n") else "\n") + fence


def normalize_blank_lines(markdown: str) -> str:
    """Use one blank line outside code, display math, and raw HTML tables/pre.

    Protected payload lines are appended byte-for-byte (including blank lines).
    The source export uses LF; this function does not alter code line endings.
    """
    lines = markdown.splitlines(keepends=True)
    out = []
    blank = False
    fence = None
    block = None
    fence_re = re.compile(r"^\s*(?:>\s*)*(`{3,}|~{3,})(.*)$")
    math_re = re.compile(r"^\s*(?:>\s*)*\$\$\s*$")
    for line in lines:
        if fence:
            out.append(line)
            close = fence_re.match(line.rstrip("\r\n"))
            if close and close[1][0] == fence[0] and len(close[1]) >= fence[1] and not close[2].strip():
                fence = None
            blank = False
            continue
        if block:
            out.append(line)
            if (block == "math" and math_re.match(line.rstrip("\r\n"))) or (block in {"table", "pre"} and re.search(r"</" + block + r"\s*>", line, re.I)):
                block = None
            blank = False
            continue
        match = fence_re.match(line.rstrip("\r\n"))
        if match:
            fence = (match[1][0], len(match[1]))
            out.append(line)
            blank = False
            continue
        if math_re.match(line.rstrip("\r\n")):
            block = "math"
            out.append(line)
            blank = False
            continue
        for candidate in ("table", "pre"):
            if re.search(r"<" + candidate + r"(?:\s|>)", line, re.I) and not re.search(r"</" + candidate + r"\s*>", line, re.I):
                block = candidate
                break
        if not line.strip():
            if not blank:
                out.append(line)
            blank = True
        else:
            out.append(line)
            blank = False
    return "".join(out)


def local_file_reference(url: str):
    """Identify file:///C:/ or /c:/ destinations without inventing a repo URL."""
    decoded = unquote(url)
    if decoded.lower().startswith("file:"):
        parsed = urlsplit(decoded)
        path = parsed.path
        fragment = parsed.fragment
    elif re.match(r"^/?[A-Za-z]:[/\\]", decoded):
        path, _, fragment = decoded.partition("#")
    else:
        return None
    path = path.replace("\\", "/")
    line_match = re.search(r":(\d+)(?::\d+)?$", path)
    line = int(line_match[1]) if line_match else None
    if line_match:
        path = path[:line_match.start()]
    if line is None and fragment:
        fragment_match = re.fullmatch(r"L?(\d+)(?:[-:]L?\d+)?", fragment)
        if fragment_match:
            line = int(fragment_match[1])
    filename = path.rsplit("/", 1)[-1]
    if not filename:
        return None
    return {"url": url, "decoded_path": path, "filename": filename, "line": line}


class LakeConverter:
    def __init__(self, doc: dict, source_base: str):
        self.doc = doc
        self.source_url = source_base.rstrip("/") + "/" + str(doc.get("slug", ""))
        self.warnings = []
        self.notes = Counter()
        self.rendered_cards = Counter()
        self.codes = []
        self.maths = []
        self.images = []
        self.links = []
        self.local_references = []
        self.anchors = []
        self.seen_tags = set()
        self.seen_text = set()
        self.seen_anchors = set()
        self.html_tables = 0
        self.md_tables = 0
        self.source_format = "body_asl" if doc.get("body_asl") else "body"
        source = doc.get(self.source_format) or ""
        self.soup = BeautifulSoup(source, "html.parser")
        # The site reserves H1 for its article title; retain the source's
        # relative section hierarchy by shifting the whole body, not only H1.
        self.heading_offset = 1 if self.soup.find("h1") else 0
        self.body_soup = BeautifulSoup(doc.get("body") or "", "html.parser")
        self.rendered_by_id = {str(n.get("id")): n for n in self.body_soup.find_all(id=True)}
        self.target_ids = set()
        for a in self.soup.find_all("a", href=True):
            frag = urlsplit(a["href"]).fragment
            if frag:
                self.target_ids.add(unquote(frag))
        self.card_data = {}
        for node in self.soup.find_all("card"):
            try:
                self.card_data[id(node)] = decode_card(node)
            except Exception as exc:
                self.warn("invalid-card-payload", str(exc), node)
        if source and self.source_format == "body":
            self.warn("html-fallback", "body_asl unavailable; HTML may contain rasterized formulas and flattened quotes")
        if doc.get("body_draft_asl") not in (None, "", doc.get("body_asl")):
            self.warn("draft-differs", "Published ASL selected; draft differs and remains in original archive")

    def warn(self, kind: str, detail: str, node=None, severity="warning"):
        item = {"kind": kind, "detail": detail, "severity": severity}
        if isinstance(node, Tag):
            data = self.card_data.get(id(node), {}) if hasattr(self, "card_data") else {}
            item.update({"tag": node.name, "id": node.get("id") or data.get("id"), "card": node.get("name")})
        self.warnings.append(item)
        return "<!-- conversion-warning: " + html.escape(kind + ": " + detail).replace("--", "—") + " -->"

    def mark(self, node):
        if isinstance(node, Tag):
            self.seen_tags.add(id(node))
        elif isinstance(node, NavigableString) and not isinstance(node, (Comment, Doctype)):
            self.seen_text.add(id(node))

    def mark_subtree(self, node):
        self.mark(node)
        if isinstance(node, Tag):
            for child in node.descendants:
                self.mark(child)

    def node_id(self, node: Tag) -> str:
        return str(node.get("id") or self.card_data.get(id(node), {}).get("id") or "")

    def anchor(self, node: Tag, force=False) -> str:
        ident = self.node_id(node)
        if not ident or ident in self.seen_anchors:
            return ""
        if not force and node.name not in BLOCK_TAGS | {"li", "card", "img"} and ident not in self.target_ids:
            return ""
        self.seen_anchors.add(ident)
        self.anchors.append(ident)
        return f'<a id="{html.escape(ident, quote=True)}"></a>'

    def styles(self, node: Tag, paragraph=False) -> str:
        pieces = []
        for piece in str(node.get("style", "")).split(";"):
            if ":" not in piece:
                continue
            key, value = [x.strip() for x in piece.split(":", 1)]
            # Preserve authored foreground/highlight and text alignment. Lake's
            # visual line-height, font classes and editor paragraph indentation
            # do not carry textual information; their count is recorded.
            if key in {"color", "background-color", "text-decoration"} or (paragraph and key == "text-align"):
                pieces.append(f"{key}: {value}")
            elif key:
                self.notes["editor_style_omitted:" + key] += 1
        return "; ".join(pieces)

    def inline_children(self, node: Tag, math_block=False) -> str:
        return "".join(self.render(c, math_block=math_block) for c in node.children)

    def prose_text(self, value: str, html_mode=False) -> str:
        escape = (lambda text: html.escape(text, quote=False)) if html_mode else escape_text
        out = []
        cursor = 0
        for pair in PROSE_BOLD_RE.finditer(value):
            out.extend([escape(value[cursor:pair.start()]), "<strong>", escape(pair[1]), "</strong>"])
            cursor = pair.end()
            self.notes["literal_markdown_bold_normalized"] += 1
        out.append(escape(value[cursor:]))
        return "".join(out)

    def empty_format(self, node: Tag):
        if node.name not in EMPTY_FORMAT_TAGS or has_visible_text(node.get_text()):
            return None
        # A formula/image/card remains meaningful even without text children.
        if node.find(["card", "img", "pre", "hr"]):
            return None
        self.mark_subtree(node)
        self.notes["empty_format_node_omitted:" + node.name] += 1
        # Keep anchors targeted by source links, including descendant anchors.
        # Untargeted editor placeholders add no visible content or separators.
        return "".join(self.anchor(n, force=True) for n in [node, *node.find_all(True)] if self.node_id(n) in self.target_ids)

    def block_children(self, node: Tag) -> str:
        return "".join(self.render(c) for c in node.children)

    def card(self, node: Tag, math_block=False, html_mode=False) -> str:
        name = str(node.get("name") or "unknown")
        self.rendered_cards[name] += 1
        data = self.card_data.get(id(node))
        if data is None or name not in KNOWN_CARDS:
            marker = self.warn("unknown-card", f"Card {name} retained as encoded source; manual conversion required", node)
            self.mark_subtree(node)
            raw = html.escape(str(node))
            return marker + f"\n<details><summary>Unconverted Lake card: {html.escape(name)}</summary><pre>{raw}</pre></details>\n"
        anchor = self.anchor(node, force=True)
        if name == "hr":
            return anchor + ("<hr>" if html_mode else "\n\n---\n\n")
        if name == "codeblock":
            code = str(data.get("code", ""))
            mode = str(data.get("mode", ""))
            record = {"id": data.get("id"), "language": mode, "characters": len(code), "sha256": sha(code), "payload_preserved": True}
            self.codes.append(record)
            html_node = self.rendered_by_id.get(str(data.get("id", "")))
            if html_node and html_node.name == "pre" and html_node.get_text() != code:
                self.warn("html-asl-code-disagreement", "ASL raw code selected; rendered HTML code differs", node)
            if data.get("collapsed") or data.get("foldLines") or data.get("lightLines"):
                self.notes["code_presentation_metadata_not_applied"] += 1
            name_text = str(data.get("name") or "")
            caption = (html.escape(name_text) if html_mode else escape_text(name_text)) + "\n" if name_text else ""
            if html_mode:
                return anchor + caption + f'<pre><code class="language-{html.escape(mode, quote=True)}">{html.escape(code)}</code></pre>'
            # A Lake codeblock mode 'latex' often contains plain Chinese flow
            # diagrams. Preserve its authored code language; never turn it into
            # a formula merely because the language is named latex.
            return "\n\n" + anchor + "\n" + caption + fenced(code, mode) + "\n\n"
        if name == "math":
            code = str(data.get("code", ""))
            self.maths.append({"id": data.get("id"), "code": code, "sha256": sha(code), "src": data.get("src"), "display": math_block, "payload_preserved": True})
            if not code:
                marker = self.warn("empty-math-payload", "Formula has no LaTeX code; source image retained", node)
                src = str(data.get("src") or "")
                return marker + (f'<img src="{html.escape(src, quote=True)}" alt="Formula">' if src else "")
            if "$" in code:
                self.warn("math-delimiter-in-payload", "LaTeX payload contains a dollar sign; review delimiter nesting", node)
            formula_code = html.escape(code, quote=False) if html_mode else code
            formula = "\n\n$$\n" + formula_code + "\n$$\n\n" if math_block and not html_mode else "$" + formula_code + "$"
            return anchor + formula
        if name == "image":
            src = str(data.get("src") or "")
            title = str(data.get("title") or "")
            visible_title = bool(data.get("showTitle"))
            crop = data.get("crop") or [0, 0, 1, 1]
            self.images.append({"id": data.get("id"), "src": src, "title": title, "showTitle": visible_title, "crop": crop, "rotation": data.get("rotation", 0), "width": data.get("width"), "height": data.get("height"), "originWidth": data.get("originWidth"), "originHeight": data.get("originHeight")})
            if not src:
                return self.warn("missing-image-src", "Image card missing src", node) + html.escape(json.dumps(data, ensure_ascii=False))
            attrs = {"src": src, "alt": title if visible_title else "", "loading": "lazy"}
            if data.get("width"):
                attrs["width"] = str(data["width"])
            if data.get("height"):
                attrs["height"] = str(data["height"])
            crop_markup = ""
            image_style = "max-width: 100%; height: auto"
            if crop != [0, 0, 1, 1]:
                attrs["data-yuque-crop"] = json.dumps(crop, separators=(",", ":"))
                # Lake crop stores normalized x/y/width/height. Preserve its
                # visual viewport with CSS while retaining the original file.
                try:
                    x, y, w, h = map(float, crop)
                    ow, oh = float(data["originWidth"]), float(data["originHeight"])
                    if w <= 0 or h <= 0:
                        raise ValueError("nonpositive crop")
                    image_style = f"position: absolute; width: {100 / w:.8g}%; max-width: none; height: auto; left: {-100 * x / w:.8g}%; top: {-100 * y / h:.8g}%"
                    crop_markup = f'<div style="position: relative; overflow: hidden; width: 100%; aspect-ratio: {ow*w:.8g} / {oh*h:.8g}">'
                    self.notes["image_crop_preserved_via_css"] += 1
                except (ValueError, TypeError, KeyError):
                    self.warn("image-crop-not-applied", "Crop metadata retained; dimensions unavailable for CSS viewport", node)
            rotation = data.get("rotation", 0)
            if rotation:
                attrs["data-yuque-rotation"] = str(rotation)
                self.warn("image-rotation-not-applied", "Rotation metadata retained; manual visual verification required", node)
            attrs["style"] = image_style
            img = "<img " + " ".join(f'{k}="{html.escape(v, quote=True)}"' for k, v in attrs.items()) + ">"
            if crop_markup:
                img = crop_markup + img + "</div>"
            if visible_title:
                caption = f"<figcaption>{html.escape(title)}</figcaption>"
                img = "<figure>" + img + caption + "</figure>"
            return anchor + img
        # A bookmark's meaningful content is its URL and visible label; retain
        # block-card description too. Icon/preview-image metadata is reported.
        src = str(data.get("src") or data.get("detail", {}).get("url") or "")
        label = str(data.get("text") or data.get("detail", {}).get("title") or src)
        self.links.append({"url": src, "label": label, "kind": name})
        detail = data.get("detail") or {}
        local = local_file_reference(src)
        if local:
            rendered = self.local_label(src, label, html_mode=html_mode)
        elif html_mode:
            rendered = f'<a href="{html.escape(src, quote=True)}">{html.escape(label)}</a>'
        else:
            rendered = f"[{escape_text(label)}](<{link_url(src)}>)"
        if name == "bookmarklink":
            card_title = str(detail.get("title") or "")
            desc = str(detail.get("desc") or "")
            if card_title and card_title != label:
                rendered += ("<br>" if html_mode else "\n\n") + (html.escape(card_title) if html_mode else escape_text(card_title))
            if desc:
                rendered += ("<br>" if html_mode else "\n\n") + (html.escape(desc) if html_mode else escape_text(desc))
            self.notes["bookmark_preview_decoration_omitted"] += 1
            return anchor + rendered + ("" if html_mode else "\n\n")
        return anchor + rendered

    def local_label(self, url: str, label: str, html_mode=False) -> str:
        reference = local_file_reference(url)
        name = reference["filename"]
        visible = name + (":" + str(reference["line"]) if reference["line"] is not None else "")
        # Retain a meaningful authored label in addition to the readable file
        # reference. Filename labels need only the line suffix added.
        plain_label = label.strip()
        if plain_label and plain_label != name and plain_label != visible:
            visible = plain_label + "（" + visible + "）"
        reference.update({"source_label": label, "replacement_text": visible, "yuque_slug": self.doc.get("slug")})
        self.local_references.append(reference)
        self.notes["local_file_link_replaced_with_readable_reference"] += 1
        return "<code>" + html.escape(visible) + "</code>" if html_mode else "`" + visible.replace("`", "\\`") + "`"

    def render_html(self, node) -> str:
        self.mark(node)
        if isinstance(node, (Comment, Doctype)):
            return ""
        if isinstance(node, NavigableString):
            if any(parent.name in {"pre", "code"} for parent in node.parents):
                return html.escape(str(node), quote=False)
            return self.prose_text(str(node), html_mode=True)
        if not isinstance(node, Tag):
            return ""
        if node.name == "meta":
            self.mark_subtree(node)
            return ""
        if node.name == "card":
            return self.card(node, html_mode=True)
        empty = self.empty_format(node)
        if empty is not None:
            return empty
        allowed = {"table", "thead", "tbody", "tfoot", "tr", "td", "th", "colgroup", "col", "caption", "p", "span", "strong", "b", "em", "i", "u", "s", "del", "sub", "sup", "br", "a", "code", "ul", "ol", "li", "blockquote", "div", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "img", "pre"}
        if node.name not in allowed:
            marker = self.warn("unknown-html-node", f"Unexpected {node.name} retained as escaped source", node)
            self.mark_subtree(node)
            return marker + "<pre>" + html.escape(str(node)) + "</pre>"
        attrs = {}
        ident = self.node_id(node)
        if ident:
            attrs["id"] = ident
            if ident not in self.seen_anchors:
                self.anchors.append(ident)
                self.seen_anchors.add(ident)
        for key in ("href", "src", "alt", "title", "rowspan", "colspan", "start", "type", "width", "height"):
            if key in node.attrs:
                attrs[key] = str(node[key])
        style = self.styles(node, paragraph=True)
        if node.name in {"ul", "ol"} and node.get("data-lake-indent"):
            try:
                style += ("; " if style else "") + f"margin-left: {int(node['data-lake-indent']) * 2}em"
                attrs["data-yuque-indent"] = str(node["data-lake-indent"])
            except ValueError:
                self.warn("invalid-list-indent", "List indent metadata is not an integer", node)
        if style:
            attrs["style"] = style
        if node.name == "a":
            self.links.append({"url": node.get("href", ""), "label": node.get_text(), "kind": "a"})
            if local_file_reference(str(node.get("href", ""))):
                self.mark_subtree(node)
                return self.anchor(node) + self.local_label(str(node["href"]), node.get_text(), html_mode=True)
        attr_text = "".join(f' {k}="{html.escape(v, quote=True)}"' for k, v in attrs.items())
        if node.name in {"br", "hr", "img", "col"}:
            return f"<{node.name}{attr_text}>"
        element = "h" + str(min(6, int(node.name[1]) + self.heading_offset)) if re.fullmatch(r"h[1-6]", node.name) else node.name
        return f"<{element}{attr_text}>" + "".join(self.render_html(c) for c in node.children) + f"</{element}>"

    def table(self, node: Tag) -> str:
        rows = node.find_all("tr", recursive=True)
        cells = [row.find_all(["td", "th"], recursive=False) for row in rows]
        complex_table = not rows or any(len(row) != len(cells[0]) for row in cells)
        for row in cells:
            for cell in row:
                if cell.has_attr("rowspan") or cell.has_attr("colspan") or len(cell.find_all("p", recursive=False)) > 1 or cell.find(["ul", "ol", "table", "pre", "card"]):
                    complex_table = True
                if cell.get("style") or cell.find(style=True):
                    complex_table = True
        # Do not invent a header row when source's first row is not marked or
        # visually header-like; raw HTML retains exact table structure.
        header = bool(cells) and all(c.name == "th" or c.find("strong") for c in cells[0])
        if complex_table or not header:
            self.html_tables += 1
            return "\n\n" + self.render_html(node) + "\n\n"
        self.md_tables += 1
        self.mark_subtree(node.find("colgroup")) if node.find("colgroup") else None
        out = [self.anchor(node, force=True)]
        for ri, row in enumerate(cells):
            self.mark(rows[ri])
            self.mark(rows[ri].parent)
            contents = []
            for cell in row:
                self.mark(cell)
                value = self.anchor(cell, force=bool(self.node_id(cell) in self.target_ids)) + self.inline_children(cell).strip()
                value = re.sub(r"\n+", "<br>", value).replace("|", "\\|")
                contents.append(value)
            out.append("| " + " | ".join(contents) + " |")
            if ri == 0:
                out.append("| " + " | ".join("---" for _ in row) + " |")
        return "\n\n" + "\n".join(out) + "\n\n"

    def render_list(self, node: Tag) -> str:
        # Lake serializes many visual nested lists as separate flat siblings.
        # HTML preserves their explicit offsets rather than accidentally turning
        # four-space-indented Markdown into a code block or inventing nesting.
        if node.get("data-lake-indent") or node.get("style"):
            self.notes["flat_list_indentation_preserved_in_html"] += 1
            return "\n\n" + self.render_html(node) + "\n\n"
        out = []
        self.mark(node)
        if self.node_id(node):
            out.append(self.anchor(node))
        start = int(node.get("start", 1))
        n = 0
        for child in node.children:
            if isinstance(child, NavigableString):
                self.mark(child)
                if str(child).strip():
                    out.append(escape_text(str(child)))
                continue
            if not isinstance(child, Tag):
                continue
            if child.name != "li":
                out.append(self.render(child).strip())
                continue
            self.mark(child)
            marker = f"{start + n}. " if node.name == "ol" else "- "
            n += 1
            rendered = self.anchor(child, force=True) + self.inline_children(child).strip()
            lines = rendered.splitlines() or [""]
            out.append(marker + lines[0])
            out.extend(" " * len(marker) + line if line else "" for line in lines[1:])
        return "\n\n" + "\n".join(out) + "\n\n"

    def render(self, node, math_block=False) -> str:
        self.mark(node)
        if isinstance(node, (Comment, Doctype)):
            return ""
        if isinstance(node, NavigableString):
            return self.prose_text(str(node))
        if not isinstance(node, Tag):
            return ""
        tag = node.name
        if tag in {"meta", "head"}:
            self.mark_subtree(node)
            return ""
        if tag == "card":
            return self.card(node, math_block=math_block)
        empty = self.empty_format(node)
        if empty is not None:
            return empty
        if tag in {"html", "body", "div"}:
            return self.anchor(node) + self.block_children(node)
        if tag == "p":
            cards = node.find_all("card")
            only_math = len(cards) == 1 and cards[0].get("name") == "math" and not node.get_text(strip=True)
            value = self.inline_children(node, math_block=only_math).strip()
            # No blanket newline cleanup: code payloads and math must keep their
            # exact authored line breaks, including empty lines.
            anchor = self.anchor(node)
            style = self.styles(node, paragraph=True)
            if style and "text-align" in style and not cards:
                return "\n\n" + anchor + f'<p style="{html.escape(style, quote=True)}">' + self.render_html_children_without_recount(node) + "</p>\n\n"
            return "\n\n" + anchor + value + "\n\n"
        if re.fullmatch(r"h[1-6]", tag):
            value = self.inline_children(node).strip()
            body_node = self.rendered_by_id.get(self.node_id(node))
            # Yuque's automatic heading counters exist only in rendered HTML.
            prefixes = body_node.find_all(attrs={"lake-read-ignore": "true"}, recursive=False) if body_node else []
            if prefixes:
                value = "".join(escape_text(p.get_text()) for p in prefixes) + value
                self.notes["automatic_heading_number_restored"] += 1
            return "\n\n" + self.anchor(node) + "\n" + "#" * min(6, int(tag[1]) + self.heading_offset) + " " + value + "\n\n"
        if tag == "blockquote":
            value = (self.anchor(node) + self.block_children(node)).strip()
            return "\n\n" + "\n".join("> " + line if line else ">" for line in value.splitlines()) + "\n\n"
        if tag in {"ul", "ol"}:
            return self.render_list(node)
        if tag == "li":
            return self.anchor(node) + self.inline_children(node)
        if tag == "table":
            return self.table(node)
        if tag == "pre":
            self.mark_subtree(node)
            mode = str(node.get("data-language") or "")
            code = node.get_text()
            self.codes.append({"id": self.node_id(node), "language": mode, "characters": len(code), "sha256": sha(code), "payload_preserved": True, "html_fallback": True})
            return "\n\n" + self.anchor(node) + "\n" + fenced(code, mode) + "\n\n"
        if tag == "code":
            self.mark_subtree(node)
            value = node.get_text()
            runs = [len(m.group()) for m in re.finditer(r"`+", value)]
            fence = "`" * max(1, max(runs, default=0) + 1)
            padding = " " if value.startswith(("`", " ")) or value.endswith(("`", " ")) else ""
            if "\n" in value:
                self.warn("inline-code-newline", "Source inline code contains newline; HTML retained", node)
                return self.anchor(node) + "<code>" + html.escape(value) + "</code>"
            return self.anchor(node) + fence + padding + value + padding + fence
        if tag == "a":
            href = str(node.get("href") or "")
            label = self.inline_children(node)
            self.links.append({"url": href, "label": node.get_text(), "kind": "a"})
            if local_file_reference(href):
                return self.anchor(node) + self.local_label(href, node.get_text())
            return self.anchor(node) + (f"[{label}](<{link_url(href)}>)" if href else label)
        if tag == "span":
            value = self.inline_children(node, math_block=math_block)
            style = self.styles(node)
            if node.get("class"):
                self.notes["editor_font_class_omitted"] += 1
            return self.anchor(node) + (f'<span style="{html.escape(style, quote=True)}">{value}</span>' if style else value)
        if tag in {"strong", "b", "em", "i"}:
            value = self.inline_children(node, math_block=math_block)
            # CommonMark punctuation/CJK delimiter boundaries can show literal
            # asterisks. Inline HTML preserves Lake's authored emphasis reliably.
            element = "strong" if tag in {"strong", "b"} else "em"
            return self.anchor(node) + f"<{element}>" + value + f"</{element}>"
        if tag in {"u", "s", "del", "sub", "sup"}:
            return self.anchor(node) + f"<{tag}>" + self.inline_children(node) + f"</{tag}>"
        if tag == "br":
            return "  \n"
        if tag == "hr":
            return "\n\n" + self.anchor(node) + "\n---\n\n"
        if tag == "img":
            src = str(node.get("src") or "")
            self.images.append({"id": self.node_id(node), "src": src, "title": node.get("title", ""), "html_fallback": True})
            if "/__latex/" in src:
                self.warn("rasterized-formula-fallback", "Formula image has no available ASL LaTeX payload", node)
            attrs = {k: str(node[k]) for k in ("src", "alt", "title", "width", "height") if k in node.attrs}
            return self.anchor(node) + "<img " + " ".join(f'{k}="{html.escape(v, quote=True)}"' for k, v in attrs.items()) + ">"
        if tag in {"tbody", "thead", "tfoot", "tr", "td", "th", "colgroup", "col"}:
            return self.inline_children(node)
        marker = self.warn("unknown-node", f"Unexpected {tag} retained as escaped source; manual conversion required", node)
        self.mark_subtree(node)
        return "\n\n" + marker + "\n" + fenced(str(node), "html") + "\n\n"

    def render_html_children_without_recount(self, node: Tag) -> str:
        # Called only for text-only paragraphs; prior render recorded semantic
        # nodes. A raw clone avoids double-counting cards/links and preserves the
        # source's centered paragraph without embedding Markdown in a HTML block.
        clone = BeautifulSoup(str(node), "html.parser").find("p")
        for elem in clone.find_all(True):
            elem.attrs = {k: v for k, v in elem.attrs.items() if k in {"href", "style", "id"}}
        return "".join(str(c) for c in clone.contents)

    def convert(self) -> dict:
        body = normalize_blank_lines("".join(self.render(node) for node in self.soup.contents).strip() + "\n")
        nontrivial_strings = [n for n in self.soup.descendants if isinstance(n, NavigableString) and not isinstance(n, (Comment, Doctype)) and str(n).strip()]
        lost = [str(n) for n in nontrivial_strings if id(n) not in self.seen_text]
        if lost:
            self.warn("unvisited-source-text", f"{len(lost)} nonempty source text nodes were not visited; review required", severity="error")
        expected_cards = Counter(str(n.get("name") or "unknown") for n in self.soup.find_all("card"))
        if expected_cards != self.rendered_cards:
            self.warn("card-count-mismatch", "Source/rendered card counts differ", severity="error")
        tags = Counter(n.name for n in self.soup.find_all(True))
        unvisited_tags = Counter(n.name for n in self.soup.find_all(True) if id(n) not in self.seen_tags)
        substantive = bool(self.soup.get_text(strip=True) or self.soup.find("card"))
        metadata = {
            "title": self.doc.get("title", ""),
            "date": self.doc.get("created_at"),
            "lastmod": self.doc.get("updated_at"),
            "draft": False,
            "yuque_slug": self.doc.get("slug"),
            "yuque_id": self.doc.get("id"),
            "yuque_source": self.source_url,
            "math": bool(self.maths),
        }
        front = "---\n" + "\n".join(k + ": " + json.dumps(v, ensure_ascii=False) for k, v in metadata.items() if v is not None) + "\n---\n\n"
        provenance = "\n原文：[" + escape_text(str(self.doc.get("title") or self.doc.get("slug") or "语雀")) + "](<" + link_url(self.source_url) + ">)\n"
        quality = {
            "slug": self.doc.get("slug"), "id": self.doc.get("id"), "title": self.doc.get("title"), "source_url": self.source_url,
            "created_at": self.doc.get("created_at"), "updated_at": self.doc.get("updated_at"),
            "source_format": self.source_format, "source_empty": not substantive,
            "source_body_sha256": sha(self.doc.get("body") or ""), "source_asl_sha256": sha(self.doc.get("body_asl") or ""),
            "body_markdown_sha256": sha(body), "body_markdown_characters": len(body),
            "source_tags": dict(tags), "unvisited_tags": dict(unvisited_tags), "source_cards": dict(expected_cards), "converted_cards": dict(self.rendered_cards),
            "source_text_nodes": len(nontrivial_strings), "unvisited_text_nodes": len(lost), "unvisited_text_samples": lost[:5],
            "heading_level_offset": self.heading_offset,
            "headings": [{"level": int(n.name[1]), "rendered_level": min(6, int(n.name[1]) + self.heading_offset), "text": n.get_text(), "id": self.node_id(n)} for n in self.soup.find_all(re.compile(r"^h[1-6]$"))],
            "codes": self.codes, "maths": self.maths, "images": self.images, "links": self.links, "anchors": self.anchors,
            "local_reference_normalizations": self.local_references,
            "tables": {"source": tags.get("table", 0), "html": self.html_tables, "markdown": self.md_tables},
            "presentation_notes": dict(self.notes), "warnings": self.warnings,
            "fidelity_checks": {"all_source_text_nodes_visited": not lost, "all_cards_converted": expected_cards == self.rendered_cards, "all_code_payloads_preserved": all(n["payload_preserved"] for n in self.codes), "all_math_payloads_preserved": all(n["payload_preserved"] for n in self.maths)},
        }
        return {"body_markdown": body, "markdown": front + body + provenance, "quality": quality}


def convert_doc(doc: dict, source_base: str = SOURCE_BASE) -> dict:
    """Convert one exported doc object (or its {'doc': ...} wrapper)."""
    if "doc" in doc and isinstance(doc["doc"], dict):
        doc = doc["doc"]
    return LakeConverter(doc, source_base).convert()


def iter_lakebook(path: str | Path):
    """Yield (member_name, doc), reading members only; never extractall."""
    with tarfile.open(path, "r:*") as archive:
        for member in archive:
            if not member.isfile() or not member.name.endswith(".json") or member.name.endswith("$meta.json"):
                continue
            file = archive.extractfile(member)
            if file is None:
                continue
            wrapper = json.load(file)
            if isinstance(wrapper, dict) and isinstance(wrapper.get("doc"), dict):
                yield member.name, wrapper["doc"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lakebook", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="Temporary conversion directory; never point this at website content")
    parser.add_argument("--source-base", default=SOURCE_BASE)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    reports = []
    slugs = set()
    for member, doc in iter_lakebook(args.lakebook):
        slug = str(doc.get("slug") or "")
        if not re.fullmatch(r"[A-Za-z0-9_-]+", slug) or slug in slugs:
            raise ValueError(f"Invalid or duplicate source slug: {slug!r}")
        slugs.add(slug)
        result = convert_doc(doc, args.source_base)
        (args.output / (slug + ".md")).write_text(result["markdown"], encoding="utf-8", newline="\n")
        quality = result["quality"]
        quality["archive_member"] = member
        (args.output / (slug + ".quality.json")).write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reports.append(quality)
    totals = Counter()
    warning_counts = Counter()
    for report in reports:
        totals.update(report["converted_cards"])
        warning_counts.update(w["kind"] for w in report["warnings"])
    summary = {
        "source": str(args.lakebook.resolve()), "documents": len(reports), "source_empty_documents": sum(r["source_empty"] for r in reports),
        "converted_card_totals": dict(totals), "warning_counts": dict(warning_counts),
        "all_fidelity_checks_pass": all(all(r["fidelity_checks"].values()) for r in reports),
        "reports": reports,
    }
    (args.output / "conversion-quality.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    local_mapping = [item for report in reports for item in report["local_reference_normalizations"]]
    (args.output.parent / "local-reference-normalization.json").write_text(json.dumps({"count": len(local_mapping), "references": local_mapping}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "reports"}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
