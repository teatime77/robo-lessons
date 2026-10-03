# 開発・執筆ガイド

## 現在の構成

`docs/index.md` の28章は、制作・実験を通じた学習順序の原本です。`docs/chapters/` に全28章の本文があり、学習内容、実験手順、段階別課題、確認問題と考え方を説明しています。章の英語ラベルは本文冒頭に置き、目次の概要から参照します。ステップ別の `toctree` に章を順序通り登録しています。

現段階では部品の型番・定格・配線、ビジュアル環境、実習アプリ、ファームウェアが未確定・未実装です。本文の説明と実施前の確認事項を分け、`docs/shared/practice-status.md` で状態を管理しています。SphinxとHTMLの検証は教材サイトの確認であり、実機の実験結果や動作保証ではありません。

MyST、MathJax、Furoと既存のPython依存固定版を維持しています。日本語本文は翻訳カタログなしで表示します。`docs/locale/ja/` の過去の試作PO/MOは変更せず、設定で適用を停止しています。

## ファイルの配置

「予定」は、必要なファイルを作る時点でディレクトリを作成します。

| 配置 | 内容 | 現在の状態・管理方針 |
| --- | --- | --- |
| `docs/index.md` | 28章の目次と順序 | 原本。章を追加したら概要・参照・toctreeを更新 |
| `docs/conf.py` | Sphinx設定 | 日本語、MyST、Furo、MathJax |
| `docs/shared/` | 用語・記号・単位、共通部品・配線、実習前の確認 | 同じ仕様を独立して複製しない |
| `docs/chapters/<slug>.md` | 生徒用の章本文 | 全28章。内容を表す英語名 |
| `docs/instructors/<slug>.md` | 講師用の授業計画、解答、対処 | 予定。対象章を参照し、問題と解答を同時更新 |
| `docs/worksheets/<slug>.md` | 実験記録シート、問題 | 予定。章本文・解答との対応を管理 |
| `docs/_includes/` | 部品表等の共通断片 | 予定。単独ページとしてはビルドしない |
| `docs/_images/` | 公開するSVG・画像 | 生成画像も管理。図中文字と代替説明は日本語 |
| `figures/` | Python、SVG編集元、将来のMermaid `.mmd` | 生成条件、出典、出力先を記録 |
| `apps/<activity>/` | TypeScript等のブラウザ実習ソース | 予定。表示は日本語。package.jsonとロックも管理 |
| `firmware/<board>/` | ESP32のソース・通信仕様・依存設定 | 予定。対象ボードとビルド方法を明記 |
| `hardware/` | 型番別データシート出典、配線編集元、CAD、部品表 | 予定。CAD編集元と配布用STL等を管理 |
| `data/<experiment>/` | 実測の原データ・条件・単位 | 予定。説明用の架空データと分け、個人情報を記録しない |
| `docs/locale/` | 将来のPO等の翻訳カタログ | 既存試作のみ。PO/POTを管理、MOは生成物 |
| `development/` | 開発資料、章テンプレート | Sphinxの教材ビルド対象外 |
| `scripts/` | 検証等の開発用スクリプト | HTMLのローカルリンク検証 |
| `_build/` | Sphinx HTML、gettext、将来のアプリ配布ビルド | 再生成できる成果物として除外 |

実習アプリはPC・スマートフォンのブラウザで操作・画像処理・AIを担当し、ESP32でモーターとセンサを扱います。アプリとファームウェアを実装する段階で、指令・計測値・単位・通信断時の動作を共有する通信仕様を作成します。Firebase Hostingは将来の公開先であり、現在の構成にはクラウド設定を追加していません。

## 章を書く・関連ファイルを更新する

1. `AGENTS.md` と対象章の目次概要、前後の章、共通資料を読みます。
2. `development/templates/chapter.md` を `docs/chapters/<slug>.md` にコピーし、仮のラベルと項目を実際の内容に置き換えます。
3. 章本文冒頭に安定したラベルを定義します。目次の見出し・概要・順序を保ち、本文への `{ref}` とステップ別 `toctree` を更新します。既存章のラベルを変えたり二重に定義したりしません。
4. 前提・次章の参照、講師資料、問題・解答、部品仕様、配線、コード、図、用語を `rg` で横断検索し、関連ファイルを一緒に更新します。
5. `make check` と差分確認を行い、本文・図・数式・日本語表示をブラウザで確認します。

未作成ページへのリンクは作りません。章番号は表示順序にだけ使います。順序が変わってもラベルは維持します。現在の28章は、内容を制作・計測・制御へ段階的につなげるため、追加・削除・結合・分割せず詳細化しています。将来構成を変える場合は前提知識と参照も同時に見直します。

MySTでは `(wheel-motion)=` のような明示ラベルと `{ref}` を使います。図には `figure` ディレクティブ、英語の `:name:`、日本語の `:alt:` とキャプションを付けます。サンプルコードは実ファイルを `literalinclude` で引用し、本文との二重管理を避けます。[MyST公式の記法](https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html)を参照してください。

## 図の生成

```bash
make figures
```

現在は `figures/generate_learning_cycle.py` がPython標準ライブラリだけで、日本語の学習手順図を `docs/_images/learning-cycle.svg` に生成します。生成元と出力を一緒に管理し、SVGにタイトルと説明を付けています。図は処理の順序を示し、物理法則の証明や測定結果には使いません。

`figures/generate_robot_models.py` は、2軸アームと台車上の倒立振子の概念図を `docs/_images/planar-arm.svg` と `docs/_images/cart-pole.svg` に生成します。描画用の座標は実機寸法ではありません。関節角・座標・力の正方向を本文と照合して更新します。

数値グラフや回路図・機構図を追加する際は、入力データ、仮定、座標、単位、生成コマンドを記録します。Matplotlib等の追加依存は、その時点で直接依存と固定版記録を更新します。

Mermaid拡張は現在導入していません。使用する場合は [sphinxcontrib-mermaid公式資料](https://github.com/mgaitan/sphinxcontrib-mermaid) に従って依存とSphinx設定を追加し、ブラウザで描画を確認します。Mermaidの図中文字は通常の本文と同じ方法では翻訳抽出されないため、図の外部ソースと日本語ラベルの管理方法も記録します。

MathJaxはSphinx標準設定のJavaScriptを利用するため、数式の描画にはブラウザから外部配信先へのアクセスが必要です。現在のSVGはネットワークなしで表示できます。オフライン授業に対応する段階で、MathJax等の配信資産をローカル化し、ライセンスも確認します。

## 依存関係と検証

検証対象はPython 3.12です。`requirements.in` は直接依存、既存の `requirements.txt` は間接依存を含む固定版記録です。今回、既存の固定版は変更していません。Sphinx・MyST・Furoがビルドを担い、sphinx-intlは将来の翻訳管理用です。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
make check
make serve
```

`make check` はpipの整合性確認、Sphinxの全ページ再読込・再出力（`-E -a`）、未解決参照を警告にする `-n`、警告を失敗にする `-W --keep-going`、生成HTMLのローカルリンク・画像・アンカー確認を行います。外部サイトの到達性やJavaScriptの動作は検証しないため、必要に応じてブラウザ確認も行います。

Makeを使わない場合：

8000番ポートが使用中の場合は `make serve PORT=8001` を使い、ブラウザでも8001番を指定します。以下の直接実行でもポート番号を変更できます。

```bash
.venv/bin/python -m pip check
.venv/bin/python -m sphinx -b html -E -a -n -W --keep-going docs _build/html
.venv/bin/python scripts/check_html.py _build/html
.venv/bin/python -m http.server 8000 --bind 127.0.0.1 --directory _build/html
```

依存を更新する場合は、`requirements.in` の対象版を変更し、新しい作業用仮想環境で間接依存も解決して固定版記録を作り、差分を確認します。

```bash
python3 -m venv .venv-refresh
.venv-refresh/bin/python -m pip install -r requirements.in
.venv-refresh/bin/python -m pip freeze > requirements.txt
make check PYTHON=.venv-refresh/bin/python
```

既存の `requirements.txt` にだけある依存も更新前に用途を確認します。固定版記録や今後の `uv.lock`・`package-lock.json` 等を無視対象にしません。Python/OSが異なる環境は追加検証して対応範囲を記録します。

## 将来の翻訳

日本語を完成させてから英訳し、校正済み英語を他言語の翻訳元とします。Sphinxのgettextは文章を抽出し、PO/MOと `language` 設定によって翻訳済み文章を管理・表示します。Sphinxとsphinx-intl自体は機械翻訳を行いません。[Sphinx公式の国際化手順](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html)に基づき、翻訳開始時にカタログとビルド方法を整えます。

校正済み英語を基準にする切替時には、日本語原文の保存先、英語基準のカタログ抽出、日本語との対応表、図中文字とアプリ表示の翻訳方法を合わせて決めます。ファイル名・ラベルは変えず、今は切替や翻訳ファイル生成を行いません。
