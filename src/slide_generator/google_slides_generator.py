"""
Google Slides generation module
"""
import json
from typing import List, Dict, Any, Optional
from googleapiclient.errors import HttpError

from .auth import GoogleAPIAuth
from .text_parser import SlideStructure
from config.settings import DEFAULT_SETTINGS, GOOGLE_SLIDES_TEMPLATES


class GoogleSlidesGenerator:
    """Generate Google Slides presentations from slide structures"""
    
    def __init__(self, auth: GoogleAPIAuth):
        self.auth = auth
        self.slides_service = auth.get_slides_service()
        self.drive_service = auth.get_drive_service()
        self.settings = DEFAULT_SETTINGS["google_slides"]
    
    def create_presentation(self, slides: List[SlideStructure], title: str = "AI Generated Presentation", template: str = "simple") -> Dict[str, Any]:
        """Create a new Google Slides presentation"""
        try:
            # Create presentation
            presentation = self.slides_service.presentations().create(body={
                'title': title
            }).execute()
            
            presentation_id = presentation['presentationId']
            print(f"Created presentation with ID: {presentation_id}")
            
            # Apply template if requested
            if template != "simple":
                self._apply_template(presentation_id, template)
            
            # Clear default slide and add our slides
            self._clear_default_slides(presentation_id)
            self._add_slides(presentation_id, slides)
            
            # Get final presentation info
            final_presentation = self.slides_service.presentations().get(
                presentationId=presentation_id
            ).execute()
            
            # Get shareable link
            drive_file = self.drive_service.files().get(
                fileId=presentation_id,
                fields="webViewLink,webContentLink"
            ).execute()
            
            return {
                "presentation_id": presentation_id,
                "title": title,
                "slides_count": len(slides),
                "web_view_link": drive_file.get('webViewLink'),
                "edit_link": f"https://docs.google.com/presentation/d/{presentation_id}/edit",
                "export_link": drive_file.get('webContentLink'),
                "template_used": template
            }
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            raise
    
    def _apply_template(self, presentation_id: str, template: str):
        """Apply a template to the presentation"""
        # Note: Google Slides API doesn't directly support templates
        # This is a placeholder for template application logic
        template_styles = self._get_template_styles(template)
        
        if template_styles:
            # Apply master slide styling
            requests = [
                {
                    'updateSlidesPosition': {
                        'slideObjectIds': [],
                        'insertionIndex': 0
                    }
                }
            ]
            
            try:
                self.slides_service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': requests}
                ).execute()
            except HttpError as error:
                print(f'Template application error: {error}')
    
    def _get_template_styles(self, template: str) -> Dict[str, Any]:
        """Get styling configuration for templates"""
        templates = {
            "modern": {
                "background_color": {"red": 0.95, "green": 0.95, "blue": 0.95},
                "title_font": "Roboto",
                "body_font": "Open Sans",
                "primary_color": {"red": 0.2, "green": 0.4, "blue": 0.8}
            },
            "focus": {
                "background_color": {"red": 1.0, "green": 1.0, "blue": 1.0},
                "title_font": "Georgia",
                "body_font": "Arial",
                "primary_color": {"red": 0.1, "green": 0.1, "blue": 0.1}
            },
            "geometric": {
                "background_color": {"red": 0.1, "green": 0.1, "blue": 0.1},
                "title_font": "Montserrat",
                "body_font": "Source Sans Pro",
                "primary_color": {"red": 0.0, "green": 0.8, "blue": 0.4}
            }
        }
        
        return templates.get(template, {})
    
    def _clear_default_slides(self, presentation_id: str):
        """Remove the default slide from the presentation"""
        try:
            presentation = self.slides_service.presentations().get(
                presentationId=presentation_id
            ).execute()
            
            slides = presentation.get('slides', [])
            if slides:
                # Delete the first (default) slide
                requests = [{
                    'deleteObject': {
                        'objectId': slides[0]['objectId']
                    }
                }]
                
                self.slides_service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': requests}
                ).execute()
        except HttpError as error:
            print(f'Error clearing default slides: {error}')
    
    def _add_slides(self, presentation_id: str, slides: List[SlideStructure]):
        """Add slides to the presentation"""
        requests = []
        
        for i, slide_structure in enumerate(slides):
            slide_id = f'slide_{i}'
            
            # Create slide
            requests.append({
                'createSlide': {
                    'objectId': slide_id,
                    'insertionIndex': i,
                    'slideLayoutReference': {
                        'predefinedLayout': self._get_slide_layout(slide_structure.slide_type)
                    }
                }
            })
        
        # Execute slide creation
        try:
            self.slides_service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': requests}
            ).execute()
            
            # Add content to slides
            self._add_content_to_slides(presentation_id, slides)
            
        except HttpError as error:
            print(f'Error adding slides: {error}')
            raise
    
    def _get_slide_layout(self, slide_type: str) -> str:
        """Get appropriate slide layout for slide type"""
        layouts = {
            "title": "TITLE_AND_BODY",
            "bullet_points": "TITLE_AND_BODY",
            "quote": "TITLE_AND_BODY",
            "image": "TITLE_AND_BODY"
        }
        return layouts.get(slide_type, "TITLE_AND_BODY")
    
    def _add_content_to_slides(self, presentation_id: str, slides: List[SlideStructure]):
        """Add text content to slides"""
        presentation = self.slides_service.presentations().get(
            presentationId=presentation_id
        ).execute()
        
        slides_data = presentation.get('slides', [])
        
        for i, (slide_structure, slide_data) in enumerate(zip(slides, slides_data)):
            slide_id = slide_data['objectId']
            
            # Find text elements in the slide
            requests = []
            text_elements = self._find_text_elements(slide_data)
            
            if text_elements:
                title_element = text_elements[0] if text_elements else None
                body_element = text_elements[1] if len(text_elements) > 1 else None
                
                # Add title
                if title_element and slide_structure.title:
                    requests.append({
                        'insertText': {
                            'objectId': title_element['objectId'],
                            'insertionIndex': 0,
                            'text': slide_structure.title
                        }
                    })
                
                # Add content
                if body_element and slide_structure.content:
                    content_text = self._format_content(slide_structure)
                    requests.append({
                        'insertText': {
                            'objectId': body_element['objectId'],
                            'insertionIndex': 0,
                            'text': content_text
                        }
                    })
                
                # Apply formatting
                self._add_formatting_requests(requests, slide_structure, title_element, body_element)
            
            # Execute content addition for this slide
            if requests:
                try:
                    self.slides_service.presentations().batchUpdate(
                        presentationId=presentation_id,
                        body={'requests': requests}
                    ).execute()
                except HttpError as error:
                    print(f'Error adding content to slide {i}: {error}')
    
    def _find_text_elements(self, slide_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find text elements in a slide"""
        text_elements = []
        
        for element in slide_data.get('pageElements', []):
            if 'shape' in element and 'text' in element['shape']:
                text_elements.append(element)
        
        return text_elements
    
    def _format_content(self, slide_structure: SlideStructure) -> str:
        """Format slide content based on slide type"""
        if slide_structure.slide_type == "bullet_points":
            return '\n'.join(f'• {point}' for point in slide_structure.content)
        elif slide_structure.slide_type == "quote":
            return f'"{slide_structure.content[0]}"' if slide_structure.content else ""
        else:
            return '\n\n'.join(slide_structure.content)
    
    def _add_formatting_requests(self, requests: List[Dict], slide_structure: SlideStructure, 
                                title_element: Dict, body_element: Dict):
        """Add text formatting requests"""
        # Title formatting
        if title_element:
            requests.append({
                'updateTextStyle': {
                    'objectId': title_element['objectId'],
                    'style': {
                        'bold': True,
                        'fontSize': {
                            'magnitude': 24,
                            'unit': 'PT'
                        }
                    },
                    'fields': 'bold,fontSize'
                }
            })
        
        # Body formatting
        if body_element:
            font_size = 16 if slide_structure.slide_type == "quote" else 14
            requests.append({
                'updateTextStyle': {
                    'objectId': body_element['objectId'],
                    'style': {
                        'fontSize': {
                            'magnitude': font_size,
                            'unit': 'PT'
                        }
                    },
                    'fields': 'fontSize'
                }
            })
    
    def share_presentation(self, presentation_id: str, email: str = None, 
                          permission_type: str = "reader") -> Dict[str, Any]:
        """Share the presentation"""
        try:
            permission = {
                'type': 'anyone',
                'role': permission_type
            }
            
            if email:
                permission['type'] = 'user'
                permission['emailAddress'] = email
            
            result = self.drive_service.permissions().create(
                fileId=presentation_id,
                body=permission
            ).execute()
            
            return {
                "permission_id": result['id'],
                "share_link": f"https://docs.google.com/presentation/d/{presentation_id}/edit?usp=sharing"
            }
            
        except HttpError as error:
            print(f'Error sharing presentation: {error}')
            raise