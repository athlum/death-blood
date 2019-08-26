.PHONY: build
macos: clean
	cp setup.py.app setup.py
	python3 setup.py py2app
	rm -rf setup.py

clean:
	rm -rf ./build ./dist