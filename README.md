# robo-lessons
Open educational materials for robotics, mathematics, physics, and programming, with interactive simulations and hands-on projects.

ロボットの制作・実験を通じて、電気・プログラミング・数学・物理を少しずつ学ぶブラウザ教材です。日本語で執筆し、まとまった段階で英訳・校正を行い、その英語から他言語に翻訳します。

教材の順序は [28章の目次](docs/index.md) が基準です。[各章のMarkdown](docs/chapters/) に、学習内容の説明、実験手順、入門・基本・発展の課題、確認問題と考え方をまとめています。実機の型番・配線・実習アプリは確定・実装後に実機検証を行います。

## ローカルで表示する

検証環境は Python 3.12。リポジトリのルートで実行します。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
make check
make serve
```

ブラウザで <http://127.0.0.1:8000/> を開きます。サーバーは `Ctrl+C` で停止します。既存の `.venv` がある場合は作成を省略できます。

8000番ポートが使用中なら `make serve PORT=8001` とし、<http://127.0.0.1:8001/> を開きます。

`make check` は依存関係の整合性、Sphinxの警告・相互参照、生成HTMLのローカルリンクを確認します。`make html` はHTMLのビルドのみ、`make figures` は図の再生成です。

## 執筆・開発

- [作業ルール](AGENTS.md)：教材方針と複数ファイルを更新する際の確認事項。
- [開発ガイド](development/README.md)：配置、依存関係、執筆・翻訳・検証の手順。
- [章のテンプレート](development/templates/chapter.md)：教材サイトのビルド対象外。
- [用語・記号・単位の共通ルール](docs/shared/conventions.md)。
- [部品・電源・配線の共通仕様](docs/shared/hardware.md)：未選定の仕様は「要確認」として管理。
- [実習前の確認](docs/shared/practice-status.md)：実施条件、疑似コード、実測と仮定の区別。

現在のテーマはFuro、本文はMyST Markdown、数式はLaTeX記法とMathJaxです。実習アプリやESP32ファームウェアは今後追加します。公開先は将来Firebase Hostingを想定しています。

ライセンスは既存の [MIT License](LICENSE) です。外部の素材を使う場合は、そのライセンスと出典も記録します。
