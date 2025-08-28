import os
import re
from html.parser import HTMLParser
from typing import List, Dict, Tuple

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")


class SimpleHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags: List[Tuple[str, Dict[str, str]]] = []
        self.in_head = False
        self.in_body = False
        self.text_stack: List[str] = []
        self.titles: List[str] = []
        self.h1_count = 0
        self.meta: List[Dict[str, str]] = []
        self.links: List[Dict[str, str]] = []
        self.scripts: List[Dict[str, str]] = []
        self.styles: List[str] = []
        self.buttons: List[Dict[str, str]] = []
        self.data_attrs: List[Tuple[str, Dict[str, str]]] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = {k: (v if v is not None else "") for k, v in attrs}
        self.tags.append((tag, attrs_dict))
        if tag == "head":
            self.in_head = True
        if tag == "body":
            self.in_body = True
        if tag == "meta":
            self.meta.append(attrs_dict)
        if tag == "link":
            self.links.append(attrs_dict)
        if tag == "script":
            self.scripts.append(attrs_dict)
        if tag == "style":
            self.text_stack.append("")
        if tag == "title":
            self.text_stack.append("")
        if tag == "h1":
            self.h1_count += 1
        # collect data- attributes per section
        if tag in ("section", "div"):
            data_attrs = {k: v for k, v in attrs_dict.items() if k.startswith("data-")}
            if data_attrs:
                self.data_attrs.append((tag, data_attrs))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        if tag == "body":
            self.in_body = False
        if tag == "style" and self.text_stack:
            self.styles.append(self.text_stack.pop())
        if tag == "title" and self.text_stack:
            self.titles.append(self.text_stack.pop().strip())

    def handle_data(self, data):
        if self.text_stack:
            self.text_stack[-1] += data

    def handle_startendtag(self, tag, attrs):
        # For self-closing tags
        if tag == "meta":
            self.meta.append({k: (v if v is not None else "") for k, v in attrs})


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_html(content: str) -> SimpleHTML:
    parser = SimpleHTML()
    parser.feed(content)
    return parser


def has_meta_viewport(parser: SimpleHTML) -> bool:
    for m in parser.meta:
        if m.get("name", "").lower() == "viewport" and "width=" in m.get("content", ""):
            return True
    return False


def has_meta_description(parser: SimpleHTML) -> bool:
    for m in parser.meta:
        if m.get("name", "").lower() == "description" and m.get("content"):
            return True
    return False


def external_resources(parser: SimpleHTML) -> Dict[str, List[Dict[str, str]]]:
    css = [l for l in parser.links if l.get("rel", "").lower() in ("stylesheet",) and l.get("href", "").startswith("http")]
    fonts = [l for l in parser.links if "fonts.googleapis.com" in l.get("href", "")]
    preconnects = [l for l in parser.links if l.get("rel", "").lower() == "preconnect"]
    scripts = [s for s in parser.scripts if s.get("src", "").startswith("http")]
    return {"css": css, "scripts": scripts, "fonts": fonts, "preconnects": preconnects}


def has_media_queries(parser: SimpleHTML) -> bool:
    # Search inline <style> blocks for @media
    for style in parser.styles:
        if "@media" in style:
            return True
    return False


def has_reveal_initialize(content: str) -> bool:
    return bool(re.search(r"Reveal\.initialize\s*\(", content))


def anchor_hrefs(content: str) -> List[str]:
    return re.findall(r"<a\s+[^>]*href=\"([^\"]+)\"", content)


def check_file_exists(href: str) -> bool:
    if href.startswith("http"):
        return True
    # relative link in docs dir
    target = os.path.join(DOCS_DIR, href)
    return os.path.exists(target)


def check_sri(attrs: Dict[str, str]) -> bool:
    # Subresource Integrity
    return bool(attrs.get("integrity")) and attrs.get("crossorigin") in ("anonymous", "use-credentials")


def audit_page(filename: str) -> Dict:
    path = os.path.join(DOCS_DIR, filename)
    content = read_file(path)
    parser = parse_html(content)
    ext = external_resources(parser)

    anchors = anchor_hrefs(content)
    local_link_issues = [a for a in anchors if not check_file_exists(a)]

    # Heuristics
    blocking_head_css = [l for l in parser.links if l.get("rel", "").lower() == "stylesheet" and l.get("href")]
    blocking_head_js = [s for s in parser.scripts if s.get("src") and not s.get("defer") and not s.get("async")]

    # SRI check for CDN assets
    cdn_css_missing_sri = [l for l in ext["css"] if not check_sri(l)]
    cdn_js_missing_sri = [s for s in ext["scripts"] if not check_sri(s)]

    # Accessibility heuristics
    zoom_disabled = False
    for m in parser.meta:
        if m.get("name", "").lower() == "viewport":
            c = m.get("content", "").lower()
            if "user-scalable=no" in c or "maximum-scale=1" in c:
                zoom_disabled = True

    return {
        "file": filename,
        "size_bytes": os.path.getsize(path),
        "has_title": bool(parser.titles and parser.titles[0]),
        "title": parser.titles[0] if parser.titles else "",
        "lang_attr": next((attrs.get("lang") for tag, attrs in parser.tags if tag == "html"), None),
        "has_meta_viewport": has_meta_viewport(parser),
        "has_meta_description": has_meta_description(parser),
        "media_queries_present": has_media_queries(parser),
        "anchors_total": len(anchors),
        "broken_local_links": local_link_issues,
        "external_css": ext["css"],
        "external_scripts": ext["scripts"],
        "preconnects": ext["preconnects"],
        "fonts": ext["fonts"],
        "blocking_head_css_count": len(blocking_head_css),
        "blocking_head_js_count": len(blocking_head_js),
        "cdn_css_missing_sri_count": len(cdn_css_missing_sri),
        "cdn_js_missing_sri_count": len(cdn_js_missing_sri),
        "reveal_initialize": has_reveal_initialize(content),
        "speaker_notes_button": "speaker-notes-button" in content,
        "data_patterns": sorted({v for _, d in parser.data_attrs for k, v in d.items() if k == "data-pattern"}),
        "zoom_disabled": zoom_disabled,
    }


def main():
    target_files = [
        "index.html",
        "demo-google-classic.html",
        "demo-google-dark.html",
        "demo-google-minimal.html",
    ]
    report = []
    for f in target_files:
        full = os.path.join(DOCS_DIR, f)
        if not os.path.exists(full):
            print(f"WARN: Missing {f}")
            continue
        report.append(audit_page(f))

    # Print concise text report
    print("AI Slide Generator - Site Audit Summary")
    print("=" * 50)
    for r in report:
        print(f"File: {r['file']} ({r['size_bytes']} bytes)")
        print(f"- Title: {'OK' if r['has_title'] else 'MISSING'} -> {r['title']}")
        print(f"- Lang: {r['lang_attr']}")
        print(f"- Viewport: {'OK' if r['has_meta_viewport'] else 'MISSING'}")
        print(f"- Meta description: {'OK' if r['has_meta_description'] else 'MISSING'}")
        print(f"- Media queries: {'YES' if r['media_queries_present'] else 'NO'}")
        print(f"- External CSS/JS: {len(r['external_css'])}/{len(r['external_scripts'])}")
        print(f"- Preconnects: {len(r['preconnects'])}")
        print(f"- Fonts: {len(r['fonts'])}")
        print(f"- Broken local links: {len(r['broken_local_links'])}")
        if r['broken_local_links']:
            print(f"  -> {r['broken_local_links']}")
        print(f"- CDN CSS/JS missing SRI: {r['cdn_css_missing_sri_count']}/{r['cdn_js_missing_sri_count']}")
        if r['file'].startswith('demo-'):
            print(f"- Reveal.initialize: {'YES' if r['reveal_initialize'] else 'NO'}")
            print(f"- Speaker notes button: {'YES' if r['speaker_notes_button'] else 'NO'}")
            print(f"- Patterns: {', '.join(r['data_patterns']) if r['data_patterns'] else '-'}")
            print(f"- Zoom disabled: {'YES' if r['zoom_disabled'] else 'NO'}")
        print("-")


if __name__ == "__main__":
    main()
