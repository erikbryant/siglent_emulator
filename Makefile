dist:
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
	./venv/bin/python -m pylint siglent_emulator/
	./venv/bin/python -m mypy siglent_emulator/
	./venv/bin/python -m black --target-version py310 siglent_emulator/

clean:
	rm -rf __pycache__
	rm -f dist/*

# Targets that do not represent actual files
.PHONY: dist test static clean
