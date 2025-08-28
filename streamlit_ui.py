#!/usr/bin/env python3
"""
AI Slide Generator - Streamlit UI
A user-friendly web interface for generating presentations from text files.
"""

import streamlit as st
import sys
import tempfile
import os
from pathlib import Path
from typing import List, Dict, Any
import io
import base64

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from slide_generator.text_parser import TextParser, SlideStructure, SlideStructureAnalyzer
from slide_generator.html_slides_generator import HTMLSlidesGenerator
from slide_generator.enhanced_html_generator import EnhancedHTMLSlidesGenerator
from config.settings import HTML_THEMES, DEFAULT_SETTINGS

# Language dictionary for multilingual support
LANGUAGES = {
    "English": {
        "page_title": "AI Slide Generator",
        "main_title": "🎯 AI Slide Generator",
        "main_subtitle": "**Transform text files into professional presentations instantly!**",
        "settings": "⚙️ Settings",
        "language": "🌐 Language",
        "choose_theme": "🎨 Choose Theme",
        "theme_help": "Select the visual theme for your presentation",
        "presentation_title": "📝 Presentation Title",
        "title_help": "Enter the title for your presentation",
        "advanced_settings": "🔧 Advanced Settings",
        "auto_open": "🚀 Auto-open in browser",
        "auto_open_help": "Automatically open the generated presentation",
        "show_suggestions": "💡 Show improvement suggestions",
        "show_suggestions_help": "Display AI suggestions for better presentation structure",
        "file_upload_title": "📁 File Upload",
        "file_upload_label": "Choose a text or markdown file",
        "file_upload_help": "Upload a .txt or .md file to generate slides",
        "sample_files": "**🎪 Try with sample files:**",
        "file_content": "File Content",
        "english_sample": "📊 English Sample",
        "japanese_sample": "🗾 Japanese Sample",
        "file_loaded": "✅ File loaded: **{}**",
        "content_length": "📊 Content length: {:,} characters",
        "preview_content": "👀 Preview file content",
        "slide_generation_title": "🎯 Slide Generation",
        "analyzing_content": "🔍 Analyzing content...",
        "generated_slides": "🎉 Generated **{} slides**",
        "total_slides": "📊 Total Slides",
        "avg_bullets": "📋 Avg Bullets",
        "slide_types": "🎭 Slide Types",
        "suggestions_title": "💡 **Suggestions for improvement:**",
        "preview_structure": "👀 Slide Structure Preview",
        "slide_n": "**Slide {}: {}**",
        "slide_type": "Type: {}",
        "more_points": "  ... and {} more points",
        "more_slides": "... and {} more slides",
        "generation_mode": "🎨 Generation Mode",
        "mode_help": "Choose between standard HTML or enhanced まじん式 presentation",
        "standard_mode": "📊 Standard HTML",
        "enhanced_mode": "✨ Enhanced (まじん式)",
        "google_theme": "🎨 Google Material Theme",
        "google_theme_help": "Select a Google Material Design theme for enhanced presentations",
        "show_validation": "🔍 Show validation results",
        "validation_help": "Display slide structure validation and pattern analysis",
        "speaker_notes": "🎤 Include speaker notes",
        "speaker_notes_help": "Generate automatic speaker notes for presentation",
        "generate_button": "🚀 Generate HTML Presentation",
        "enhanced_button": "✨ Generate Enhanced Presentation",
        "creating": "🎨 Creating presentation...",
        "creating_enhanced": "✨ Creating enhanced presentation with まじん式 patterns...",
        "success": "🎉 Presentation generated successfully!",
        "enhanced_success": "✨ Enhanced presentation with まじん式 patterns created successfully!",
        "slides_created": "📊 Slides Created",
        "theme": "🎨 Theme",
        "file_size": "📏 File Size",
        "download_button": "💾 Download Presentation",
        "preview_button": "👀 Preview in Browser",
        "opened_browser": "🚀 Opened in browser!",
        "error_generating": "❌ Error generating presentation: {}",
        "upload_instruction": "👆 Please upload a file or select a sample to get started!",
        "quick_guide": "📚 Quick Start Guide",
        "how_to_use": """**How to use this tool:**
                
1. **📁 Upload** a text (.txt) or markdown (.md) file
2. **⚙️ Configure** settings in the sidebar
3. **👀 Preview** the slide structure 
4. **🚀 Generate** your presentation
5. **💾 Download** the HTML file

**Supported formats:**
- Plain text files with natural structure
- Markdown files with headers and bullet points
- Both English and Japanese content

**Features:**
- 🎨 Multiple themes (Night, Black, White, etc.)
- 📊 Smart content analysis
- 💡 AI improvement suggestions
- 🚀 One-click generation
- 💾 Instant download"""
    },
    "日本語": {
        "page_title": "AI スライド生成ツール",
        "main_title": "🎯 AI スライド生成ツール",
        "main_subtitle": "**テキストファイルから瞬時にプロフェッショナルなプレゼンテーションを作成！**",
        "settings": "⚙️ 設定",
        "language": "🌐 言語",
        "choose_theme": "🎨 テーマを選択",
        "theme_help": "プレゼンテーションの外観テーマを選択してください",
        "presentation_title": "📝 プレゼンテーションタイトル",
        "title_help": "プレゼンテーションのタイトルを入力してください",
        "advanced_settings": "🔧 詳細設定",
        "auto_open": "🚀 ブラウザで自動オープン",
        "auto_open_help": "生成されたプレゼンテーションを自動的に開く",
        "show_suggestions": "💡 改善提案を表示",
        "show_suggestions_help": "より良いプレゼンテーション構造のためのAI提案を表示する",
        "file_upload_title": "📁 ファイルアップロード",
        "file_upload_label": "テキストまたはマークダウンファイルを選択",
        "file_upload_help": "スライドを生成するために .txt または .md ファイルをアップロードしてください",
        "sample_files": "**🎪 サンプルファイルで試す:**",
        "file_content": "ファイル内容",
        "english_sample": "📊 英語サンプル",
        "japanese_sample": "🗾 日本語サンプル",
        "file_loaded": "✅ ファイル読み込み完了: **{}**",
        "content_length": "📊 コンテンツ長: {:,} 文字",
        "preview_content": "👀 ファイル内容をプレビュー",
        "slide_generation_title": "🎯 スライド生成",
        "analyzing_content": "🔍 コンテンツを解析中...",
        "generated_slides": "🎉 **{}枚のスライド**を生成しました",
        "total_slides": "📊 総スライド数",
        "avg_bullets": "📋 平均箇条書き",
        "slide_types": "🎭 スライドタイプ",
        "suggestions_title": "💡 **改善提案:**",
        "preview_structure": "👀 スライド構造プレビュー",
        "slide_n": "**スライド {}: {}**",
        "slide_type": "タイプ: {}",
        "more_points": "  ... 他 {} 個のポイント",
        "more_slides": "... 他 {} 枚のスライド",
        "generation_mode": "🎨 生成モード",
        "mode_help": "標準HTMLまたはまじん式拡張プレゼンテーションから選択",
        "standard_mode": "📊 標準HTML",
        "enhanced_mode": "✨ 拡張 (まじん式)",
        "google_theme": "🎨 Google Materialテーマ",
        "google_theme_help": "拡張プレゼンテーション用のGoogle Material Designテーマを選択",
        "show_validation": "🔍 検証結果を表示",
        "validation_help": "スライド構造の検証とパターン解析を表示",
        "speaker_notes": "🎤 スピーカーノートを含める",
        "speaker_notes_help": "プレゼンテーション用の自動スピーカーノートを生成",
        "generate_button": "🚀 HTMLプレゼンテーション生成",
        "enhanced_button": "✨ 拡張プレゼンテーション生成",
        "creating": "🎨 プレゼンテーション作成中...",
        "creating_enhanced": "✨ まじん式パターンで拡張プレゼンテーション作成中...",
        "success": "🎉 プレゼンテーション生成成功！",
        "enhanced_success": "✨ まじん式パターンの拡張プレゼンテーション作成成功！",
        "slides_created": "📊 作成スライド数",
        "theme": "🎨 テーマ",
        "file_size": "📏 ファイルサイズ",
        "download_button": "💾 プレゼンテーションをダウンロード",
        "preview_button": "👀 ブラウザでプレビュー",
        "opened_browser": "🚀 ブラウザで開きました！",
        "error_generating": "❌ プレゼンテーション生成エラー: {}",
        "upload_instruction": "👆 開始するにはファイルをアップロードするか、サンプルを選択してください！",
        "quick_guide": "📚 クイックスタートガイド",
        "how_to_use": """**このツールの使い方:**

1. **📁 アップロード** テキスト (.txt) またはマークダウン (.md) ファイルを選択
2. **⚙️ 設定** サイドバーで設定を調整
3. **👀 プレビュー** スライド構造を確認
4. **🚀 生成** プレゼンテーションを作成
5. **💾 ダウンロード** HTMLファイルを保存

**対応フォーマット:**
- 自然な構造を持つプレーンテキストファイル
- ヘッダーと箇条書きを含むマークダウンファイル
- 日本語・英語コンテンツ両対応

**機能:**
- 🎨 複数テーマ (Night, Black, White など)
- 📊 スマートコンテンツ解析
- 💡 AI改善提案
- 🚀 ワンクリック生成
- 💾 即座ダウンロード"""
    }
}

# Page configuration
st.set_page_config(
    page_title="AI Slide Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Note: Page title cannot be changed dynamically in Streamlit
# It's set once at app startup and remains static throughout the session

def main():
    """Main Streamlit application"""
    
    # Initialize session state for language
    if 'language' not in st.session_state:
        st.session_state.language = 'English'
    
    # Get current language texts
    texts = LANGUAGES[st.session_state.language]
    
    # Header
    st.title(texts["main_title"])
    st.markdown(texts["main_subtitle"])
    
    # Sidebar for settings
    with st.sidebar:
        st.header(texts["settings"])
        
        # Language selection
        language_options = list(LANGUAGES.keys())
        selected_language = st.selectbox(
            texts["language"],
            options=language_options,
            index=language_options.index(st.session_state.language),
            help="Select your preferred language / 言語を選択してください"
        )
        
        # Update session state if language changed
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            st.rerun()
        
        # Generation mode selection
        generation_mode = st.radio(
            texts["generation_mode"],
            options=[texts["standard_mode"], texts["enhanced_mode"]],
            index=0,
            help=texts["mode_help"]
        )
        
        is_enhanced_mode = generation_mode == texts["enhanced_mode"]
        
        # Theme selection - different for enhanced vs standard
        if is_enhanced_mode:
            # Google Material Design themes
            google_theme_options = ["google_classic", "google_dark", "google_minimal"]
            google_theme_names = {
                "google_classic": "🔵 Google Classic",
                "google_dark": "🔴 Google Dark", 
                "google_minimal": "⚪ Google Minimal"
            }
            selected_theme = st.selectbox(
                texts["google_theme"],
                options=google_theme_options,
                format_func=lambda x: google_theme_names[x],
                index=0,
                help=texts["google_theme_help"]
            )
        else:
            # Standard HTML themes
            theme_options = list(HTML_THEMES.keys())
            selected_theme = st.selectbox(
                texts["choose_theme"],
                options=theme_options,
                index=theme_options.index("night"),
                help=texts["theme_help"]
            )
        
        # Title input
        presentation_title = st.text_input(
            texts["presentation_title"], 
            value="AI Generated Presentation" if st.session_state.language == 'English' else "AI生成プレゼンテーション",
            help=texts["title_help"]
        )
        
        # Advanced settings
        with st.expander(texts["advanced_settings"]):
            auto_open = st.checkbox(
                texts["auto_open"], 
                value=False,
                help=texts["auto_open_help"]
            )
            show_suggestions = st.checkbox(
                texts["show_suggestions"], 
                value=True,
                help=texts["show_suggestions_help"]
            )
            
            # Enhanced mode specific settings
            if is_enhanced_mode:
                show_validation = st.checkbox(
                    texts["show_validation"],
                    value=True,
                    help=texts["validation_help"]
                )
                include_speaker_notes = st.checkbox(
                    texts["speaker_notes"],
                    value=True,
                    help=texts["speaker_notes_help"]
                )
            else:
                show_validation = False
                include_speaker_notes = False
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header(texts["file_upload_title"])
        
        # File uploader with drag & drop
        uploaded_file = st.file_uploader(
            texts["file_upload_label"],
            type=['txt', 'md'],
            help=texts["file_upload_help"],
            accept_multiple_files=False
        )
        
        # Sample file buttons
        st.markdown(texts["sample_files"])
        col_sample1, col_sample2 = st.columns(2)
        
        with col_sample1:
            if st.button(texts["english_sample"], use_container_width=True):
                with open("examples/sample_markdown.md", 'r', encoding='utf-8') as f:
                    sample_content = f.read()
                st.session_state['sample_content'] = sample_content
                st.session_state['sample_filename'] = "sample_markdown.md"
                
        with col_sample2:
            if st.button(texts["japanese_sample"], use_container_width=True):
                with open("examples/sample_presentation.txt", 'r', encoding='utf-8') as f:
                    sample_content = f.read()
                st.session_state['sample_content'] = sample_content
                st.session_state['sample_filename'] = "sample_presentation.txt"
        
        # Process uploaded file or sample
        content = None
        filename = None
        
        if uploaded_file is not None:
            content = uploaded_file.getvalue().decode('utf-8')
            filename = uploaded_file.name
        elif 'sample_content' in st.session_state:
            content = st.session_state['sample_content']
            filename = st.session_state['sample_filename']
        
        # Show file info
        if content:
            st.success(texts["file_loaded"].format(filename))
            st.info(texts["content_length"].format(len(content)))
            
            # Preview content
            with st.expander(texts["preview_content"]):
                st.text_area(texts["file_content"], content, height=200, disabled=True)
    
    with col2:
        st.header(texts["slide_generation_title"])
        
        if content:
            # Parse the content
            with st.spinner(texts["analyzing_content"]):
                parser = TextParser()
                
                # Create temporary file for parsing
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp_file:
                    tmp_file.write(content)
                    tmp_file.flush()
                    
                    try:
                        slides = parser.parse_file(tmp_file.name)
                        analysis = SlideStructureAnalyzer.analyze_slides(slides)
                        suggestions = SlideStructureAnalyzer.suggest_improvements(slides)
                    finally:
                        os.unlink(tmp_file.name)
            
            # Display analysis results
            st.success(texts["generated_slides"].format(analysis['total_slides']))
            
            # Analysis metrics
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            
            with col_metric1:
                st.metric(texts["total_slides"], analysis['total_slides'])
                
            with col_metric2:
                st.metric(texts["avg_bullets"], f"{analysis['avg_bullets_per_slide']:.1f}")
                
            with col_metric3:
                slide_types_count = len(analysis['slide_types'])
                st.metric(texts["slide_types"], slide_types_count)
            
            # Show suggestions if enabled
            if show_suggestions and suggestions:
                st.warning(texts["suggestions_title"])
                for suggestion in suggestions:
                    st.write(f"  • {suggestion}")
            
            # Slide preview
            with st.expander(texts["preview_structure"], expanded=True):
                for i, slide in enumerate(slides[:5], 1):  # Show first 5 slides
                    st.write(texts["slide_n"].format(i, slide.title))
                    st.caption(texts["slide_type"].format(slide.slide_type))
                    if slide.content:
                        for j, point in enumerate(slide.content[:3], 1):  # Show first 3 points
                            st.write(f"  {j}. {point}")
                        if len(slide.content) > 3:
                            st.write(texts["more_points"].format(len(slide.content) - 3))
                    st.divider()
                
                if len(slides) > 5:
                    st.info(texts["more_slides"].format(len(slides) - 5))
            
            # Generate presentation button
            st.markdown("---")
            
            # Choose button text and generator based on mode
            button_text = texts["enhanced_button"] if is_enhanced_mode else texts["generate_button"]
            spinner_text = texts["creating_enhanced"] if is_enhanced_mode else texts["creating"]
            success_text = texts["enhanced_success"] if is_enhanced_mode else texts["success"]
            
            if st.button(button_text, type="primary", use_container_width=True):
                with st.spinner(spinner_text):
                    # Choose generator based on mode
                    if is_enhanced_mode:
                        generator = EnhancedHTMLSlidesGenerator()
                    else:
                        generator = HTMLSlidesGenerator()
                    
                    # Create output file in temporary directory
                    output_filename = f"{presentation_title.replace(' ', '_')}.html"
                    temp_output = tempfile.mktemp(suffix=".html")
                    
                    try:
                        if is_enhanced_mode:
                            # Enhanced generation with additional parameters
                            result = generator.create_presentation(
                                slides=slides,
                                title=presentation_title,
                                theme=selected_theme,
                                output_path=temp_output,
                                language=selected_language.lower()[:2]  # "en" or "ja"
                            )
                        else:
                            # Standard generation
                            result = generator.create_presentation(
                                slides=slides,
                                title=presentation_title,
                                theme=selected_theme,
                                output_path=temp_output
                            )
                        
                        # Read generated file
                        with open(temp_output, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                        
                        st.success(success_text)
                        
                        # Display generation results
                        if is_enhanced_mode:
                            # Enhanced mode - show additional information
                            col_result1, col_result2, col_result3, col_result4 = st.columns(4)
                            
                            with col_result1:
                                st.metric(texts["slides_created"], result['slides_count'])
                                
                            with col_result2:
                                st.metric(texts["theme"], result['theme'])
                                
                            with col_result3:
                                st.metric(texts["file_size"], f"{result['file_size']:,} bytes")
                                
                            with col_result4:
                                pattern_count = len(result.get('pattern_distribution', {}))
                                st.metric("🎨 Patterns", pattern_count)
                            
                            # Show pattern distribution
                            if 'pattern_distribution' in result:
                                st.subheader("🔍 まじん式 Pattern Distribution")
                                pattern_dist = result['pattern_distribution']
                                for pattern, count in pattern_dist.items():
                                    st.write(f"  • **{pattern}**: {count} slides")
                            
                            # Show validation results if enabled
                            if show_validation and 'validation_result' in result:
                                validation = result['validation_result']
                                st.subheader("✅ Validation Results")
                                
                                if validation['is_valid']:
                                    st.success("✅ Slide structure is valid")
                                else:
                                    st.error("❌ Slide structure has issues")
                                
                                if validation.get('warnings'):
                                    with st.expander("⚠️ Warnings", expanded=False):
                                        for warning in validation['warnings']:
                                            st.warning(f"• {warning}")
                                
                                if validation.get('suggestions'):
                                    with st.expander("💡 Suggestions", expanded=False):
                                        for suggestion in validation['suggestions']:
                                            st.info(f"• {suggestion}")
                                            
                            # Speaker notes info
                            if include_speaker_notes:
                                st.info("🎤 Speaker notes have been automatically generated and included in the presentation. Press 'S' during the presentation to view them.")
                        
                        else:
                            # Standard mode - original layout
                            col_result1, col_result2, col_result3 = st.columns(3)
                            
                            with col_result1:
                                st.metric(texts["slides_created"], result['slides_count'])
                                
                            with col_result2:
                                st.metric(texts["theme"], result['theme'])
                                
                            with col_result3:
                                st.metric(texts["file_size"], f"{result['file_size']:,} bytes")
                        
                        # Download button
                        st.download_button(
                            label=texts["download_button"],
                            data=html_content,
                            file_name=output_filename,
                            mime="text/html",
                            type="primary",
                            use_container_width=True
                        )
                        
                        # Preview button
                        if st.button(texts["preview_button"], use_container_width=True):
                            # Create a temporary file for preview
                            preview_file = tempfile.mktemp(suffix=".html")
                            with open(preview_file, 'w', encoding='utf-8') as f:
                                f.write(html_content)
                            
                            # Open in browser (this works locally)
                            import webbrowser
                            webbrowser.open(f"file://{preview_file}")
                            st.success(texts["opened_browser"])
                    
                    except Exception as e:
                        st.error(texts["error_generating"].format(str(e)))
                    
                    finally:
                        # Cleanup
                        if os.path.exists(temp_output):
                            os.unlink(temp_output)
        
        else:
            st.info(texts["upload_instruction"])
            
            # Quick start guide
            with st.expander(texts["quick_guide"], expanded=True):
                st.markdown(texts["how_to_use"])

def create_download_link(file_content: str, filename: str, link_text: str):
    """Create a download link for file content"""
    b64 = base64.b64encode(file_content.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

if __name__ == "__main__":
    main()