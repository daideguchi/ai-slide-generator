#!/usr/bin/env python3
"""
Google Style Themes - まじん式デザインシステム統合
Google風デザインテーマとCSS生成システム
"""

from dataclasses import dataclass
from typing import Dict, Any, List
from enum import Enum

class GoogleColors:
    """Google Material Design カラーパレット"""
    PRIMARY_BLUE = "#4285F4"
    GOOGLE_BLUE = "#4285F4"
    GOOGLE_RED = "#EA4335"
    GOOGLE_YELLOW = "#FBBC04"
    GOOGLE_GREEN = "#34A853"
    
    TEXT_PRIMARY = "#333333"
    TEXT_SECONDARY = "#666666"
    
    BACKGROUND_WHITE = "#FFFFFF"
    BACKGROUND_GRAY = "#F8F9FA"
    FAINT_GRAY = "#E8EAED"
    LANE_TITLE_BG = "#F5F5F3"
    LANE_BORDER = "#DADCE0"
    CARD_BG = "#FFFFFF"
    CARD_BORDER = "#DADCE0"
    NEUTRAL_GRAY = "#9E9E9E"
    GHOST_GRAY = "#EFEFED"

@dataclass
class GoogleStyleConfig:
    """Google風スタイル設定"""
    primary_color: str = GoogleColors.PRIMARY_BLUE
    background_color: str = GoogleColors.BACKGROUND_WHITE
    text_color: str = GoogleColors.TEXT_PRIMARY
    accent_color: str = GoogleColors.GOOGLE_GREEN
    
    # フォント設定
    font_family: str = "Google Sans, Arial, sans-serif"
    title_size: str = "2.5em"
    heading_size: str = "1.8em"
    body_size: str = "1.1em"
    small_size: str = "0.9em"
    
    # レイアウト設定
    slide_padding: str = "40px 60px"
    content_max_width: str = "900px"
    border_radius: str = "8px"
    box_shadow: str = "0 2px 8px rgba(0,0,0,0.1)"

class GoogleStyleThemes:
    """まじん式Google風テーマ集"""
    
    @staticmethod
    def get_google_classic_theme() -> Dict[str, Any]:
        """Google Classic テーマ（標準的なGoogle風デザイン）"""
        config = GoogleStyleConfig()
        
        return {
            "name": "Google Classic",
            "description": "標準的なGoogle風デザイン",
            "css": f"""
                /* Google Classic Theme - まじん式デザイン */
                .reveal {{
                    font-family: {config.font_family};
                    color: {config.text_color};
                    background: {config.background_color};
                }}
                
                /* スライド基本設定 */
                .reveal .slides section {{
                    text-align: left;
                    padding: {config.slide_padding};
                    background: {config.background_color};
                    border-radius: {config.border_radius};
                    box-shadow: {config.box_shadow};
                    margin: 20px;
                }}
                
                /* タイトルスライド */
                .reveal .slides section.title-slide {{
                    text-align: center;
                    background: linear-gradient(135deg, {config.primary_color} 0%, {GoogleColors.GOOGLE_BLUE} 100%);
                    color: white;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }}
                
                .reveal .slides section.title-slide h1 {{
                    font-size: 3em;
                    font-weight: 400;
                    margin-bottom: 30px;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                }}
                
                .reveal .slides section.title-slide .date {{
                    font-size: 1.2em;
                    opacity: 0.9;
                    margin-top: 20px;
                }}
                
                /* セクションスライド（章扉） */
                .reveal .slides section.section-slide {{
                    background: {GoogleColors.BACKGROUND_GRAY};
                    position: relative;
                    text-align: center;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                
                .reveal .slides section.section-slide::before {{
                    content: attr(data-section-number);
                    position: absolute;
                    top: 20%;
                    left: 50%;
                    transform: translateX(-50%);
                    font-size: 12em;
                    font-weight: 900;
                    color: {GoogleColors.GHOST_GRAY};
                    z-index: 1;
                }}
                
                .reveal .slides section.section-slide h2 {{
                    font-size: 2.8em;
                    color: {config.primary_color};
                    font-weight: 400;
                    z-index: 2;
                    position: relative;
                }}
                
                /* 標準コンテンツスライド */
                .reveal .slides section h1,
                .reveal .slides section h2 {{
                    color: {config.primary_color};
                    font-weight: 400;
                    margin-bottom: 20px;
                    position: relative;
                }}
                
                .reveal .slides section h1::after,
                .reveal .slides section h2::after {{
                    content: '';
                    position: absolute;
                    left: 0;
                    bottom: -8px;
                    width: 60px;
                    height: 4px;
                    background: {config.primary_color};
                }}
                
                .reveal .slides section h3 {{
                    color: {GoogleColors.TEXT_SECONDARY};
                    font-size: {config.body_size};
                    font-weight: 500;
                    margin: 15px 0;
                }}
                
                /* 箇条書きスタイル */
                .reveal .slides section ul {{
                    margin: 20px 0;
                    list-style: none;
                }}
                
                .reveal .slides section ul li {{
                    margin: 12px 0;
                    padding-left: 25px;
                    position: relative;
                    font-size: {config.body_size};
                    line-height: 1.6;
                }}
                
                .reveal .slides section ul li::before {{
                    content: '•';
                    color: {config.primary_color};
                    font-size: 1.4em;
                    position: absolute;
                    left: 0;
                    top: -2px;
                }}
                
                /* 2カラムレイアウト */
                .reveal .slides section .two-columns {{
                    display: flex;
                    gap: 40px;
                    margin: 30px 0;
                }}
                
                .reveal .slides section .two-columns > div {{
                    flex: 1;
                }}
                
                /* 比較レイアウト */
                .reveal .slides section .compare-layout {{
                    display: flex;
                    gap: 30px;
                    margin: 30px 0;
                }}
                
                .reveal .slides section .compare-box {{
                    flex: 1;
                    border: 2px solid {GoogleColors.LANE_BORDER};
                    border-radius: {config.border_radius};
                    overflow: hidden;
                    background: {GoogleColors.CARD_BG};
                }}
                
                .reveal .slides section .compare-header {{
                    background: {config.primary_color};
                    color: white;
                    padding: 15px 20px;
                    font-weight: 500;
                    text-align: center;
                }}
                
                .reveal .slides section .compare-content {{
                    padding: 20px;
                }}
                
                /* プロセス（ステップ）レイアウト */
                .reveal .slides section .process-steps {{
                    margin: 30px 0;
                }}
                
                .reveal .slides section .process-step {{
                    display: flex;
                    align-items: center;
                    margin: 20px 0;
                    position: relative;
                }}
                
                .reveal .slides section .process-number {{
                    width: 40px;
                    height: 40px;
                    border: 2px solid {config.primary_color};
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: white;
                    color: {config.primary_color};
                    font-weight: bold;
                    margin-right: 20px;
                    flex-shrink: 0;
                }}
                
                .reveal .slides section .process-text {{
                    font-size: {config.body_size};
                    line-height: 1.5;
                }}
                
                .reveal .slides section .process-step::after {{
                    content: '';
                    position: absolute;
                    left: 19px;
                    top: 50px;
                    width: 2px;
                    height: 40px;
                    background: {GoogleColors.FAINT_GRAY};
                }}
                
                .reveal .slides section .process-step:last-child::after {{
                    display: none;
                }}
                
                /* タイムライン */
                .reveal .slides section .timeline {{
                    margin: 40px 0;
                    position: relative;
                }}
                
                .reveal .slides section .timeline::before {{
                    content: '';
                    position: absolute;
                    top: 50%;
                    left: 60px;
                    right: 60px;
                    height: 2px;
                    background: {GoogleColors.FAINT_GRAY};
                }}
                
                .reveal .slides section .timeline-items {{
                    display: flex;
                    justify-content: space-between;
                    position: relative;
                    z-index: 2;
                    padding: 0 60px;
                }}
                
                .reveal .slides section .timeline-item {{
                    text-align: center;
                    position: relative;
                }}
                
                .reveal .slides section .timeline-dot {{
                    width: 16px;
                    height: 16px;
                    border-radius: 50%;
                    margin: 0 auto 10px;
                    background: {GoogleColors.GOOGLE_GREEN};
                    border: 3px solid white;
                    box-shadow: 0 0 0 2px {GoogleColors.GOOGLE_GREEN};
                }}
                
                .reveal .slides section .timeline-dot.next {{
                    background: white;
                    box-shadow: 0 0 0 2px {GoogleColors.GOOGLE_YELLOW};
                }}
                
                .reveal .slides section .timeline-dot.todo {{
                    background: white;
                    box-shadow: 0 0 0 2px {GoogleColors.NEUTRAL_GRAY};
                }}
                
                .reveal .slides section .timeline-label {{
                    font-weight: 500;
                    margin-bottom: 5px;
                }}
                
                .reveal .slides section .timeline-date {{
                    font-size: {config.small_size};
                    color: {GoogleColors.TEXT_SECONDARY};
                }}
                
                /* カードグリッド */
                .reveal .slides section .cards-grid {{
                    display: grid;
                    gap: 20px;
                    margin: 30px 0;
                }}
                
                .reveal .slides section .cards-grid.cols-2 {{
                    grid-template-columns: repeat(2, 1fr);
                }}
                
                .reveal .slides section .cards-grid.cols-3 {{
                    grid-template-columns: repeat(3, 1fr);
                }}
                
                .reveal .slides section .card {{
                    background: {GoogleColors.CARD_BG};
                    border: 1px solid {GoogleColors.CARD_BORDER};
                    border-radius: {config.border_radius};
                    padding: 20px;
                    box-shadow: {config.box_shadow};
                    transition: transform 0.2s ease;
                }}
                
                .reveal .slides section .card:hover {{
                    transform: translateY(-2px);
                }}
                
                .reveal .slides section .card-title {{
                    font-weight: 600;
                    color: {config.primary_color};
                    margin-bottom: 10px;
                }}
                
                .reveal .slides section .card-desc {{
                    font-size: {config.small_size};
                    line-height: 1.5;
                    color: {GoogleColors.TEXT_SECONDARY};
                }}
                
                /* プログレスバー */
                .reveal .slides section .progress-items {{
                    margin: 30px 0;
                }}
                
                .reveal .slides section .progress-item {{
                    margin: 20px 0;
                    display: flex;
                    align-items: center;
                }}
                
                .reveal .slides section .progress-label {{
                    width: 200px;
                    font-size: {config.body_size};
                    margin-right: 20px;
                }}
                
                .reveal .slides section .progress-bar {{
                    flex: 1;
                    height: 20px;
                    background: {GoogleColors.FAINT_GRAY};
                    border-radius: 10px;
                    overflow: hidden;
                    margin-right: 15px;
                }}
                
                .reveal .slides section .progress-fill {{
                    height: 100%;
                    background: {GoogleColors.GOOGLE_GREEN};
                    transition: width 1s ease;
                }}
                
                .reveal .slides section .progress-percent {{
                    font-size: {config.small_size};
                    color: {GoogleColors.TEXT_SECONDARY};
                    min-width: 40px;
                }}
                
                /* テーブル */
                .reveal .slides section table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background: white;
                    box-shadow: {config.box_shadow};
                    border-radius: {config.border_radius};
                    overflow: hidden;
                }}
                
                .reveal .slides section table th {{
                    background: {config.primary_color};
                    color: white;
                    padding: 15px 20px;
                    text-align: left;
                    font-weight: 500;
                }}
                
                .reveal .slides section table td {{
                    padding: 12px 20px;
                    border-bottom: 1px solid {GoogleColors.FAINT_GRAY};
                }}
                
                .reveal .slides section table tr:last-child td {{
                    border-bottom: none;
                }}
                
                /* インライン強調記法 */
                .reveal .slides section .google-highlight {{
                    color: {config.primary_color};
                    font-weight: bold;
                }}
                
                .reveal .slides section .bold {{
                    font-weight: bold;
                }}
                
                /* クロージングスライド */
                .reveal .slides section.closing-slide {{
                    text-align: center;
                    background: {GoogleColors.BACKGROUND_GRAY};
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                
                .reveal .slides section.closing-slide img {{
                    max-width: 300px;
                    opacity: 0.8;
                }}
                
                /* レスポンシブ対応 */
                @media (max-width: 768px) {{
                    .reveal .slides section {{
                        padding: 30px 40px;
                    }}
                    
                    .reveal .slides section .two-columns,
                    .reveal .slides section .compare-layout {{
                        flex-direction: column;
                        gap: 20px;
                    }}
                    
                    .reveal .slides section .cards-grid.cols-3 {{
                        grid-template-columns: repeat(2, 1fr);
                    }}
                    
                    .reveal .slides section .timeline-items {{
                        flex-direction: column;
                        gap: 30px;
                        padding: 0;
                    }}
                    
                    .reveal .slides section .timeline::before {{
                        display: none;
                    }}
                }}
            """,
            "fonts": [
                "https://fonts.googleapis.com/css2?family=Google+Sans:wght@300;400;500;700&display=swap"
            ]
        }
    
    @staticmethod
    def get_google_dark_theme() -> Dict[str, Any]:
        """Google Dark テーマ（ダークモード対応）"""
        config = GoogleStyleConfig(
            background_color="#1F1F1F",
            text_color="#E8EAED",
            primary_color="#8AB4F8"
        )
        
        base_theme = GoogleStyleThemes.get_google_classic_theme()
        
        # ダークモード用にCSS調整
        dark_css = base_theme["css"].replace(
            GoogleColors.BACKGROUND_WHITE, "#1F1F1F"
        ).replace(
            GoogleColors.TEXT_PRIMARY, "#E8EAED"
        ).replace(
            GoogleColors.PRIMARY_BLUE, "#8AB4F8"
        ).replace(
            GoogleColors.CARD_BG, "#303030"
        ).replace(
            GoogleColors.FAINT_GRAY, "#444444"
        )
        
        return {
            "name": "Google Dark",
            "description": "Google風ダークテーマ",
            "css": dark_css,
            "fonts": base_theme["fonts"]
        }
    
    @staticmethod  
    def get_google_minimal_theme() -> Dict[str, Any]:
        """Google Minimal テーマ（シンプル版）"""
        config = GoogleStyleConfig(
            slide_padding="50px 80px",
            box_shadow="none"
        )
        
        base_theme = GoogleStyleThemes.get_google_classic_theme()
        
        # ミニマル調整
        minimal_css = base_theme["css"].replace(
            "box-shadow: 0 2px 8px rgba(0,0,0,0.1);", ""
        ).replace(
            "margin: 20px;", "margin: 0;"
        )
        
        return {
            "name": "Google Minimal",
            "description": "Google風ミニマルテーマ",
            "css": minimal_css,
            "fonts": base_theme["fonts"]
        }
    
    @staticmethod
    def get_all_google_themes() -> Dict[str, Dict[str, Any]]:
        """全てのGoogle風テーマを取得"""
        return {
            "google_classic": GoogleStyleThemes.get_google_classic_theme(),
            "google_dark": GoogleStyleThemes.get_google_dark_theme(),
            "google_minimal": GoogleStyleThemes.get_google_minimal_theme()
        }

if __name__ == "__main__":
    # テーマ情報の表示
    themes = GoogleStyleThemes.get_all_google_themes()
    print("Available Google Style Themes:")
    print("=" * 40)
    
    for theme_key, theme_data in themes.items():
        print(f"• {theme_data['name']}: {theme_data['description']}")