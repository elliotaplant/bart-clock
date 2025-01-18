#!/usr/bin/python3
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from PIL import Image,ImageDraw,ImageFont
import logging
import time
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    from lib.waveshare_epd import epd2in13_V3
    
    epd = epd2in13_V3.EPD()
    logging.info("Init and Clear")
    epd.init()
    epd.Clear()
    
    # Create new image with white background
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    
    # Add text
    draw.text((10, 10), 'Hello, World!', fill=0)
    
    # Display image
    epd.display(epd.getbuffer(image))
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except Exception as e:
    logging.error(e)
    traceback.print_exc()
    exit()
