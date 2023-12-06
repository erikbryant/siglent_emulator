venv/bin/activate: requirements.txt
	python3 -m venv venv
	venv/bin/python -m pip install -r requirements.txt

sdist: venv/bin/activate
	venv/bin/python -m pip install --upgrade build
	venv/bin/python -m build

test: venv/bin/activate
	venv/bin/python -m tox

pylint: venv/bin/activate
	venv/bin/python -m pylint src/ tests/

mypy: venv/bin/activate
	venv/bin/python -m mypy src/ tests/

black: venv/bin/activate
	venv/bin/python -m black --target-version py312 $(CHECK_FLAGS) src/ tests/

all: pylint mypy black test

sdg1032x: venv/bin/activate
	venv/bin/python src/siglent_emulator_verifier.py ${IP} ${PORT}

clean:
	find . -name "__pycache__" -type d -print0 | xargs -0 rm -rf
	rm -rf src/siglent_emulator.egg-info
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf docs
	rm -rf venv
	rm -f .coverage

# Targets that do not represent actual files
.PHONY: sdist test pylint mypy black all sdg1032x clean
