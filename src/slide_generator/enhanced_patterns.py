#!/usr/bin/env python3
"""
Enhanced Slide Patterns - まじん式プロンプト設計統合
Googleスライド自動生成のための高度なパターンシステム
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import re

class SlidePattern(Enum):
    """スライドの表現パターン（まじん式8パターン準拠）"""
    TITLE = "title"           # 表紙
    SECTION = "section"       # 章扉  
    CONTENT = "content"       # 1～2カラム箇条書き＋小見出し
    COMPARE = "compare"       # 左右比較
    PROCESS = "process"       # 手順・工程
    TIMELINE = "timeline"     # 時系列
    DIAGRAM = "diagram"       # レーン図＋カード＋自動矢印
    CARDS = "cards"          # カードグリッド
    TABLE = "table"          # 表形式
    PROGRESS = "progress"    # 進捗バー
    CLOSING = "closing"      # 結び

@dataclass
class EnhancedSlideStructure:
    """まじん式設計思想に基づく拡張スライド構造"""
    pattern: SlidePattern
    title: str
    subhead: Optional[str] = None
    content: List[str] = field(default_factory=list)
    speaker_notes: Optional[str] = None  # 発表原稿
    
    # パターン固有フィールド
    compare_data: Optional[Dict[str, Any]] = None
    process_steps: Optional[List[str]] = None
    timeline_data: Optional[List[Dict[str, Any]]] = None
    diagram_lanes: Optional[List[Dict[str, Any]]] = None
    cards_items: Optional[List[Union[str, Dict[str, str]]]] = None
    table_data: Optional[Dict[str, Any]] = None
    progress_items: Optional[List[Dict[str, Any]]] = None
    
    # メタデータ
    section_number: Optional[int] = None
    date: Optional[str] = None
    images: List[str] = field(default_factory=list)

class InlineStyleParser:
    """インライン強調記法パーサー（まじん式仕様）"""
    
    @staticmethod
    def parse_styled_text(text: str) -> Dict[str, Any]:
        """
        インライン強調記法を解析
        **太字** → 太字
        [[重要語]] → 太字＋Googleブルー
        """
        if not text:
            return {"clean_text": "", "styles": []}
        
        styles = []
        clean_text = ""
        offset = 0
        
        # [[重要語]] パターン
        for match in re.finditer(r'\[\[([^\]]+)\]\]', text):
            start = match.start() - offset
            end = start + len(match.group(1))
            clean_text = clean_text[:start] + match.group(1) + clean_text[match.end() - offset:]
            styles.append({
                "start": start,
                "end": end,
                "bold": True,
                "color": "#4285F4"  # Google Blue
            })
            offset += 4  # [[ と ]] の文字数
        
        # **太字** パターン  
        text_temp = clean_text
        clean_text = ""
        offset = 0
        
        for match in re.finditer(r'\*\*([^*]+)\*\*', text_temp):
            start = match.start() - offset
            end = start + len(match.group(1))
            clean_text = clean_text[:start] + match.group(1) + clean_text[match.end() - offset:]
            styles.append({
                "start": start,
                "end": end,
                "bold": True
            })
            offset += 4  # ** の文字数
        
        # 最終的なクリーンテキストを設定
        if not clean_text:
            clean_text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
            clean_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_text)
        
        return {
            "clean_text": clean_text,
            "styles": styles
        }

class PatternSelector:
    """コンテンツに最適なパターンを選定するAI（まじん式戦略設計）"""
    
    @staticmethod
    def select_optimal_pattern(title: str, content: List[str], context: str = "") -> SlidePattern:
        """
        タイトルとコンテンツから最適なパターンを選定
        まじん式: AIを戦略コンサルとして活用
        """
        title_lower = title.lower()
        content_text = " ".join(content).lower() if content else ""
        combined = f"{title_lower} {content_text} {context}".lower()
        
        # パターン判定ロジック（優先順位順）
        patterns_keywords = {
            SlidePattern.COMPARE: [
                "vs", "対比", "比較", "違い", "差", "選択肢", "メリット", "デメリット",
                "before", "after", "以前", "以降", "左右", "優劣"
            ],
            SlidePattern.PROCESS: [
                "手順", "ステップ", "プロセス", "工程", "流れ", "段階", "方法",
                "step", "process", "procedure", "workflow", "how to"
            ],
            SlidePattern.TIMELINE: [
                "時系列", "スケジュール", "予定", "計画", "ロードマップ", "歴史",
                "timeline", "schedule", "roadmap", "history", "年", "月", "日"
            ],
            SlidePattern.PROGRESS: [
                "進捗", "進度", "達成率", "完了", "進行", "パーセント", "%",
                "progress", "completion", "achievement", "status"
            ],
            SlidePattern.TABLE: [
                "表", "一覧", "リスト", "項目", "比較表", "仕様",
                "table", "list", "specification", "comparison"
            ],
            SlidePattern.DIAGRAM: [
                "図", "関係", "構造", "組織", "フロー", "レーン", "部門",
                "diagram", "structure", "organization", "flow", "lane"
            ],
            SlidePattern.CARDS: [
                "カード", "項目", "要素", "特徴", "機能", "サービス",
                "cards", "features", "services", "items", "elements"
            ]
        }
        
        # キーワードマッチングによるスコア計算
        pattern_scores = {}
        for pattern, keywords in patterns_keywords.items():
            score = sum(1 for keyword in keywords if keyword in combined)
            if score > 0:
                pattern_scores[pattern] = score
        
        # 最高スコアのパターンを選択
        if pattern_scores:
            best_pattern = max(pattern_scores, key=pattern_scores.get)
            return best_pattern
        
        # デフォルトはCONTENT（箇条書き）
        return SlidePattern.CONTENT

class SpeakerNotesGenerator:
    """スピーカーノート自動生成（まじん式発表原稿システム）"""
    
    @staticmethod
    def generate_speaker_notes(slide: EnhancedSlideStructure) -> str:
        """
        スライド内容に基づいて発表原稿を生成
        まじん式: プレーンテキストで要点を簡潔に
        """
        notes_parts = []
        
        # タイトルベースの導入
        if slide.title:
            intro = f"それでは、{slide.title}について説明いたします。"
            notes_parts.append(intro)
        
        # サブヘッドがある場合
        if slide.subhead:
            subhead_note = f"{slide.subhead}という観点から見ていきます。"
            notes_parts.append(subhead_note)
        
        # パターン別の原稿生成
        if slide.pattern == SlidePattern.CONTENT:
            if slide.content:
                notes_parts.append("主要なポイントは以下の通りです。")
                for i, point in enumerate(slide.content[:3], 1):  # 最大3点まで
                    clean_text = InlineStyleParser.parse_styled_text(point)["clean_text"]
                    notes_parts.append(f"{i}点目として、{clean_text}")
        
        elif slide.pattern == SlidePattern.COMPARE:
            notes_parts.append("こちらは比較検討の結果をまとめたものです。")
            if slide.compare_data:
                left_title = slide.compare_data.get('left_title', '左側')
                right_title = slide.compare_data.get('right_title', '右側')
                notes_parts.append(f"{left_title}と{right_title}を比較して検討いたします。")
        
        elif slide.pattern == SlidePattern.PROCESS:
            notes_parts.append("こちらのプロセスに沿って進めていきます。")
            if slide.process_steps:
                steps_count = len(slide.process_steps)
                notes_parts.append(f"全体で{steps_count}つのステップに分かれています。")
        
        elif slide.pattern == SlidePattern.TIMELINE:
            notes_parts.append("時系列で整理すると、このような流れになります。")
            if slide.timeline_data:
                notes_parts.append(f"{len(slide.timeline_data)}つの主要なマイルストーンがあります。")
        
        elif slide.pattern == SlidePattern.CARDS:
            notes_parts.append("重要な要素をカード形式でまとめました。")
            if slide.cards_items:
                notes_parts.append(f"{len(slide.cards_items)}つの項目についてご説明します。")
        
        elif slide.pattern == SlidePattern.TABLE:
            notes_parts.append("詳細な情報を表形式で整理しています。")
        
        elif slide.pattern == SlidePattern.PROGRESS:
            notes_parts.append("現在の進捗状況をご報告いたします。")
        
        elif slide.pattern == SlidePattern.DIAGRAM:
            notes_parts.append("全体の構造と関係性を図で示しています。")
        
        # 締めの言葉
        if slide.pattern not in [SlidePattern.TITLE, SlidePattern.SECTION, SlidePattern.CLOSING]:
            notes_parts.append("以上がこちらのスライドの内容になります。")
        
        return " ".join(notes_parts)

class SlideStructureValidator:
    """スライド構造の自己検証システム（まじん式品質保証）"""
    
    @staticmethod
    def validate_slide_structure(slides: List[EnhancedSlideStructure]) -> Dict[str, Any]:
        """
        スライド構造の妥当性を検証
        まじん式: 自己検証機能で信頼性UP
        """
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        # 基本構造チェック
        if not slides:
            validation_result["errors"].append("スライドが存在しません")
            validation_result["is_valid"] = False
            return validation_result
        
        # タイトルスライドチェック
        has_title = any(slide.pattern == SlidePattern.TITLE for slide in slides)
        if not has_title:
            validation_result["warnings"].append("タイトルスライドがありません")
        
        # クロージングスライドチェック  
        has_closing = any(slide.pattern == SlidePattern.CLOSING for slide in slides)
        if not has_closing:
            validation_result["suggestions"].append("クロージングスライドの追加を推奨します")
        
        # 文字数チェック
        for i, slide in enumerate(slides):
            if slide.title and len(slide.title) > 40:
                validation_result["warnings"].append(f"スライド{i+1}: タイトルが40文字を超えています")
            
            if slide.content:
                for j, content in enumerate(slide.content):
                    clean_text = InlineStyleParser.parse_styled_text(content)["clean_text"]
                    if len(clean_text) > 90:
                        validation_result["warnings"].append(
                            f"スライド{i+1}: 箇条書き{j+1}が90文字を超えています"
                        )
        
        # スライド枚数チェック
        if len(slides) > 50:
            validation_result["errors"].append("スライド枚数が50枚を超えています（GAS制限）")
            validation_result["is_valid"] = False
        elif len(slides) > 30:
            validation_result["warnings"].append("スライド枚数が多めです（30枚以上）")
        
        # 章構成チェック
        sections = [slide for slide in slides if slide.pattern == SlidePattern.SECTION]
        if len(sections) >= 2:
            # アジェンダスライドの存在確認
            has_agenda = any(
                slide.pattern == SlidePattern.CONTENT and 
                any(keyword in slide.title.lower() for keyword in ["アジェンダ", "agenda", "目次"])
                for slide in slides
            )
            if not has_agenda:
                validation_result["suggestions"].append("複数章がある場合、アジェンダスライドの追加を推奨します")
        
        return validation_result

class EnhancedSlideGenerator:
    """まじん式設計思想統合スライドジェネレーター"""
    
    def __init__(self):
        self.pattern_selector = PatternSelector()
        self.notes_generator = SpeakerNotesGenerator()
        self.validator = SlideStructureValidator()
    
    def enhance_slide_structure(self, basic_slides) -> List[EnhancedSlideStructure]:
        """
        基本スライド構造を拡張スライド構造に変換
        まじん式: 戦略設計者としてのAI活用
        """
        enhanced_slides = []
        
        for slide in basic_slides:
            # 最適パターン選定
            optimal_pattern = self.pattern_selector.select_optimal_pattern(
                slide.title, slide.content
            )
            
            # 拡張構造作成
            enhanced_slide = EnhancedSlideStructure(
                pattern=optimal_pattern,
                title=slide.title,
                content=slide.content[:],
                section_number=getattr(slide, 'section_number', None)
            )
            
            # パターン固有データの設定
            self._populate_pattern_data(enhanced_slide, slide)
            
            # スピーカーノート生成
            enhanced_slide.speaker_notes = self.notes_generator.generate_speaker_notes(enhanced_slide)
            
            enhanced_slides.append(enhanced_slide)
        
        return enhanced_slides
    
    def _populate_pattern_data(self, enhanced_slide: EnhancedSlideStructure, basic_slide):
        """パターン固有データを設定"""
        if enhanced_slide.pattern == SlidePattern.COMPARE and len(enhanced_slide.content) >= 2:
            mid = len(enhanced_slide.content) // 2
            enhanced_slide.compare_data = {
                "left_title": "選択肢A",
                "right_title": "選択肢B", 
                "left_items": enhanced_slide.content[:mid],
                "right_items": enhanced_slide.content[mid:]
            }
        
        elif enhanced_slide.pattern == SlidePattern.PROCESS:
            enhanced_slide.process_steps = enhanced_slide.content[:]
        
        elif enhanced_slide.pattern == SlidePattern.CARDS:
            enhanced_slide.cards_items = [{"title": item, "desc": ""} for item in enhanced_slide.content]
        
        elif enhanced_slide.pattern == SlidePattern.TIMELINE and enhanced_slide.content:
            # 簡単なタイムライン生成
            enhanced_slide.timeline_data = []
            for i, item in enumerate(enhanced_slide.content):
                enhanced_slide.timeline_data.append({
                    "label": item,
                    "date": f"Phase {i+1}",
                    "state": "todo"
                })
    
    def validate_and_optimize(self, slides: List[EnhancedSlideStructure]) -> Dict[str, Any]:
        """構造検証と最適化提案"""
        return self.validator.validate_slide_structure(slides)

if __name__ == "__main__":
    # テスト用サンプル
    print("Enhanced Slide Patterns - まじん式プロンプト設計統合")
    print("=" * 50)
    
    # インライン記法テスト
    test_text = "これは**重要な**ポイントで、[[特に注意]]すべき項目です"
    parsed = InlineStyleParser.parse_styled_text(test_text)
    print(f"Original: {test_text}")
    print(f"Clean: {parsed['clean_text']}")
    print(f"Styles: {parsed['styles']}")