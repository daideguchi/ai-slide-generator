"""
Command Line Interface for AI Slide Generator
"""
import sys
from pathlib import Path
from typing import Optional

import click
from colorama import Fore, Back, Style, init

from .text_parser import TextParser, SlideStructureAnalyzer
from .google_slides_generator import GoogleSlidesGenerator
from .html_slides_generator import HTMLSlidesGenerator
from .enhanced_html_generator import EnhancedHTMLSlidesGenerator
from .auth import setup_google_auth
from config.settings import GOOGLE_SLIDES_TEMPLATES, HTML_THEMES, DEFAULT_OUTPUT_DIR

# Initialize colorama for cross-platform colored terminal text
init(autoreset=True)


def print_success(message: str):
    """Print success message in green"""
    click.echo(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str):
    """Print error message in red"""
    click.echo(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_warning(message: str):
    """Print warning message in yellow"""
    click.echo(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_info(message: str):
    """Print info message in blue"""
    click.echo(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


@click.group()
@click.version_option(version="1.0.0", prog_name="AI Slide Generator")
def cli():
    """
    AI Slide Generator - Create presentations from text files
    
    Generate high-quality slides from text content using Google Slides API
    or HTML/Reveal.js presentations.
    """
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.option('--title', '-t', default="AI Generated Presentation", 
              help='Presentation title')
@click.option('--template', '-T', default="simple", 
              type=click.Choice(list(GOOGLE_SLIDES_TEMPLATES.keys())),
              help='Google Slides template to use')
@click.option('--share', '-s', is_flag=True,
              help='Make presentation publicly viewable')
@click.option('--email', '-e', type=str,
              help='Email address to share presentation with')
@click.option('--output-info', '-o', type=click.Path(),
              help='File to save presentation info (JSON)')
def google(input_file: str, title: str, template: str, share: bool, 
          email: Optional[str], output_info: Optional[str]):
    """Generate Google Slides presentation from text file"""
    
    print_info(f"🚀 Generating Google Slides presentation from {input_file}")
    
    try:
        # Setup authentication
        print_info("🔑 Setting up Google API authentication...")
        auth = setup_google_auth()
        
        if not auth:
            print_error("Authentication failed. Please set up Google API credentials.")
            sys.exit(1)
        
        print_success("Google API authentication successful")
        
        # Parse text file
        print_info("📝 Parsing text file...")
        parser = TextParser()
        slides = parser.parse_file(input_file)
        
        if not slides:
            print_error("No slides could be generated from the input file.")
            sys.exit(1)
        
        print_success(f"Generated {len(slides)} slides")
        
        # Analyze slides
        analysis = SlideStructureAnalyzer.analyze_slides(slides)
        suggestions = SlideStructureAnalyzer.suggest_improvements(slides)
        
        if suggestions:
            print_warning("Suggestions for improvement:")
            for suggestion in suggestions:
                print_warning(f"  • {suggestion}")
        
        # Generate presentation
        print_info("🎨 Creating Google Slides presentation...")
        generator = GoogleSlidesGenerator(auth)
        result = generator.create_presentation(slides, title, template)
        
        print_success("Presentation created successfully!")
        print_info(f"📊 Slides count: {result['slides_count']}")
        print_info(f"🎨 Template: {result['template_used']}")
        print_info(f"🔗 Edit link: {result['edit_link']}")
        print_info(f"👀 View link: {result['web_view_link']}")
        
        # Share if requested
        if share or email:
            print_info("🔗 Setting up sharing...")
            share_result = generator.share_presentation(
                result['presentation_id'], 
                email=email,
                permission_type='writer' if email else 'reader'
            )
            print_success(f"Share link: {share_result['share_link']}")
        
        # Save output info
        if output_info:
            import json
            output_data = {**result, **analysis}
            Path(output_info).write_text(json.dumps(output_data, indent=2))
            print_success(f"Presentation info saved to {output_info}")
        
    except Exception as e:
        print_error(f"Error generating presentation: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.option('--title', '-t', default="AI Generated Presentation",
              help='Presentation title')
@click.option('--theme', '-T', default="black",
              type=click.Choice(list(HTML_THEMES.keys())),
              help='HTML presentation theme')
@click.option('--output', '-o', default="presentation.html",
              type=click.Path(),
              help='Output HTML file path')
@click.option('--open-browser', '-b', is_flag=True,
              help='Open presentation in browser after creation')
def html(input_file: str, title: str, theme: str, output: str, open_browser: bool):
    """Generate HTML presentation using Reveal.js from text file"""
    
    print_info(f"🚀 Generating HTML presentation from {input_file}")
    
    try:
        # Parse text file
        print_info("📝 Parsing text file...")
        parser = TextParser()
        slides = parser.parse_file(input_file)
        
        if not slides:
            print_error("No slides could be generated from the input file.")
            sys.exit(1)
        
        print_success(f"Generated {len(slides)} slides")
        
        # Analyze slides
        analysis = SlideStructureAnalyzer.analyze_slides(slides)
        suggestions = SlideStructureAnalyzer.suggest_improvements(slides)
        
        if suggestions:
            print_warning("Suggestions for improvement:")
            for suggestion in suggestions:
                print_warning(f"  • {suggestion}")
        
        # Generate HTML presentation
        print_info("🎨 Creating HTML presentation...")
        generator = HTMLSlidesGenerator()
        result = generator.create_presentation(slides, title, theme, output)
        
        print_success("HTML presentation created successfully!")
        print_info(f"📊 Slides count: {result['slides_count']}")
        print_info(f"🎨 Theme: {result['theme']}")
        print_info(f"📄 Output file: {result['output_path']}")
        print_info(f"📏 File size: {result['file_size']:,} bytes")
        
        # Open in browser if requested
        if open_browser:
            import webbrowser
            webbrowser.open(f"file://{Path(result['output_path']).absolute()}")
            print_success("Opened presentation in default browser")
        
    except Exception as e:
        print_error(f"Error generating presentation: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
def analyze(input_file: str):
    """Analyze text file and show slide structure preview"""
    
    print_info(f"🔍 Analyzing {input_file}")
    
    try:
        # Parse text file
        parser = TextParser()
        slides = parser.parse_file(input_file)
        
        if not slides:
            print_error("No slides could be generated from the input file.")
            sys.exit(1)
        
        # Show analysis
        analysis = SlideStructureAnalyzer.analyze_slides(slides)
        suggestions = SlideStructureAnalyzer.suggest_improvements(slides)
        
        print_success(f"Analysis complete")
        print(f"\n{Fore.CYAN}📊 SLIDE STRUCTURE ANALYSIS{Style.RESET_ALL}")
        print(f"{'='*50}")
        print(f"Total slides: {analysis['total_slides']}")
        print(f"Average bullet points per slide: {analysis['avg_bullets_per_slide']:.1f}")
        
        print(f"\n{Fore.CYAN}📑 SLIDE TYPES{Style.RESET_ALL}")
        for slide_type, count in analysis['slide_types'].items():
            print(f"  {slide_type}: {count}")
        
        print(f"\n{Fore.CYAN}📋 SLIDE TITLES{Style.RESET_ALL}")
        for i, title in enumerate(analysis['titles'], 1):
            print(f"  {i:2d}. {title[:60]}{'...' if len(title) > 60 else ''}")
        
        if suggestions:
            print(f"\n{Fore.YELLOW}💡 SUGGESTIONS{Style.RESET_ALL}")
            for suggestion in suggestions:
                print_warning(f"  • {suggestion}")
        else:
            print_success("\n✨ Your slide structure looks good!")
        
        # Show detailed slide preview
        print(f"\n{Fore.CYAN}👀 SLIDE PREVIEW{Style.RESET_ALL}")
        print(f"{'='*50}")
        
        for i, slide in enumerate(slides[:5], 1):  # Show first 5 slides
            print(f"\n{Fore.MAGENTA}Slide {i}: {slide.title}{Style.RESET_ALL}")
            print(f"Type: {slide.slide_type}")
            if slide.content:
                for j, content in enumerate(slide.content[:3], 1):  # Show first 3 points
                    print(f"  {j}. {content[:80]}{'...' if len(content) > 80 else ''}")
                if len(slide.content) > 3:
                    print(f"  ... and {len(slide.content) - 3} more points")
        
        if len(slides) > 5:
            print(f"\n... and {len(slides) - 5} more slides")
        
    except Exception as e:
        print_error(f"Error analyzing file: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.option('--title', '-t', default="AI Generated Presentation",
              help='Presentation title')
@click.option('--theme', '-T', default="google_classic",
              type=click.Choice(["google_classic", "google_dark", "google_minimal"]),
              help='Google Material Design theme')
@click.option('--output', '-o', default="enhanced_presentation.html",
              type=click.Path(),
              help='Output HTML file path')
@click.option('--language', '-l', default="ja",
              type=click.Choice(["ja", "en"]),
              help='Presentation language (Japanese or English)')
@click.option('--open-browser', '-b', is_flag=True,
              help='Open presentation in browser after creation')
@click.option('--show-validation', '-v', is_flag=True,
              help='Show slide structure validation results')
def enhanced(input_file: str, title: str, theme: str, output: str, language: str, 
            open_browser: bool, show_validation: bool):
    """Generate enhanced HTML presentation with まじん式 patterns and Google themes"""
    
    print_info(f"🚀 Generating enhanced presentation from {input_file}")
    print_info(f"✨ Using まじん式 pattern design methodology")
    
    try:
        # Parse text file
        print_info("📝 Parsing text file...")
        parser = TextParser()
        slides = parser.parse_file(input_file)
        
        if not slides:
            print_error("No slides could be generated from the input file.")
            sys.exit(1)
        
        print_success(f"Generated {len(slides)} basic slides")
        
        # Generate enhanced presentation
        print_info("🎨 Creating enhanced presentation with Google themes...")
        generator = EnhancedHTMLSlidesGenerator()
        result = generator.create_presentation(slides, title, theme, output, language)
        
        print_success("Enhanced presentation created successfully!")
        print_info(f"📊 Slides count: {result['slides_count']}")
        print_info(f"🎨 Theme: {result['theme']}")
        print_info(f"🌍 Language: {language}")
        print_info(f"📄 Output file: {result['output_path']}")
        print_info(f"📏 File size: {result['file_size']:,} bytes")
        
        # Show pattern distribution
        print_info("🔍 まじん式 Pattern Distribution:")
        pattern_dist = result['pattern_distribution']
        for pattern, count in pattern_dist.items():
            print_info(f"  • {pattern}: {count} slides")
        
        # Show validation results if requested
        if show_validation:
            validation = result['validation_result']
            print_info("✅ Structure Validation:")
            
            if validation['is_valid']:
                print_success("  Slide structure is valid")
            else:
                print_error("  Slide structure has issues")
            
            if validation['warnings']:
                print_warning("  Warnings:")
                for warning in validation['warnings']:
                    print_warning(f"    • {warning}")
            
            if validation['suggestions']:
                print_info("  Suggestions:")
                for suggestion in validation['suggestions']:
                    print_info(f"    • {suggestion}")
        
        # Open in browser if requested
        if open_browser:
            import webbrowser
            webbrowser.open(f"file://{Path(result['output_path']).absolute()}")
            print_success("Opened enhanced presentation in default browser")
        
    except Exception as e:
        print_error(f"Error generating enhanced presentation: {e}")
        import traceback
        print_error(f"Details: {traceback.format_exc()}")
        sys.exit(1)


@cli.command()
def setup():
    """Setup Google API credentials for Google Slides integration"""
    
    print_info("🔧 Setting up Google API credentials")
    print()
    print("To use Google Slides integration, you need to:")
    print()
    print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
    print("2. Create a new project or select an existing one")
    print("3. Enable the following APIs:")
    print("   • Google Slides API")
    print("   • Google Drive API")
    print("4. Create OAuth 2.0 credentials:")
    print("   • Go to 'Credentials' in the left sidebar")
    print("   • Click 'Create Credentials' > 'OAuth client ID'")
    print("   • Choose 'Desktop application'")
    print("   • Download the credentials file")
    print("5. Save the file as 'credentials.json' in this project directory")
    print()
    
    credentials_path = Path("credentials.json")
    if credentials_path.exists():
        print_success("Found credentials.json file")
        
        # Test authentication
        print_info("Testing authentication...")
        try:
            auth = setup_google_auth()
            if auth:
                print_success("Google API authentication test successful!")
                print_info("You can now use 'slide-generator google' command")
            else:
                print_error("Authentication test failed")
        except Exception as e:
            print_error(f"Authentication error: {e}")
    else:
        print_warning("credentials.json not found in current directory")
        print_info("Please complete the setup steps above")


@cli.command()
def templates():
    """List available templates and themes"""
    
    print(f"{Fore.CYAN}📋 AVAILABLE TEMPLATES & THEMES{Style.RESET_ALL}")
    print("="*50)
    
    print(f"\n{Fore.GREEN}🎨 Google Slides Templates:{Style.RESET_ALL}")
    for key, name in GOOGLE_SLIDES_TEMPLATES.items():
        print(f"  {key:12} → {name}")
    
    print(f"\n{Fore.BLUE}🌐 HTML/Reveal.js Themes:{Style.RESET_ALL}")
    for key, name in HTML_THEMES.items():
        print(f"  {key:12} → {name}")
    
    print(f"\n{Fore.MAGENTA}✨ Enhanced Google Material Themes (まじん式):{Style.RESET_ALL}")
    google_themes = {
        "google_classic": "Google Classic - Clean blue and white design",
        "google_dark": "Google Dark - Professional dark theme", 
        "google_minimal": "Google Minimal - Minimalist design with subtle colors"
    }
    for key, name in google_themes.items():
        print(f"  {key:15} → {name}")
    
    print(f"\n{Fore.YELLOW}💡 Usage Examples:{Style.RESET_ALL}")
    print("  slide-generator google input.txt --template modern")
    print("  slide-generator html input.txt --theme night")
    print("  slide-generator enhanced input.txt --theme google_classic --language ja")
    print("  slide-generator enhanced input.txt --theme google_dark --show-validation")


def main():
    """Main entry point for the CLI"""
    cli()


if __name__ == '__main__':
    main()