.PHONY: build
macos:
	cp setup.py.app setup.py
	python3 setup.py py2app
	rm -rf setup.py