.PHONY: env
env:
	conda env update -n ligo -f environment.yml

.PHONY: html
html:
	myst build --html

.PHONY: clean
clean:
	rm -rf figures/*
	rm -rf audio/*
	rm -rf _build/*