"""
Test cases for text parser module
"""
import pytest
from pathlib import Path
import tempfile

from slide_generator.text_parser import TextParser, SlideStructure, SlideStructureAnalyzer


class TestSlideStructure:
    """Test SlideStructure class"""
    
    def test_slide_structure_creation(self):
        slide = SlideStructure("Test Title", ["Point 1", "Point 2"])
        assert slide.title == "Test Title"
        assert len(slide.content) == 2
        assert slide.slide_type == "bullet_points"
    
    def test_slide_structure_to_dict(self):
        slide = SlideStructure("Test Title", ["Point 1"], "title")
        result = slide.to_dict()
        
        assert result["title"] == "Test Title"
        assert result["content"] == ["Point 1"]
        assert result["slide_type"] == "title"


class TestTextParser:
    """Test TextParser class"""
    
    def setup_method(self):
        self.parser = TextParser()
    
    def test_parse_simple_text(self):
        # Create temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("""Introduction
- This is a test
- Another point

Main Content
This is some content.
More content here.

Conclusion
- Final point
- Last point""")
            temp_path = f.name
        
        try:
            slides = self.parser.parse_file(temp_path)
            
            assert len(slides) >= 3
            assert any("Introduction" in slide.title for slide in slides)
            assert any("Main Content" in slide.title for slide in slides)
            assert any("Conclusion" in slide.title for slide in slides)
            
        finally:
            Path(temp_path).unlink()
    
    def test_parse_markdown(self):
        # Create temporary markdown file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("""# Main Title

## Section 1
- Bullet point 1
- Bullet point 2

## Section 2
Some paragraph text.

> This is a quote

## Section 3
- Final point""")
            temp_path = f.name
        
        try:
            slides = self.parser.parse_file(temp_path)
            
            assert len(slides) >= 3
            title_slide = slides[0]
            assert title_slide.slide_type == "title"
            
            # Check for quote slide
            quote_slides = [s for s in slides if s.slide_type == "quote"]
            assert len(quote_slides) > 0
            
        finally:
            Path(temp_path).unlink()
    
    def test_title_detection(self):
        test_cases = [
            ("TITLE IN CAPS", True),
            ("Title with colon:", True),
            ("Short title", True),
            ("1. Numbered title", True),
            ("This is a very long line that should not be considered a title because it exceeds the maximum length", False),
            ("- Bullet point", False)
        ]
        
        for text, expected in test_cases:
            result = self.parser._is_title_line(text)
            assert result == expected, f"Failed for: {text}"
    
    def test_clean_title(self):
        test_cases = [
            ("Title with colon:", "Title with colon"),
            ("1. Numbered title", "Numbered title"),
            ("  Whitespace title  ", "Whitespace title"),
            ("Very long title that exceeds the maximum length and should be truncated properly", 
             "Very long title that exceeds the maximum length and should b...")
        ]
        
        for input_title, expected in test_cases:
            result = self.parser._clean_title(input_title)
            assert result == expected, f"Failed for: {input_title}"


class TestSlideStructureAnalyzer:
    """Test SlideStructureAnalyzer class"""
    
    def test_analyze_empty_slides(self):
        analysis = SlideStructureAnalyzer.analyze_slides([])
        assert analysis["total_slides"] == 0
    
    def test_analyze_slides(self):
        slides = [
            SlideStructure("Title", [], "title"),
            SlideStructure("Content 1", ["Point 1", "Point 2"], "bullet_points"),
            SlideStructure("Content 2", ["Point 3"], "bullet_points"),
            SlideStructure("Quote", ["Famous quote"], "quote")
        ]
        
        analysis = SlideStructureAnalyzer.analyze_slides(slides)
        
        assert analysis["total_slides"] == 4
        assert analysis["slide_types"]["title"] == 1
        assert analysis["slide_types"]["bullet_points"] == 2
        assert analysis["slide_types"]["quote"] == 1
        assert analysis["avg_bullets_per_slide"] == 1.0  # (0 + 2 + 1 + 1) / 4
    
    def test_suggest_improvements(self):
        # Test with many slides
        many_slides = [SlideStructure(f"Slide {i}", []) for i in range(25)]
        suggestions = SlideStructureAnalyzer.suggest_improvements(many_slides)
        assert any("reducing content" in suggestion.lower() for suggestion in suggestions)
        
        # Test with many bullet points
        busy_slides = [SlideStructure("Busy", [f"Point {i}" for i in range(10)])]
        suggestions = SlideStructureAnalyzer.suggest_improvements(busy_slides)
        assert any("bullet points" in suggestion.lower() for suggestion in suggestions)
        
        # Test missing title slide
        no_title_slides = [SlideStructure("Content", [], "bullet_points")]
        suggestions = SlideStructureAnalyzer.suggest_improvements(no_title_slides)
        assert any("title slide" in suggestion.lower() for suggestion in suggestions)