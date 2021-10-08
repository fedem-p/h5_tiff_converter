.PHONY: docs

docs:
		rm -rf notebooks/_build/html
		find notebooks/api ! -name 'index.rst' -type f -exec rm -f {} +
		pip install -r notebooks/requirements.txt
		pip install H5-2-Tiff-Converter
		jb build notebooks
