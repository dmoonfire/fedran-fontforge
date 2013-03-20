class FedranGlyph(object):
    """Class that represents a single glyphy (character) inside the
    font."""

    def __init__(self, font, gid, label):
        self.font = font
        self.gid = gid
        self.label = label

    def _get(name):
        """Internal method for getting property values inside the
        glphy. If the glphy does not have the property, then the value
        from the base font is used instead. In both cases, if the
        value is a method, it is called with no parameters before
        returning the results."""

        def get(self):
            # Try to get the value from the current glyph. If not,
            # then use the base so we have a common place for
            # settings.
            if var in self.__dict__:
                value = self.__dict__[name]
            else:
                value = self.base_font.__dict__[name]

            # If the resulting variable has a '__call__', then it is a
            # method. We call it with no parameters to resolve the
            # parameter.
            if hasattr(value, '__call__'):
                value = value(self)

            # Return the resulting variable.
            return value

    def _set(name):
        """Internal method for setting property values inside the
        glyph."""

        def set(self, value):
            self.__dict__[name] = value
        return set

    def generate(self, font):
        """Generates a single glyph inside the font."""

        glyph = font.createChar(self.gid, self.label)
        pen = glyph.glyphPen();
        pen.moveTo((100,100));
        pen.lineTo((100,200));
        pen.lineTo((200,200));
        pen.lineTo((200,100));
        pen.closePath();
        pen = None
