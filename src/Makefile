#
# Common
#

# This contains all the classes that make up the system for purposes
# of generating fonts. If any of these change, then all fonts need to
# be regenerated.
PYTHON_REQUIREMENTS = $(wildcard fedran/*.py) generate.py Makefile

FONTS_YAML = $(wildcard fonts/*.yaml)
FONTS_TTF = $(addprefix ../build/,$(subst fonts/,,$(FONTS_YAML:yaml=ttf)))
FONTS_OTF = $(FONTS_TTF:ttf=otf)
FONTS_SFD = $(FONTS_TTF:ttf=sfd)

COMPARISONS_YAML = $(wildcard comparisons/*.yaml)
COMPARISONS_PNG = $(addprefix ../build/,$(COMPARISONS_YAML:yaml=png))

#
# Primary Targets
#

all: generate

clean:
	rm -rf ../build/

# Generate all of the font files.
generate: $(FONTS_TTF) $(FONTS_OTF) $(FONTS_SFD)

../build/%.ttf: generate.py fonts/%.yaml
	mkdir -p ../build/
	./generate.py fonts/$*.yaml --ttf=../build/$*.ttf --otf=../build/$*.otf --sfd=../build/$*.sfd --directory=../build

../build/%.otf: ../build/%.ttf

../build/%.sfd: ../build/%.ttf

# Preview
preview: ../build/Fedran.pdf

../build/Fedran.pdf: ../build/Fedran.ttf
	mfgames-font unicode-chart ../build/Fedran.ttf ../build/Fedran.pdf > /dev/null

#
# Comparisons
#
# Comparisons are PNG images that are generated from a corresponding
# YAML file which compares different values of parameters against each
# other in a X by Y grid. The YAML file determines the parameters that
# are compared to each other and combines a row and column's
# parameters into a single set before generating the font.

compare: $(COMPARISONS_PNG)

../build/comparisons/%.png: comparisons/%.yaml $(PYTHON_REQUIREMENTS) compare.py
	mkdir -p ../build/comparisons
	./compare.py --renderer=harfbuzz comparisons/$*.yaml ../build/comparisons/$*.png

#
# Requirements
#

# Used to install the requirements in Debian-based systems.
install-requirements:
	sudo apt-get install fontforge python-fontforge python-yaml imagemagick libharfbuzz-bin fonts-freefont-ttf
