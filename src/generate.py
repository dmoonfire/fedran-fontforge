#!/usr/bin/env python
import sys

import fedran

def generate(args):
    # Loop through all the remaining arguments which should be just
    # INI files.
    for ini_file in args:
        # Create the font description from the INI file.
        font = fedran.FedranFont()
        font.initialize(ini_file)

        # Generate the font.
        font.generate()


if __name__ == "__main__":
    generate(sys.argv[1:])
