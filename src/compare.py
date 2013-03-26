#!/usr/bin/env python


"""Command-line utility for generating a comparison of various
parameters in the font and displaying them in a single graphic with
labels."""


import argparse
import logging
import mfgames_tools
import mfgames_tools.process
import os
import shutil
import subprocess
import sys
import tempfile
import yaml

import fedran


class CompareTool(mfgames_tools.process.InputFileProcess):
    """A process that takes an input file to process and generates an
    output image file."""

    def setup_arguments(self, parser):
        # Call the base implementation for common parameters.
        super(CompareTool, self).setup_arguments(parser)

        # Set up the required command-line options.
        parser.add_argument(
            'image',
            type=str,
            help="Output image filename")

        parser.add_argument(
            '--renderer',
            type=str,
            default='harfbuzz',
            choices=['harfbuzz', 'imagemagick'],
            help="Determines rendering engine for the output text.")

    def get_help(self):
        return "Generate a comparison image for generated fonts"

    def create_text_image(
            self,
            text,
            background_color, foreground_color,
            font_filename, font_size,
            output_filename):
        # If we are using Harfbuzz (which handles kerning better than
        # ImageMagic), we need to use `hb-view` to generate the
        # output.
        if self.args.renderer == "harfbuzz":
            subprocess.call(
                ["hb-view",
                 "--font-size=" + format(font_size),
                 "--background=" + background_color,
                 "--foreground=" + foreground_color,
                 "--output-file=" + output_filename,
                 "--output-format=png",
                 "--margin=0",
                 font_filename,
                 text])

        if self.args.renderer == "imagemagick":
            subprocess.call(
                ["convert",
                 "-background", background_color,
                 "-fill", foreground_color,
                 "-stroke", foreground_color,
                 "-font", font_filename,
                 "-pointsize", format(font_size),
                 "-gravity", "South",
                 "label:" + text,
                 output_filename])

    def process_file(self, config_filename):
        # Get the logging context and report that we're doing something.
        self.log = logging.getLogger('compare')
        self.log.info("Generating comparison from " + self.args.file)

        # Grab the configuration file and parse it.
        config_stream = file(config_filename, 'r')
        self.config = yaml.load(config_stream)
        
        # Figure out how many rows an columns we'll be generating.
        rows = len(self.config['y-axis'])
        columns = len(self.config['x-axis'])

        self.log.info(
            "Generating {0} rows by {1} columns".format(rows, columns))

        # Create a temporary directory for the output.
        self.dirname = tempfile.mkdtemp(prefix='fedran-compare-')
        self.log.debug('Using temporary directory: ' + self.dirname)

        # Generate one font for every row and column combination. This
        # will have a consistent naming convention (font-RxC.ttf).
        cell_images = []
            
        for row in range(rows):
            # Go through the columns and generate each image.
            for column in range(columns):
                # Create the font and put it into the temporary
                # directory.
                self.generate_font(row, column)

                # Create a thumbnail of the font.
                cell_filename = self.generate_cell_image(row, column)
                cell_images.append(cell_filename)

        # Generate the file row images.
        self.generate_image(cell_images)

        # Clean up the temporary files.
        shutil.rmtree(self.dirname)
        self.log.debug('Cleaned up temporary directory')

    def generate_font(self, row, column):
        """Generates a single font using the information from a given
        row and column to produce the results. The name of the font is
        always "font-RxC.ttf" and will be placed in the temporary
        directory."""

        # Figure out the filename we'll be creating.
        filename = "font-{0}x{1}.ttf".format(row, column)
        self.log.debug("Generating {0}".format(filename))

        # Create the font object and initialize it with both the font,
        # row, and column information.
        font = fedran.FedranFont()
        #font.initialize(config)
        #font.initialize(config['x-axis'][column])
        #font.initialize(config['y-axis'][row])

        # Override the name of the font in case it is missing.
        font.name = "Comparison{0}{1}".format(row, column)

        # Generate the font using FontForge.
        font.generate()

        # Write out the TTF font which we'll use with ImageMagick.
        filename = "font-{0}x{1}.ttf".format(row, column)
        font.save_ttf(os.path.join(self.dirname, filename))

    def generate_cell_image(self, row, column):
        """Create a thumbnail image of the given font with the label
        requested."""

        # Figure out all the paths we need.
        basename = "font-{0}x{1}".format(row, column)
        fontname = basename + ".ttf"
        fontpath = os.path.join(self.dirname, fontname)
        text_filepath = os.path.join(self.dirname, basename + "-text.png")
        label1_filepath = os.path.join(self.dirname, basename + "-1-label.png")
        label2_filepath = os.path.join(self.dirname, basename + "-2-label.png")
        image_filepath = os.path.join(self.dirname, basename + ".png")

        text = self.config['text']
        label1 = self.config['x-axis'][column]['label']
        label2 = self.config['y-axis'][row]['label']

        font_size = self.config['font-size']
        label_size = self.config['label-size']
        label_font = self.config['label-font']

        background_color = "#F5DEB3"

        # Create the label in the given text and size. Allow for
        # switching rendering engines while generating the results.
        self.create_text_image(
            text,
            background_color, "#24201A",
            fontpath, font_size,
            text_filepath)            
        self.create_text_image(
            label1,
            background_color, "#786D57",
            label_font, label_size,
            label1_filepath)            
        self.create_text_image(
            label2,
            background_color, "#786D57",
            label_font, label_size,
            label2_filepath)            

        subprocess.call(
            ["convert",
             text_filepath,
             label1_filepath,
             label2_filepath,
             "-gravity", "center",
             "-background", background_color,
             "-append",
             image_filepath])
        
        # Return the resulting filepath so we can combine it.
        return image_filepath

    def generate_image(self, images):
        # Figure out all the paths we need.
        filepath = self.args.image

        # Create a row image from the cell images using ImageMagick's
        # `montage` program.
        rows = len(self.config['y-axis'])
        columns = len(self.config['x-axis'])
        background_color = "#F5DEB3"
        x_margin = self.config['x-margin']
        y_margin = self.config['y-margin']

        args = ['montage']
        args.extend(images)
        args.extend(
            ["-background", background_color,
             "-geometry", "+{0}+{1}".format(x_margin, y_margin),
             "-tile", "{1}x{0}".format(rows, columns),
             filepath])
        print args

        subprocess.call(args)

        # Return the resulting filename.
        return filepath


def generate_comparison(tool_args):
    """Generates a comparison from the first argument, an INI file,
    and writes out the resulting image to the second argument, the
    name of an image file."""

    # Set up logging with a timestamp.
    FORMAT = '%(asctime).19s %(message)s'
    logging.basicConfig(
        format=FORMAT,
        level=logging.DEBUG)

    # Create a comparison tool and parse the arguments.
    parser = argparse.ArgumentParser()

    compare = CompareTool()
    compare.setup_arguments(parser)

    args = parser.parse_args(tool_args)

    # Process the single file input.
    compare.process(args)


#
# Entry Point
#

if __name__ == "__main__":
    generate_comparison(sys.argv[1:])
