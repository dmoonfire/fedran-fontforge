"""Implements the rendering of the Unicode Block 000 (Basic Latin)."""


import fedran.glyph


def initialize_glyphs(font):
    font.add_glyph(G0048(font))
    font.add_glyph(G004F(font))
    font.add_glyph(G006E(font))
    font.add_glyph(G006F(font))


class G0048(fedran.glyph.FedranGlyph):
    def __init__(self, font):
        super(G0048, self).__init__(font, 0x0048, 'LATIN CAPITAL LETTER H')


class G004F(fedran.glyph.FedranGlyph):
    def __init__(self, font):
        super(G004F, self).__init__(font, 0x004F, 'LATIN CAPITAL LETTER O')


class G006E(fedran.glyph.FedranGlyph):
    def __init__(self, font):
        super(G006E, self).__init__(font, 0x006E, 'LATIN SMALL LETTER N')


class G006F(fedran.glyph.FedranGlyph):
    def __init__(self, font):
        super(G006F, self).__init__(font, 0x006F, 'LATIN SMALL LETTER O')
