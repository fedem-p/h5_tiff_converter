.PHONY: docs

docs:
		rm -rf notebooks/_build/html
		find notebooks/api ! -name 'index.rst' -type f -exec rm -f {} +
		pip install -r notebooks/requirements.txt
		pip install -r requirements.txt
		pip install h5tiff
		pip install -e .
		jupyter-book build notebooks/
