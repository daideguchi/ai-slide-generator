"""
Test cases for HTML slides generator module
"""
import pytest
from pathlib import Path
import tempfile

from slide_generator.html_slides_generator import HTMLSlidesGenerator
from slide_generator.text_parser import SlideStructure


class TestHTMLSlidesGenerator:
    """Test HTMLSlidesGenerator class"""
    
    def setup_method(self):
        self.generator = HTMLSlidesGenerator()
        self.sample_slides = [
            SlideStructure("Introduction", ["Welcome", "Overview"], "title"),
            SlideStructure("Main Points", ["Point 1", "Point 2", "Point 3"], "bullet_points"),
            SlideStructure("Quote", ["Life is what happens when you're busy making other plans"], "quote"),
            SlideStructure("Conclusion", ["Thank you", "Questions?"], "bullet_points")
        ]
    
    def test_create_presentation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_presentation.html"
            
            result = self.generator.create_presentation(
                self.sample_slides,
                title="Test Presentation",
                theme="black",
                output_path=str(output_path)
            )
            
            assert result["title"] == "Test Presentation"
            assert result["slides_count"] == 4
            assert result["theme"] == "black"
            assert Path(result["output_path"]).exists()
            
            # Verify HTML content
            html_content = Path(result["output_path"]).read_text()
            assert "<title>Test Presentation</title>" in html_content
            assert "reveal.js" in html_content
            assert "Introduction" in html_content
            assert "Main Points" in html_content
    
    def test_create_title_slide(self):
        slide = SlideStructure("Welcome", ["Subtitle here"], "title")
        html = self.generator._create_title_slide(slide)
        
        assert "<h1>Welcome</h1>" in html
        assert "<h3>Subtitle here</h3>" in html
        assert "<section>" in html
    
    def test_create_bullet_slide(self):
        slide = SlideStructure("Main Points", ["Point 1", "Point 2"], "bullet_points")
        html = self.generator._create_bullet_slide(slide)
        
        assert "<h2>Main Points</h2>" in html
        assert "<ul>" in html
        assert "<li class=\"fragment\">Point 1</li>" in html
        assert "<li class=\"fragment\">Point 2</li>" in html
    
    def test_create_quote_slide(self):
        slide = SlideStructure("Famous Quote", ["To be or not to be"], "quote")
        html = self.generator._create_quote_slide(slide)
        
        assert "<h2>Famous Quote</h2>" in html
        assert "<blockquote" in html
        assert "&quot;To be or not to be&quot;" in html
    
    def test_get_reveal_config(self):
        config_json = self.generator._get_reveal_config("black")
        
        # Should be valid JSON
        import json
        config = json.loads(config_json)
        
        assert "hash" in config
        assert "controls" in config
        assert "progress" in config
        assert "plugins" in config
        assert config["transition"] == "slide"  # Default for black theme
    
    def test_get_available_themes(self):
        themes = self.generator.get_available_themes()
        
        assert isinstance(themes, list)
        assert "black" in themes
        assert "white" in themes
        assert "night" in themes
    
    def test_create_custom_css(self):
        theme_config = {
            "base_theme": "custom",
            "background_color": "#ff0000",
            "text_color": "#ffffff", 
            "heading_color": "#00ff00",
            "link_color": "#0000ff"
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            css_path = Path(temp_dir) / "custom.css"
            result = self.generator.create_custom_css(theme_config, str(css_path))
            
            assert Path(result).exists()
            css_content = Path(result).read_text()
            assert "--r-background-color: #ff0000;" in css_content
            assert "--r-main-color: #ffffff;" in css_content