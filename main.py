import sys
import os
import logging
import time
from display import Display
from bart_api import get_next_trains
from PIL import Image,ImageDraw,ImageFont

# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)

from lib.TP_lib import epd2in13_V3
from lib.TP_lib import gt1151

logging.basicConfig(level=logging.DEBUG)

try:
    # Display init
    epd = epd2in13_V3.EPD()
    touch = gt1151.GT1151()
    touch_dev = gt1151.GT_Development()
    touch_old = gt1151.GT_Development()
    
    # Init touch and display
    logging.info("Initializing...")
    touch.GT_Init()
    epd.init(0)
    epd.Clear(0xFF)
    
    # Create initial image
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    
    # Draw initial text
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    draw.text((10, 10), "Touch anywhere...", font=font, fill=0)
    epd.display(epd.getbuffer(image))
    
    last_update = 0
    last_x = 0
    last_y = 0
    
    # Touch detection loop
    while True:
        display = Display()
        touch_dev.Touch = 1
        touch.GT_Scan(touch_dev, touch_old)
        
        current_time = time.time()
        
        # Only update if touch detected and at least 2 seconds since last update
        if touch_dev.TouchpointFlag and current_time - last_update > 2:
            # Only update if position has changed significantly
            if abs(touch_dev.X[0] - last_x) > 5 or abs(touch_dev.Y[0] - last_y) > 5:
                logging.info(f"Touch detected at: ({touch_dev.X[0], touch_dev.Y[0]})")
                logging.info("Storing touch time, coords")
                last_update = current_time
                last_x = touch_dev.X[0]
                last_y = touch_dev.Y[0]
                logging.info("Fetching train data")
                trains = get_next_trains()
                logging.info("Displaying result")
                display.show_trains(trains)
                logging.info("Complete")
        
        time.sleep(1)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd.sleep()
    exit()
