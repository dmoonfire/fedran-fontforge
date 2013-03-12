all: generate

clean:
	rm -rf ../build/

# Generate all of the font files.
generate:
	mkdir -p ../build/
	./generate.py

# Used to install the requirements in a Debian-based system.
install-requirements:
	sudo apt-get install fontforge python-fontforge