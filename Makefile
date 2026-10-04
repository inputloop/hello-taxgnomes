# hello-taxgnomes: one literate recipe unfolds into the builder, the page, its egad hooks and the checks.
# Copyright 2026 Corwin Brust <corwin@bru.st> and Contributors; GPL-3.0-or-later.
EMACS ?= emacs
RECIPE = hello-taxgnomes.org

all: unfold build page

unfold:
	awk -f unfold.awk $(RECIPE) >/dev/null
	chmod +x tools/tg1bd.py tools/tg1rd tools/tg1dr.py tools/tg1pg.py tools/tg1ck.py tests/taxgnomes-tests.sh

build:
	python3 tools/tg1bd.py

page:
	python3 tools/tg1pg.py

check-unfold:
	@sh tests/unfold-check.sh $(RECIPE) "$(EMACS)"

check: check-unfold
	sh tests/taxgnomes-tests.sh
	sh tests/taxgnomes-tests.sh --reader
	sh tests/taxgnomes-tests.sh --cold
	sh tests/taxgnomes-tests.sh --offline
	sh tests/taxgnomes-tests.sh --egad
	sh tests/taxgnomes-tests.sh --prove-red
	sh tests/unfold-check.sh $(RECIPE) "$(EMACS)" --prove-red

.PHONY: all unfold build page check check-unfold
