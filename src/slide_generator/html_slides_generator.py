"""
HTML slides generation module using Reveal.js
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
from jinja2 import Template

from .text_parser import SlideStructure
from config.settings import DEFAULT_SETTINGS, HTML_THEMES


class HTMLSlidesGenerator:
    """Generate HTML presentations using Reveal.js framework"""
    
    def __init__(self):
        self.settings = DEFAULT_SETTINGS["html_slides"]
        self.template_dir = Path(__file__).parent.parent.parent / "templates" / "html_slides"
    
    def create_presentation(self, slides: List[SlideStructure], title: str = "AI Generated Presentation", 
                          theme: str = "black", output_path: str = "presentation.html") -> Dict[str, Any]:
        """Create HTML presentation from slide structures"""
        
        # Generate HTML content
        html_content = self._generate_html(slides, title, theme)
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html_content, encoding='utf-8')
        
        return {
            "output_path": str(output_file.absolute()),
            "title": title,
            "slides_count": len(slides),
            "theme": theme,
            "file_size": output_file.stat().st_size,
            "preview_url": f"file://{output_file.absolute()}"
        }
    
    def _generate_html(self, slides: List[SlideStructure], title: str, theme: str) -> str:
        """Generate complete HTML content"""
        
        # Create slide content
        slides_html = []
        for slide in slides:
            slide_html = self._create_slide_html(slide)
            slides_html.append(slide_html)
        
        # Main template
        template_content = self._get_base_template()
        template = Template(template_content)
        
        return template.render(
            title=title,
            slides=slides_html,
            theme=theme,
            reveal_config=self._get_reveal_config(theme)
        )
    
    def _create_slide_html(self, slide: SlideStructure) -> str:
        """Create HTML for a single slide"""
        
        if slide.slide_type == "title":
            return self._create_title_slide(slide)
        elif slide.slide_type == "bullet_points":
            return self._create_bullet_slide(slide)
        elif slide.slide_type == "quote":
            return self._create_quote_slide(slide)
        else:
            return self._create_content_slide(slide)
    
    def _create_title_slide(self, slide: SlideStructure) -> str:
        """Create title slide HTML"""
        content_html = ""
        if slide.content:
            content_html = f'<h3>{slide.content[0]}</h3>'
        
        return f'''
        <section>
            <h1>{slide.title}</h1>
            {content_html}
        </section>
        '''
    
    def _create_bullet_slide(self, slide: SlideStructure) -> str:
        """Create bullet points slide HTML"""
        bullets_html = ""
        if slide.content:
            bullet_items = '\n'.join(f'<li class="fragment">{point}</li>' for point in slide.content)
            bullets_html = f'<ul>{bullet_items}</ul>'
        
        return f'''
        <section>
            <h2>{slide.title}</h2>
            {bullets_html}
        </section>
        '''
    
    def _create_quote_slide(self, slide: SlideStructure) -> str:
        """Create quote slide HTML"""
        quote_text = slide.content[0] if slide.content else ""
        
        return f'''
        <section>
            <h2>{slide.title}</h2>
            <blockquote class="fragment">
                &quot;{quote_text}&quot;
            </blockquote>
        </section>
        '''
    
    def _create_content_slide(self, slide: SlideStructure) -> str:
        """Create content slide HTML"""
        content_html = ""
        if slide.content:
            paragraphs = '\n'.join(f'<p class="fragment">{paragraph}</p>' for paragraph in slide.content)
            content_html = paragraphs
        
        return f'''
        <section>
            <h2>{slide.title}</h2>
            {content_html}
        </section>
        '''
    
    def _get_base_template(self) -> str:
        """Get the base HTML template"""
        return '''<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ title }}</title>
    
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/theme/{{ theme }}.css" id="theme">
    
    <!-- Theme used for syntax highlighted code -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/highlight/monokai.css">
    
    <style>
        .reveal .slides {
            text-align: left;
        }
        
        .reveal h1, .reveal h2, .reveal h3 {
            text-align: center;
            margin-bottom: 1em;
        }
        
        .reveal ul {
            margin-left: 1em;
        }
        
        .reveal li {
            margin-bottom: 0.5em;
        }
        
        .reveal blockquote {
            text-align: center;
            font-style: italic;
            font-size: 1.2em;
            margin: 1em auto;
            padding: 1em;
            border-left: 4px solid #ccc;
        }
        
        .reveal .progress {
            color: #42affa;
        }
        
        .slide-number {
            color: #42affa !important;
        }
        
        /* Custom animations */
        .reveal .fragment.fade-in-then-out {
            opacity: 0;
            visibility: hidden;
        }
        
        .reveal .fragment.fade-in-then-out.visible {
            opacity: 1;
            visibility: inherit;
        }
        
        .reveal .fragment.fade-in-then-out.current-fragment {
            opacity: 1;
            visibility: inherit;
        }
        
        .reveal .fragment.fade-in-then-out.past {
            opacity: 0;
            visibility: hidden;
        }
    </style>
</head>

<body>
    <div class="reveal">
        <div class="slides">
            {% for slide in slides %}
            {{ slide }}
            {% endfor %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/notes/notes.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/markdown/markdown.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/highlight/highlight.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/math/math.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/search/search.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/zoom/zoom.js"></script>

    <script>
        Reveal.initialize({{ reveal_config|safe }});
    </script>
</body>
</html>'''
    
    def _get_reveal_config(self, theme: str) -> str:
        """Get Reveal.js configuration as JSON string"""
        
        config = {
            "hash": True,
            "controls": self.settings["controls"],
            "progress": self.settings["progress"],
            "center": self.settings["center"],
            "touch": self.settings["touch"],
            "loop": self.settings["loop"],
            "rtl": self.settings["rtl"],
            "transition": self.settings["transition"],
            "transitionSpeed": "default",
            "backgroundTransition": "fade",
            
            # Navigation settings
            "keyboard": True,
            "overview": True,
            "disableLayout": False,
            
            # Fragment settings
            "fragments": True,
            "fragmentInURL": True,
            
            # Slide number settings
            "slideNumber": "c/t",
            "showSlideNumber": "all",
            
            # Plugin configuration
            "plugins": [
                "RevealNotes",
                "RevealMarkdown", 
                "RevealHighlight",
                "RevealMath.KaTeX",
                "RevealSearch",
                "RevealZoom"
            ],
            
            # Math plugin settings
            "math": {
                "mathjax": "https://cdn.jsdelivr.net/gh/mathjax/mathjax@2.7.8/MathJax.js",
                "config": "TeX-AMS_HTML-full",
                "TeX": {
                    "Macros": {
                        "RR": "{\\mathbb R}",
                        "bold": ["{\\bf #1}",1]
                    }
                }
            },
            
            # Search plugin settings
            "search": {
                "matchShortcuts": True,
                "searchResultsTitle": "Search Results",
                "autoSearch": False
            }
        }
        
        # Theme-specific adjustments
        if theme == "black":
            config["transition"] = "slide"
        elif theme == "white":
            config["transition"] = "fade"
        elif theme == "league":
            config["transition"] = "convex"
        elif theme == "night":
            config["transition"] = "concave"
        
        import json
        return json.dumps(config, indent=2)
    
    def get_available_themes(self) -> List[str]:
        """Get list of available themes"""
        return list(HTML_THEMES.keys())
    
    def create_custom_css(self, theme_config: Dict[str, Any], output_path: str) -> str:
        """Create custom CSS file for advanced theming"""
        
        css_content = f'''
/* Custom theme based on {theme_config.get("base_theme", "black")} */

:root {{
    --r-background-color: {theme_config.get("background_color", "#191919")};
    --r-main-font: {theme_config.get("main_font", "Source Sans Pro")};
    --r-main-font-size: {theme_config.get("font_size", "42px")};
    --r-main-color: {theme_config.get("text_color", "#fff")};
    --r-block-margin: {theme_config.get("block_margin", "20px")};
    --r-heading-margin: {theme_config.get("heading_margin", "0 0 20px 0")};
    --r-heading-font: {theme_config.get("heading_font", "Source Sans Pro")};
    --r-heading-color: {theme_config.get("heading_color", "#fff")};
    --r-heading-line-height: {theme_config.get("heading_line_height", "1.2")};
    --r-heading-letter-spacing: {theme_config.get("heading_letter_spacing", "normal")};
    --r-heading-text-transform: {theme_config.get("heading_text_transform", "uppercase")};
    --r-heading-text-shadow: {theme_config.get("heading_text_shadow", "none")};
    --r-heading-font-weight: {theme_config.get("heading_font_weight", "600")};
    --r-heading1-text-shadow: {theme_config.get("heading1_text_shadow", "none")};
    --r-heading1-size: {theme_config.get("heading1_size", "2.5em")};
    --r-heading2-size: {theme_config.get("heading2_size", "1.6em")};
    --r-heading3-size: {theme_config.get("heading3_size", "1.3em")};
    --r-heading4-size: {theme_config.get("heading4_size", "1em")};
    --r-code-font: {theme_config.get("code_font", "monospace")};
    --r-link-color: {theme_config.get("link_color", "#42affa")};
    --r-link-color-hover: {theme_config.get("link_color_hover", "#8dcffc")};
    --r-selection-background-color: {theme_config.get("selection_bg", "rgba(79, 64, 28, 0.99)")};
    --r-selection-color: {theme_config.get("selection_color", "#fff")};
}}

.reveal .progress {{
    color: {theme_config.get("progress_color", "var(--r-link-color)")};
}}

.reveal .controls {{
    color: {theme_config.get("controls_color", "var(--r-link-color)")};
}}
'''
        
        # Write custom CSS file
        css_path = Path(output_path)
        css_path.write_text(css_content, encoding='utf-8')
        
        return str(css_path.absolute())