"""Python class to generate a parametric font for the Fedran world."""


import ConfigParser
import fontforge
import logging
import os

import fedran.block0000


class LookupDictionary(object):
    def __init__(self, parent):
        object.__setattr__(self, "parent", parent)
        object.__setattr__(self, "values", {})

    def __getattr__(self, key):
        # If we have the key inside ourselves, then grab
        # that. Otherwise, grab it from the parent.
        values = object.__getattribute__(self, "values")

        if key in values:
            value = values[key]
        else:
            # Try finding it in the parent object. If we can't find a
            # parent, then we just return None.
            parent = self.parent

            if parent is None: return None

            value = parent.__getattr__(key)

        # If we have a none at this point, then just return None.
        if value is None: return None

        # At this point, we have a value. If the value is callable,
        # then we need to resolve it as a function.
        if hasattr(value, '__call__'):
            value = value(self)

        # Return the resulting value.
        return value

    def __setattr__(self, key, value):
        self.values[key] = value

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
        self.values = LookupDictionary(None)
        v = self.values

        # The em width is hard-coded to 1000. This is also the line
        # height.
        v.em = 1000

        # The basic framing vertical metrics are the ascent (the part
        # above the baseline where the glyphs go), the descent (the
        # part below the baseline for the glyphs, expressed as
        # negatives), and a line gap which is separated into a top and
        # bottom line gap.
        v.ascent = lambda g: (0.6 * g.em)
        v.descent = lambda g: (-0.3 * g.em)
        v.top_line_gap = lambda g: (g.em - g.ascent + g.descent) / 2
        v.bottom_line_gap = lambda g: (
            g.em - g.top_line_gap - g.ascent + g.descent)
        v.line_gap = lambda g: (g.top_line_gap + g.bottom_line_gap)

        # The baseline is determined by the bottom line gap minus the
        # descent. Most of the measurements are based on baseline
        # calculations.
        v.baseline = lambda g: (g.bottom_line_gap - g.descent)

        # The mean height (roughly the x-height) is the top-point of
        # the lowercase letters while the cap height is the height of
        # the capital letters and lowercase ascenders.
        v.mean_height = lambda g: (g.ascent * 0.6)
        v.cap_height = lambda g: (g.ascent * 0.8)

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
