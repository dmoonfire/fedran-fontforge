import fedran


class FedranGlyph(object):
    """Class that represents a single glyphy (character) inside the
    font."""

    def __init__(self, parent, gid, label):
        self.parent = parent
        self.gid = gid
        self.label = label
        self.values = fedran.LookupDictionary(parent.values)

    # baseline = _prop("baseline")
    # bottom_line_gap = _prop("bottom_line_gap")
    # top_line_gap = _prop("top_line_gap")
    # line_gap = _prop("line_gap")
    # em = _prop("em")
    # ascent = _prop("ascent")
    # descent = _prop("descent")
    # cap_height = _prop("cap_height")
    # mean_height = _prop("mean_height")

    def generate(self, font):
        """Generates a single glyph inside the font."""

        # Create the font and set up the initial pen.
        glyph = font.createChar(self.gid, self.label)
        pen = glyph.glyphPen();

        # Have the glyph draw itself.
        self.draw(self.values, font, glyph, pen)

        # Clean out the pen so FontForge releases all the resources.
        pen = None

        glyph.right_side_bearing = 100

    #@abstract
    def draw(self, values, font, glyph, pen):
        pass
