# This is a Makefile

.PHONY: env
env:
	@if conda env list | grep -q "ligo"; then \
		conda env update -n ligo -f environment.yml; \
	else \
		conda env create -f environment.yml; \
	fi

.PHONY: html
html:
	myst build --html

.PHONY: clean
clean:
	rm -rf figures/*
	rm -rf audio/*
	rm -rf _build/*