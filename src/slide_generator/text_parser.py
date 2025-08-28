"""
Text parsing and slide structure generation module
"""
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

from config.settings import DEFAULT_SETTINGS


class SlideStructure:
    """Represents a single slide structure"""
    
    def __init__(self, title: str, content: List[str], slide_type: str = "bullet_points"):
        self.title = title
        self.content = content
        self.slide_type = slide_type  # "title", "bullet_points", "image", "quote"
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "content": self.content,
            "slide_type": self.slide_type
        }


class TextParser:
    """Parse text files and generate slide structures"""
    
    def __init__(self, settings: Dict[str, Any] = None):
        self.settings = settings or DEFAULT_SETTINGS["parsing"]
        
    def parse_file(self, file_path: str) -> List[SlideStructure]:
        """Parse a text or markdown file into slide structures"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = path.read_text(encoding='utf-8')
        
        if path.suffix.lower() == '.md':
            return self.parse_markdown(content)
        else:
            return self.parse_text(content)
    
    def parse_markdown(self, content: str) -> List[SlideStructure]:
        """Parse markdown content into slide structures"""
        # Convert markdown to HTML for easier parsing
        html = markdown.markdown(content, extensions=['extra'])
        soup = BeautifulSoup(html, 'html.parser')
        
        slides = []
        current_slide = None
        
        # Find all headings and content
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'blockquote']):
            if element.name.startswith('h'):
                # New slide with heading
                if current_slide:
                    slides.append(current_slide)
                
                title = element.get_text().strip()
                current_slide = SlideStructure(title, [])
                
                # Determine slide type based on heading level
                if element.name == 'h1':
                    current_slide.slide_type = "title"
            
            elif element.name in ['p', 'blockquote']:
                if current_slide:
                    text = element.get_text().strip()
                    if text:
                        current_slide.content.append(text)
                        if element.name == 'blockquote':
                            current_slide.slide_type = "quote"
            
            elif element.name in ['ul', 'ol']:
                if current_slide:
                    # Extract list items
                    list_items = [li.get_text().strip() for li in element.find_all('li')]
                    current_slide.content.extend(list_items[:self.settings["max_bullet_points"]])
        
        # Add the last slide
        if current_slide:
            slides.append(current_slide)
        
        return self._clean_slides(slides)
    
    def parse_text(self, content: str) -> List[SlideStructure]:
        """Parse plain text content into slide structures"""
        slides = []
        lines = content.split('\n')
        current_slide = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a title (all caps, or ends with :, or is short)
            if self._is_title_line(line):
                if current_slide:
                    slides.append(current_slide)
                
                title = self._clean_title(line)
                current_slide = SlideStructure(title, [])
            
            elif current_slide:
                # Add as content
                if line.startswith('-') or line.startswith('*') or line.startswith('•'):
                    # Bullet point
                    bullet = line[1:].strip()
                    if len(current_slide.content) < self.settings["max_bullet_points"]:
                        current_slide.content.append(bullet)
                else:
                    # Regular text
                    current_slide.content.append(line)
            
            else:
                # First line without a clear title, make it both title and content
                current_slide = SlideStructure(line[:50] + "..." if len(line) > 50 else line, [line])
        
        # Add the last slide
        if current_slide:
            slides.append(current_slide)
        
        return self._clean_slides(slides)
    
    def _is_title_line(self, line: str) -> bool:
        """Determine if a line should be treated as a slide title"""
        # All uppercase
        if line.isupper() and len(line) > 3:
            return True
        
        # Ends with colon
        if line.endswith(':'):
            return True
        
        # Short line (likely a title)
        if len(line) <= self.settings["max_slide_title_length"] and not line.startswith('-') and not line.startswith('*'):
            return True
        
        # Starts with numbers (1. 2. etc.)
        if re.match(r'^\d+\.?\s+', line):
            return True
        
        return False
    
    def _clean_title(self, title: str) -> str:
        """Clean and format title"""
        # Remove trailing colon
        if title.endswith(':'):
            title = title[:-1]
        
        # Remove leading numbers
        title = re.sub(r'^\d+\.?\s*', '', title)
        
        # Truncate if too long
        if len(title) > self.settings["max_slide_title_length"]:
            title = title[:self.settings["max_slide_title_length"]] + "..."
        
        return title.strip()
    
    def _clean_slides(self, slides: List[SlideStructure]) -> List[SlideStructure]:
        """Clean and optimize slide structures"""
        cleaned_slides = []
        
        for slide in slides:
            # Skip empty slides
            if not slide.title and not slide.content:
                continue
            
            # Ensure title exists
            if not slide.title and slide.content:
                slide.title = slide.content[0][:50] + "..." if len(slide.content[0]) > 50 else slide.content[0]
                slide.content = slide.content[1:]
            
            # Limit bullet points
            if len(slide.content) > self.settings["max_bullet_points"]:
                slide.content = slide.content[:self.settings["max_bullet_points"]]
            
            # Truncate long bullet points
            slide.content = [
                point[:self.settings["max_bullet_point_length"]] + "..." 
                if len(point) > self.settings["max_bullet_point_length"] else point
                for point in slide.content
            ]
            
            cleaned_slides.append(slide)
        
        return cleaned_slides


class SlideStructureAnalyzer:
    """Analyze and optimize slide structures"""
    
    @staticmethod
    def analyze_slides(slides: List[SlideStructure]) -> Dict[str, Any]:
        """Analyze slide structures and return statistics"""
        if not slides:
            return {"total_slides": 0, "slide_types": {}, "avg_bullets_per_slide": 0}
        
        slide_types = {}
        total_bullets = 0
        
        for slide in slides:
            slide_type = slide.slide_type
            slide_types[slide_type] = slide_types.get(slide_type, 0) + 1
            total_bullets += len(slide.content)
        
        return {
            "total_slides": len(slides),
            "slide_types": slide_types,
            "avg_bullets_per_slide": total_bullets / len(slides),
            "titles": [slide.title for slide in slides]
        }
    
    @staticmethod
    def suggest_improvements(slides: List[SlideStructure]) -> List[str]:
        """Suggest improvements for slide structure"""
        suggestions = []
        
        analysis = SlideStructureAnalyzer.analyze_slides(slides)
        
        if analysis["total_slides"] == 0:
            suggestions.append("No slides generated. Please check your input file.")
            return suggestions
        
        if analysis["total_slides"] > 20:
            suggestions.append("Consider reducing content - presentations work better with fewer slides.")
        
        if analysis["avg_bullets_per_slide"] > 7:
            suggestions.append("Consider reducing bullet points per slide for better readability.")
        
        if "title" not in analysis["slide_types"]:
            suggestions.append("Consider adding a title slide at the beginning.")
        
        return suggestions