PYTHON ?= .venv/bin/python
PORT ?= 8000
HTML_DIR := _build/html

.PHONY: html check figures serve

html:
	$(PYTHON) -m sphinx -b html -n -W --keep-going docs $(HTML_DIR)

check:
	$(PYTHON) -m pip check
	$(PYTHON) -m sphinx -b html -E -a -n -W --keep-going docs $(HTML_DIR)
	$(PYTHON) scripts/check_html.py $(HTML_DIR)

figures:
	$(PYTHON) figures/generate_learning_cycle.py
	$(PYTHON) figures/generate_robot_models.py

serve: html
	$(PYTHON) -m http.server $(PORT) --bind 127.0.0.1 --directory $(HTML_DIR)
