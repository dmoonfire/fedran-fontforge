"""Python class to generate a parametric font for the Fedran world."""


import fontforge
import ConfigParser

import fedran.block0000


class FedranFont(object):
    def __init__(self):
        # Initialize the common variables and properties
        self.initialize_metrics()

        # Set up the various unicode planes.
        self.glyphs = {}
        fedran.block0000.initialize_glyphs(self)

    def initialize(self, ini_file):
        # Keep track of the INI file we're using
        self.ini_file = ini_file

        # Parse the INI file so we can pull out the elements needed.
        config = ConfigParser.ConfigParser()
        config.read(ini_file)

        # Pull out the common fields.
        self.name = config.get('Font', 'name')
        self.filename = config.get('Font', 'filename')

    def initialize_metrics(self):
        # Set up the internal metrics.
        self.height_to_width = 1.618

    def add_glyph(self, glyph):
        self.glyphs[glyph.gid] = glyph

    def generate(self):
        """Goes through all the registered glyphs inside the font and
        generates each one."""

        # Create a new font.
        font = fontforge.font()

        # Go through the glyphs and generate each one. We display the
        # current status of the generation to the screen so we can see
        # something happening.
        total = len(self.glyphs)
        processed = 0

        for gid, glyph in self.glyphs.iteritems():
            processed += 1
            print "[{0:4}/{1:4}] Unicode {3:04x}: {2}".format(
                processed,
                total,
                glyph.label,
                glyph.gid)
            glyph.generate(font)

        # Finalize the font.
        font.fontname = self.name
        font.generate("../build/" + self.filename + ".ttf")
