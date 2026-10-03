project = "Robotics Learning"
author = "Ko Hamada"

# 教材の原文は日本語。翻訳工程は development/README.md を参照。
language = "ja"

extensions = [
    "myst_parser",
    "sphinx.ext.mathjax",
]

source_suffix = {
    ".md": "markdown",
}

root_doc = "index"
exclude_patterns = ["_build", "locale/**", "_includes/**"]
nitpicky = True

html_theme = "furo"
html_title = "ロボットで学ぶ"

# Support Markdown math notation.
myst_enable_extensions = [
    "dollarmath",
]

# 古い試作カタログは保持するが、現在の日本語本文には適用しない。
# 翻訳を開始する段階で locale_dirs と言語別ビルドを設定する。
locale_dirs = []
gettext_compact = False
