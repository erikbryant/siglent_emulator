venv/bin/activate: requirements.txt
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip
	./venv/bin/python -m pip install black
	./venv/bin/python -m pip install coverage
	./venv/bin/python -m pip install mypy
	./venv/bin/python -m pip install pylint
	./venv/bin/python -m pip install -r requirements.txt

test: venv/bin/activate
	./venv/bin/python -m coverage run --source=. -m unittest
	./venv/bin/python -m coverage report

static: venv/bin/activate
	./venv/bin/python -m pylint src/siglent_emulator/
	./venv/bin/python -m mypy src/siglent_emulator/
	./venv/bin/python -m black --target-version py310 src/siglent_emulator/

clean:
	rm -rf __pycache__

# Targets that do not represent actual files
.PHONY: test static clean
