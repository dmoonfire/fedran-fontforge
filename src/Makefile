all: generate

clean:
	rm -rf ../build/

# Generate all of the font files.
generate: ../build/Fedran-Miwafu.ttf

../build/Fedran-Miwafu.ttf: generate.py fedran-miwafu.ini
	mkdir -p ../build/
	./generate.py fedran-miwafu.ini

# Used to install the requirements in a Debian-based system.
install-requirements:
	sudo apt-get install fontforge python-fontforge
