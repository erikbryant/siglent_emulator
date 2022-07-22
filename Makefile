dist: venv/bin/activate
	./venv/bin/python -m pip install --upgrade build
	./venv/bin/python -m build

venv/bin/activate: requirements.txt
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip
	./venv/bin/python -m pip install --upgrade black
	./venv/bin/python -m pip install --upgrade coverage
	./venv/bin/python -m pip install --upgrade mypy
	./venv/bin/python -m pip install --upgrade pylint
	./venv/bin/python -m pip install -r requirements.txt

test: venv/bin/activate
	./venv/bin/python -m coverage run --source=. -m unittest
	./venv/bin/python -m coverage report

static: venv/bin/activate
	./venv/bin/python -m pylint src/ tests/
	./venv/bin/python -m mypy src/ tests/
	./venv/bin/python -m black --target-version py310 src/ tests/

clean:
	find . -name "__pycache__" -type d -print0 | xargs -0 rm -rf
	rm -rf src/siglent_emulator.egg-info
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf docs
	rm -rf venv
	rm -f .coverage

# Targets that do not represent actual files
.PHONY: dist test static clean
