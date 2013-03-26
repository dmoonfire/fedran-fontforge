"""Python class to generate a parametric font for the Fedran world."""


import ConfigParser
import fontforge
import logging
import os

import fedran.block0000


class FedranFont(object):
    def __init__(self):
        # Set up logging.
        self.log = logging.getLogger("font")

        # Initialize the common variables and properties
        self.initialize_metrics()

        # Set up the various unicode planes.
        self.glyphs = {}
        fedran.block0000.initialize_glyphs(self)

    def initialize(self, config):
        # Keep track of the INI file we're using
        self.config = config

        # Pull out the common fields.
        self.name = config['name']

    def initialize_metrics(self):
        # Set up the internal metrics.
        self.height_to_width = 1.618

    def add_glyph(self, glyph):
        self.glyphs[glyph.gid] = glyph

    def generate(self):
        """Goes through all the registered glyphs inside the font and
        generates each one."""

        # Create a new font.
        self.font = fontforge.font()

        # Go through the glyphs and generate each one. We display the
        # current status of the generation to the screen so we can see
        # something happening.
        total = len(self.glyphs)
        processed = 0

        for gid, glyph in self.glyphs.iteritems():
            processed += 1
            self.log.debug("  [{0:4}/{1:4}] Unicode {3:04x}: {2}".format(
                processed,
                total,
                glyph.label,
                glyph.gid))
            glyph.generate(self.font)

        # Finalize the font.
        self.font.fontname = self.name

    def save_ttf(self, filename):
        self.log.info("Generating TTF font: " + filename)
        self.font.generate(filename)

    def save_otf(self, filename):
        self.log.info("Generating OTF font: " + filename)
        self.font.generate(filename)

    def save_sfd(self, filename):
        self.log.info("Generating SFD font: " + filename)
        self.font.save(filename)
