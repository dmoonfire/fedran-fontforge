#!/usr/bin/env python
import fontforge

# Create a new font.
font = fontforge.font()

glyph = font.createChar(65, "A")
pen = glyph.glyphPen();
pen.moveTo((100,100));
pen.lineTo((100,200));
pen.lineTo((200,200));
pen.lineTo((200,100));
pen.closePath();
pen = None

glyph = font.createChar(66, "B")
pen = glyph.glyphPen();
pen.moveTo((100,100));
pen.lineTo((100,200));
pen.lineTo((200,100));
pen.closePath();
pen = None

print len(font)

#font.save("test.sfd")
font.selection.select(("ranges",None),"A","A")
font.autoHint()

print font["A"].foreground

font.fontname = "Fedran"
font.generate("../build/Fedran-Miwafu.ttf")
