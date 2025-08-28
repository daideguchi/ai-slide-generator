# AI Slide Generator

テキストから高品質なスライドを自動生成するツール

## 機能

1. **🌐 Web UI (Streamlit)**: ドラッグ&ドロップで簡単スライド生成 ⭐ **新機能！**
2. **Google Slides生成**: テキストファイルからGoogle Slidesプレゼンテーションを自動作成
3. **HTML スライド生成**: Reveal.jsを使用したWebプレゼンテーション生成
4. **テンプレート対応**: カスタマイズ可能なデザインテンプレート
5. **CLI インターフェース**: シンプルなコマンドライン操作

## 使用方法

### 🌟 Web UI (推奨・最も簡単)

**1. 起動方法:**
```bash
# Mac/Linux
./run_ui.sh

# Windows
run_ui.bat

# 手動起動
source venv/bin/activate  # 仮想環境有効化
PYTHONPATH=src streamlit run streamlit_ui.py
```

**2. ブラウザでアクセス:**
```
http://localhost:8501
```

**3. 操作手順:**
- 📁 ファイルをドラッグ&ドロップ
- ⚙️ テーマとタイトルを選択
- 👀 スライド構造をプレビュー
- 🚀 「Generate HTML Presentation」をクリック
- 💾 完成したHTMLファイルをダウンロード

### CLI方式

### Google Slides生成
```bash
python slide_generator.py google input.txt --template="modern"
```

### HTML スライド生成
```bash
python slide_generator.py html input.txt --theme="dark"
```

## セットアップ

1. Google Cloud Console でAPI認証を設定
2. credentials.jsonファイルを配置
3. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

## 対応ファイル形式

- テキストファイル (.txt)
- Markdownファイル (.md)