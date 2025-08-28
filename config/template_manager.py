"""
Template management system for AI Slide Generator
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from .settings import TEMPLATES_DIR, GOOGLE_SLIDES_TEMPLATES, HTML_THEMES


class TemplateManager:
    """Manage presentation templates and themes"""
    
    def __init__(self):
        self.google_templates_dir = TEMPLATES_DIR / "google_slides"
        self.html_templates_dir = TEMPLATES_DIR / "html_slides"
        
        # Ensure template directories exist
        self.google_templates_dir.mkdir(parents=True, exist_ok=True)
        self.html_templates_dir.mkdir(parents=True, exist_ok=True)
    
    def get_google_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get Google Slides template configuration"""
        template_file = self.google_templates_dir / f"{template_id}_template.json"
        
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Return default template if specific one not found
        return self._get_default_google_template(template_id)
    
    def _get_default_google_template(self, template_id: str) -> Dict[str, Any]:
        """Get default template configuration"""
        default_templates = {
            "simple": {
                "template_name": "Simple",
                "background_color": {"red": 1.0, "green": 1.0, "blue": 1.0},
                "title_font": "Arial",
                "body_font": "Arial",
                "title_color": {"red": 0.0, "green": 0.0, "blue": 0.0},
                "body_color": {"red": 0.3, "green": 0.3, "blue": 0.3}
            },
            "modern": {
                "template_name": "Modern",
                "background_color": {"red": 0.95, "green": 0.95, "blue": 0.95},
                "title_font": "Roboto",
                "body_font": "Open Sans",
                "title_color": {"red": 0.2, "green": 0.4, "blue": 0.8},
                "body_color": {"red": 0.3, "green": 0.3, "blue": 0.3}
            },
            "focus": {
                "template_name": "Focus",
                "background_color": {"red": 1.0, "green": 1.0, "blue": 1.0},
                "title_font": "Georgia",
                "body_font": "Georgia",
                "title_color": {"red": 0.1, "green": 0.1, "blue": 0.1},
                "body_color": {"red": 0.4, "green": 0.4, "blue": 0.4}
            }
        }
        
        return default_templates.get(template_id, default_templates["simple"])
    
    def get_html_theme_config(self, theme_id: str) -> Dict[str, Any]:
        """Get HTML theme configuration"""
        theme_configs = {
            "black": {
                "theme_name": "Black",
                "background_color": "#111",
                "text_color": "#fff",
                "heading_color": "#fff",
                "link_color": "#42affa",
                "transition": "slide"
            },
            "white": {
                "theme_name": "White", 
                "background_color": "#fff",
                "text_color": "#222",
                "heading_color": "#222",
                "link_color": "#2a76dd",
                "transition": "fade"
            },
            "league": {
                "theme_name": "League",
                "background_color": "#2b2b2b",
                "text_color": "#eee",
                "heading_color": "#eee",
                "link_color": "#13daec",
                "transition": "convex"
            },
            "night": {
                "theme_name": "Night",
                "background_color": "#111122",
                "text_color": "#eee",
                "heading_color": "#eee",
                "link_color": "#e7ad52",
                "transition": "concave"
            },
            "sky": {
                "theme_name": "Sky",
                "background_color": "#f7fbfc",
                "text_color": "#333",
                "heading_color": "#333",
                "link_color": "#3b759e",
                "transition": "linear"
            }
        }
        
        return theme_configs.get(theme_id, theme_configs["black"])
    
    def save_custom_google_template(self, template_id: str, template_config: Dict[str, Any]):
        """Save custom Google Slides template"""
        template_file = self.google_templates_dir / f"{template_id}_template.json"
        
        with open(template_file, 'w', encoding='utf-8') as f:
            json.dump(template_config, f, indent=2, ensure_ascii=False)
    
    def save_custom_html_theme(self, theme_id: str, css_content: str):
        """Save custom HTML theme CSS"""
        theme_file = self.html_templates_dir / f"{theme_id}_theme.css"
        
        with open(theme_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
    
    def list_available_templates(self) -> Dict[str, List[str]]:
        """List all available templates"""
        google_templates = list(GOOGLE_SLIDES_TEMPLATES.keys())
        
        # Add custom templates
        for template_file in self.google_templates_dir.glob("*_template.json"):
            template_id = template_file.stem.replace("_template", "")
            if template_id not in google_templates:
                google_templates.append(template_id)
        
        html_themes = list(HTML_THEMES.keys())
        
        # Add custom themes
        for theme_file in self.html_templates_dir.glob("*_theme.css"):
            theme_id = theme_file.stem.replace("_theme", "")
            if theme_id not in html_themes:
                html_themes.append(theme_id)
        
        return {
            "google_slides": google_templates,
            "html_themes": html_themes
        }
    
    def validate_template_config(self, template_config: Dict[str, Any]) -> List[str]:
        """Validate template configuration"""
        errors = []
        
        required_fields = ["template_name"]
        for field in required_fields:
            if field not in template_config:
                errors.append(f"Missing required field: {field}")
        
        # Validate color format
        color_fields = ["background_color", "title_color", "body_color"]
        for field in color_fields:
            if field in template_config:
                color = template_config[field]
                if not isinstance(color, dict):
                    errors.append(f"Invalid color format for {field}: must be dict with red, green, blue")
                else:
                    for component in ["red", "green", "blue"]:
                        if component not in color:
                            errors.append(f"Missing {component} component in {field}")
                        elif not 0 <= color[component] <= 1:
                            errors.append(f"Invalid {component} value in {field}: must be between 0 and 1")
        
        return errors
    
    def create_template_from_existing(self, base_template: str, new_template: str, 
                                    modifications: Dict[str, Any]) -> bool:
        """Create new template based on existing one with modifications"""
        try:
            base_config = self.get_google_template(base_template)
            if not base_config:
                return False
            
            # Apply modifications
            new_config = {**base_config, **modifications}
            new_config["template_name"] = new_template.title()
            new_config["template_id"] = new_template
            
            # Validate new configuration
            errors = self.validate_template_config(new_config)
            if errors:
                print(f"Validation errors: {errors}")
                return False
            
            # Save new template
            self.save_custom_google_template(new_template, new_config)
            return True
            
        except Exception as e:
            print(f"Error creating template: {e}")
            return False


class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self):
        self.config_file = Path("slide_generator_config.json")
        self.default_config = {
            "default_google_template": "simple",
            "default_html_theme": "black", 
            "default_output_directory": "output",
            "auto_open_html": False,
            "auto_share_google_slides": False,
            "max_slides_per_presentation": 50,
            "parsing_settings": {
                "max_bullet_points": 7,
                "max_slide_title_length": 60,
                "max_bullet_point_length": 120
            },
            "google_slides_settings": {
                "slide_size": "LARGE_16_9",
                "default_font": "Arial",
                "default_font_size": 14
            },
            "html_settings": {
                "transition": "slide",
                "controls": True,
                "progress": True,
                "center": True
            }
        }
        
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                merged_config = {**self.default_config, **config}
                return merged_config
                
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.default_config
        
        return self.default_config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config_ref = self.config
        
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        config_ref[keys[-1]] = value
        self.save_config()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.default_config.copy()
        self.save_config()


# Global instances
template_manager = TemplateManager()
config_manager = ConfigManager()