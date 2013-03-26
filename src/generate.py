#!/usr/bin/env python


"""Generation script that takes a INI file that describes a font and
generates the appropriate OTF, TTF, or SDF as needed."""


import argparse
import logging
import mfgames_tools
import mfgames_tools.process
import sys
import yaml

import fedran


class GenerateTool(mfgames_tools.process.InputFileProcess):
    """A process that takes a description of font metrics and
    generates the appropriate output."""

    def setup_arguments(self, parser):
        # Call the base implementation for common parameters.
        super(GenerateTool, self).setup_arguments(parser)

        # Set up the required command-line options.
        parser.add_argument(
            '--directory',
            type=str,
            help="Output directory for resulting fonts")

        parser.add_argument(
            '--ttf',
            help="Generate a TTF font")
        parser.add_argument(
            '--otf',
            help="Generate a OTF font")
        parser.add_argument(
            '--sfd',
            help="Generate a SFD font")

    def get_help(self):
        return "Generate fonts from a font description file"

    def process_file(self, config_filename):
        # Get the logging context and report that we're doing something.
        self.log = logging.getLogger('generate')
        self.log.info("Generating font from " + config_filename)

        # Create the font description from the YAML configuration file.
        config_stream = file(config_filename, 'r')
        config = yaml.load(config_stream)

        font = fedran.FedranFont()
        font.initialize(config)

        # Generate the font in memory.
        font.generate()

        # Figure out where we'll be writing the files.
        directory = self.args.directory
        if directory is None: directory = os.path.dirname(file)

        self.log.debug("Writing files out to " + directory)

        # Write out the resulting fonts.
        if self.args.ttf is not None:
            font.save_ttf(self.args.ttf)

        if self.args.otf is not None:
            font.save_otf(self.args.otf)

        if self.args.sfd is not None:
            font.save_sfd(self.args.sfd)


def generate(tool_args):
    # Set up logging with a timestamp.
    FORMAT = '%(asctime).19s %(message)s'
    logging.basicConfig(
        format=FORMAT,
        level=logging.DEBUG)

    # Set up the generation tool (which has some common functionality)
    # and use that to parse the input.
    parser = argparse.ArgumentParser()

    generate = GenerateTool()
    generate.setup_arguments(parser)

    args = parser.parse_args(tool_args)

    # Process the single file input.
    generate.process(args)


if __name__ == "__main__":
    generate(sys.argv[1:])
