#!/usr/bin/env python3
"""
Enhanced HTML Slides Generator - まじん式プロンプト設計統合
Google Material Design + 8パターン + スピーカーノート対応
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from jinja2 import Template

from .text_parser import SlideStructure
from .enhanced_patterns import (
    EnhancedSlideGenerator, EnhancedSlideStructure, SlidePattern,
    InlineStyleParser, SpeakerNotesGenerator
)
from .google_style_themes import GoogleStyleThemes, GoogleColors


class EnhancedHTMLSlidesGenerator:
    """まじん式設計統合HTMLスライドジェネレーター"""
    
    def __init__(self):
        self.enhanced_generator = EnhancedSlideGenerator()
        self.google_themes = GoogleStyleThemes()
        self.notes_generator = SpeakerNotesGenerator()
        self.inline_parser = InlineStyleParser()
    
    def create_presentation(self, slides: List[SlideStructure], title: str = "AI Generated Presentation",
                          theme: str = "google_classic", output_path: str = "presentation.html",
                          language: str = "ja") -> Dict[str, Any]:
        """Enhanced presentation generation with まじん式 patterns"""
        
        # Convert to enhanced slide structures
        enhanced_slides = self.enhanced_generator.enhance_slide_structure(slides)
        
        # Validate and optimize
        validation_result = self.enhanced_generator.validate_and_optimize(enhanced_slides)
        
        # Generate HTML content
        html_content = self._generate_enhanced_html(enhanced_slides, title, theme, language)
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(html_content, encoding='utf-8')
        
        return {
            "output_path": str(output_file.absolute()),
            "title": title,
            "slides_count": len(enhanced_slides),
            "theme": theme,
            "file_size": output_file.stat().st_size,
            "preview_url": f"file://{output_file.absolute()}",
            "validation_result": validation_result,
            "pattern_distribution": self._get_pattern_distribution(enhanced_slides),
            "speaker_notes_included": True
        }
    
    def _generate_enhanced_html(self, slides: List[EnhancedSlideStructure], title: str,
                               theme: str, language: str) -> str:
        """Generate complete enhanced HTML content"""
        
        # Create slide content with patterns
        slides_html = []
        for i, slide in enumerate(slides):
            slide_html = self._create_pattern_slide_html(slide, i+1)
            slides_html.append(slide_html)
        
        # Get Google theme CSS
        all_themes = self.google_themes.get_all_google_themes()
        theme_data = all_themes.get(theme, all_themes['google_classic'])
        theme_css = theme_data['css']
        
        # Base template with enhanced features
        template_content = self._get_enhanced_base_template()
        template = Template(template_content)
        
        return template.render(
            title=title,
            slides=slides_html,
            theme=theme,
            theme_css=theme_css,
            reveal_config=self._get_enhanced_reveal_config(theme, language),
            speaker_notes_enabled=True,
            total_slides=len(slides),
            language=language
        )
    
    def _create_pattern_slide_html(self, slide: EnhancedSlideStructure, slide_number: int) -> str:
        """Create HTML based on slide pattern"""
        
        pattern_methods = {
            SlidePattern.TITLE: self._create_title_pattern_slide,
            SlidePattern.SECTION: self._create_section_pattern_slide,
            SlidePattern.CONTENT: self._create_content_pattern_slide,
            SlidePattern.COMPARE: self._create_compare_pattern_slide,
            SlidePattern.PROCESS: self._create_process_pattern_slide,
            SlidePattern.TIMELINE: self._create_timeline_pattern_slide,
            SlidePattern.DIAGRAM: self._create_diagram_pattern_slide,
            SlidePattern.CARDS: self._create_cards_pattern_slide,
            SlidePattern.TABLE: self._create_table_pattern_slide,
            SlidePattern.PROGRESS: self._create_progress_pattern_slide,
            SlidePattern.CLOSING: self._create_closing_pattern_slide
        }
        
        method = pattern_methods.get(slide.pattern, self._create_content_pattern_slide)
        slide_html = method(slide)
        
        # Add speaker notes
        speaker_notes = ""
        if slide.speaker_notes:
            speaker_notes = f'<aside class="notes">{slide.speaker_notes}</aside>'
        
        return f'''
        <section data-pattern="{slide.pattern.value}" data-slide-number="{slide_number}">
            {slide_html}
            {speaker_notes}
        </section>
        '''
    
    def _create_title_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create title slide with Google styling"""
        title_styled = self._apply_inline_styles(slide.title)
        subhead_html = ""
        if slide.subhead:
            subhead_styled = self._apply_inline_styles(slide.subhead)
            subhead_html = f'<h3 class="google-subhead">{subhead_styled}</h3>'
        
        date_html = ""
        if slide.date:
            date_html = f'<p class="google-date">{slide.date}</p>'
        
        return f'''
        <div class="google-title-slide">
            <h1 class="google-main-title">{title_styled}</h1>
            {subhead_html}
            {date_html}
        </div>
        '''
    
    def _create_section_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create section slide (chapter opener)"""
        title_styled = self._apply_inline_styles(slide.title)
        
        section_number_html = ""
        if slide.section_number:
            section_number_html = f'<div class="google-section-number">{slide.section_number:02d}</div>'
        
        return f'''
        <div class="google-section-slide">
            {section_number_html}
            <h1 class="google-section-title">{title_styled}</h1>
        </div>
        '''
    
    def _create_content_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create content slide with bullet points"""
        title_styled = self._apply_inline_styles(slide.title)
        
        content_html = ""
        if slide.content:
            bullet_items = []
            for i, point in enumerate(slide.content):
                point_styled = self._apply_inline_styles(point)
                bullet_items.append(f'<li class="fragment" data-fragment-index="{i}">{point_styled}</li>')
            
            content_html = f'<ul class="google-bullet-list">{"".join(bullet_items)}</ul>'
        
        return f'''
        <div class="google-content-slide">
            <h2 class="google-slide-title">{title_styled}</h2>
            {content_html}
        </div>
        '''
    
    def _create_compare_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create comparison slide with left/right layout"""
        title_styled = self._apply_inline_styles(slide.title)
        
        compare_html = ""
        if slide.compare_data:
            left_title = slide.compare_data.get('left_title', 'Option A')
            right_title = slide.compare_data.get('right_title', 'Option B')
            left_items = slide.compare_data.get('left_items', [])
            right_items = slide.compare_data.get('right_items', [])
            
            left_content = ""
            if left_items:
                left_bullets = "".join([f'<li class="fragment">{self._apply_inline_styles(item)}</li>' for item in left_items])
                left_content = f'<ul>{left_bullets}</ul>'
            
            right_content = ""
            if right_items:
                right_bullets = "".join([f'<li class="fragment">{self._apply_inline_styles(item)}</li>' for item in right_items])
                right_content = f'<ul>{right_bullets}</ul>'
            
            compare_html = f'''
            <div class="google-compare-container">
                <div class="google-compare-left">
                    <h3 class="google-compare-title">{left_title}</h3>
                    {left_content}
                </div>
                <div class="google-compare-right">
                    <h3 class="google-compare-title">{right_title}</h3>
                    {right_content}
                </div>
            </div>
            '''
        
        return f'''
        <div class="google-compare-slide">
            <h2 class="google-slide-title">{title_styled}</h2>
            {compare_html}
        </div>
        '''
    
    def _create_process_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create process/workflow slide with steps"""
        title_styled = self._apply_inline_styles(slide.title)
        
        process_html = ""
        if slide.process_steps:
            steps_items = []
            for i, step in enumerate(slide.process_steps):
                step_styled = self._apply_inline_styles(step)
                steps_items.append(f'''
                <div class="google-process-step fragment" data-fragment-index="{i}">
                    <div class="google-step-number">{i+1}</div>
                    <div class="google-step-content">{step_styled}</div>
                </div>
                ''')
            
            process_html = f'<div class="google-process-container">{"".join(steps_items)}</div>'
        
        return f'''
        <div class="google-process-slide">
            <h2 class="google-slide-title">{title_styled}</h2>
            {process_html}
        </div>
        '''
    
    def _create_timeline_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create timeline slide"""
        title_styled = self._apply_inline_styles(slide.title)
        
        timeline_html = ""
        if slide.timeline_data:
            timeline_items = []
            for i, item in enumerate(slide.timeline_data):
                label = self._apply_inline_styles(item.get('label', ''))
                date = item.get('date', '')
                state = item.get('state', 'todo')  # todo, in-progress, done
                
                timeline_items.append(f'''
                <div class="google-timeline-item fragment" data-fragment-index="{i}" data-state="{state}">
                    <div class="google-timeline-date">{date}</div>
                    <div class="google-timeline-marker"></div>
                    <div class="google-timeline-content">{label}</div>
                </div>
                ''')
            
            timeline_html = f'<div class="google-timeline-container">{"".join(timeline_items)}</div>'
        
        return f'''
        <div class="google-timeline-slide">
            <h2 class="google-slide-title">{title_styled}</h2>
            {timeline_html}
        </div>
        '''
    
    def _create_diagram_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create diagram slide with lanes and cards"""
        title_styled = self._apply_inline_styles(slide.title)
        
        # For now, create a simple card grid - can be enhanced with actual diagram logic
        return self._create_cards_pattern_slide(slide)
    
    def _create_cards_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create cards grid slide"""
        title_styled = self._apply_inline_styles(slide.title)
        
        cards_html = ""
        if slide.cards_items:
            card_items = []
            for i, card in enumerate(slide.cards_items):
                if isinstance(card, str):
                    card_title = self._apply_inline_styles(card)
                    card_desc = ""
                else:
                    card_title = self._apply_inline_styles(card.get('title', ''))
                    card_desc = f'<p class="google-card-desc">{self._apply_inline_styles(card.get("desc", ""))}</p>' if card.get('desc') else ""
                
                card_items.append(f'''
                <div class="google-card fragment" data-fragment-index="{i}">
                    <h3 class="google-card-title">{card_title}</h3>
                    {card_desc}
                </div>
                ''')
            
            cards_html = f'<div class="google-cards-container">{"".join(card_items)}</div>'
        
        return f'''
        <div class="google-cards-slide">
            <h2 class="google-slide-title">{title_styled}</h2>
            {cards_html}
        </div>
        '''
    
    def _create_table_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create table slide"""
        title_styled = self._apply_inline_styles(slide.title)
        
        # Convert content to simple table format
        table_html = ""
        if slide.content:
            rows = []
            for i, item in enumerate(slide.content):
                item_styled = self._apply_inline_styles(item)
                rows.append(f'<tr class="fragment" data-fragment-index="{i}"><td>{item_styled}</td></tr>')
            
            table_html = f'''
            <table class="google-table">
                <tbody>
                    {"".join(rows)}
                </tbody>
            </table>
            '''
        
        return f'''
        <div class="google-table-slide">
            <h2 class="google-slide-title">{title_styled}</h2>
            {table_html}
        </div>
        '''
    
    def _create_progress_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create progress slide with progress bars"""
        title_styled = self._apply_inline_styles(slide.title)
        
        progress_html = ""
        if slide.progress_items:
            progress_items = []
            for i, item in enumerate(slide.progress_items):
                label = self._apply_inline_styles(item.get('label', ''))
                value = item.get('value', 0)
                max_value = item.get('max', 100)
                percentage = int((value / max_value) * 100) if max_value > 0 else 0
                
                progress_items.append(f'''
                <div class="google-progress-item fragment" data-fragment-index="{i}">
                    <div class="google-progress-label">{label}</div>
                    <div class="google-progress-bar">
                        <div class="google-progress-fill" style="width: {percentage}%"></div>
                    </div>
                    <div class="google-progress-value">{percentage}%</div>
                </div>
                ''')
            
            progress_html = f'<div class="google-progress-container">{"".join(progress_items)}</div>'
        
        return f'''
        <div class="google-progress-slide">
            <h2 class="google-slide-title">{title_styled}</h2>
            {progress_html}
        </div>
        '''
    
    def _create_closing_pattern_slide(self, slide: EnhancedSlideStructure) -> str:
        """Create closing slide"""
        title_styled = self._apply_inline_styles(slide.title)
        
        content_html = ""
        if slide.content:
            content_items = []
            for item in slide.content:
                content_styled = self._apply_inline_styles(item)
                content_items.append(f'<p class="google-closing-text fragment">{content_styled}</p>')
            
            content_html = f'<div class="google-closing-content">{"".join(content_items)}</div>'
        
        return f'''
        <div class="google-closing-slide">
            <h1 class="google-closing-title">{title_styled}</h1>
            {content_html}
        </div>
        '''
    
    def _apply_inline_styles(self, text: str) -> str:
        """Apply inline styling markup (**bold**, [[important]])"""
        parsed = self.inline_parser.parse_styled_text(text)
        clean_text = parsed["clean_text"]
        styles = parsed["styles"]
        
        if not styles:
            return clean_text
        
        # Apply styles by wrapping with spans
        result = ""
        last_end = 0
        
        for style in sorted(styles, key=lambda s: s["start"]):
            # Add text before this style
            result += clean_text[last_end:style["start"]]
            
            # Apply style
            style_classes = []
            style_attrs = []
            
            if style.get("bold"):
                style_classes.append("google-bold")
            
            if style.get("color"):
                style_attrs.append(f'color: {style["color"]}')
            
            class_attr = f' class="{" ".join(style_classes)}"' if style_classes else ""
            style_attr = f' style="{"; ".join(style_attrs)}"' if style_attrs else ""
            
            styled_text = clean_text[style["start"]:style["end"]]
            result += f'<span{class_attr}{style_attr}>{styled_text}</span>'
            
            last_end = style["end"]
        
        # Add remaining text
        result += clean_text[last_end:]
        
        return result
    
    def _get_enhanced_base_template(self) -> str:
        """Get enhanced base HTML template with Google themes"""
        return '''<!doctype html>
<html lang="{{ language }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ title }}</title>
    
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/reveal.css">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;1,400&family=Google+Sans:wght@400;500;700&display=swap" rel="stylesheet">
    
    <!-- Google Material Icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    
    <style>
        {{ theme_css|safe }}
        
        /* まじん式 Enhanced Patterns Styles */
        .google-bold {
            font-weight: 700;
            color: var(--google-primary-blue);
        }
        
        /* Speaker Notes Button */
        .speaker-notes-button {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background: var(--google-primary-blue);
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .speaker-notes-button:hover {
            background: var(--google-blue-dark);
        }
        
        /* Pattern indicators */
        [data-pattern="title"] {
            background: linear-gradient(135deg, var(--google-primary-blue), var(--google-blue-light));
            color: white;
        }
        
        [data-pattern="section"] {
            background: var(--google-grey-50);
            border-left: 8px solid var(--google-primary-blue);
        }
        
        [data-pattern="compare"] .google-compare-container {
            position: relative;
        }
        
        [data-pattern="compare"] .google-compare-container::after {
            content: "VS";
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--google-primary-blue);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.8em;
        }
    </style>
</head>

<body>
    <!-- Speaker Notes Button -->
    {% if speaker_notes_enabled %}
    <button class="speaker-notes-button" onclick="RevealNotes.open()" title="スピーカーノートを開く">
        <span class="material-icons">notes</span>
    </button>
    {% endif %}

    <div class="reveal">
        <div class="slides">
            {% for slide in slides %}
            {{ slide|safe }}
            {% endfor %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/notes/notes.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/markdown/markdown.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.6.1/plugin/highlight/highlight.js"></script>

    <script>
        // Enhanced Reveal.js configuration
        Reveal.initialize({{ reveal_config|safe }});
        
        // Pattern-specific animations
        Reveal.on('slidechanged', event => {
            const currentSlide = event.currentSlide;
            const pattern = currentSlide.dataset.pattern;
            
            // Add pattern-specific animations or behaviors
            if (pattern === 'timeline') {
                // Animate timeline items sequentially
                const timelineItems = currentSlide.querySelectorAll('.google-timeline-item');
                timelineItems.forEach((item, index) => {
                    setTimeout(() => {
                        item.style.animationDelay = `${index * 0.2}s`;
                    }, 100);
                });
            }
            
            if (pattern === 'progress') {
                // Animate progress bars
                const progressBars = currentSlide.querySelectorAll('.google-progress-fill');
                progressBars.forEach((bar, index) => {
                    setTimeout(() => {
                        bar.style.transition = 'width 1s ease-out';
                    }, 500 + index * 200);
                });
            }
        });
    </script>
</body>
</html>'''
    
    def _get_enhanced_reveal_config(self, theme: str, language: str) -> str:
        """Get enhanced Reveal.js configuration"""
        config = {
            "hash": True,
            "controls": True,
            "progress": True,
            "center": True,
            "touch": True,
            "loop": False,
            "rtl": False,
            "transition": "slide",
            "transitionSpeed": "default",
            "backgroundTransition": "fade",
            
            # Enhanced navigation
            "keyboard": True,
            "overview": True,
            "disableLayout": False,
            "slideNumber": "c/t",
            "showSlideNumber": "all",
            
            # Fragment settings for まじん式 patterns
            "fragments": True,
            "fragmentInURL": True,
            
            # Plugin configuration
            "plugins": [
                "RevealNotes",
                "RevealMarkdown",
                "RevealHighlight"
            ],
            
            # まじん式 specific settings
            "viewDistance": 3,
            "mobileViewDistance": 2,
            "parallaxBackgroundImage": "",
            "parallaxBackgroundSize": "",
            "parallaxBackgroundHorizontal": 0,
            "parallaxBackgroundVertical": 0
        }
        
        import json
        return json.dumps(config, indent=2)
    
    def _get_pattern_distribution(self, slides: List[EnhancedSlideStructure]) -> Dict[str, int]:
        """Get distribution of slide patterns used"""
        distribution = {}
        for slide in slides:
            pattern = slide.pattern.value
            distribution[pattern] = distribution.get(pattern, 0) + 1
        
        return distribution
    
    def get_available_google_themes(self) -> List[str]:
        """Get list of available Google themes"""
        all_themes = self.google_themes.get_all_google_themes()
        return list(all_themes.keys())