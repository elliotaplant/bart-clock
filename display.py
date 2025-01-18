# display.py - Handles e-Paper display
import logging
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from typing import List
from bart_api import Train

class Display:
    def __init__(self):
        from lib.TP_lib import epd2in13_V3
        self.epd = epd2in13_V3.EPD()
        self.font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        self.font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

    def show_trains(self, trains: List[Train]) -> None:
        """Display the trains on the e-Paper display."""
        try:
            logging.info("Initializing e-Paper...")
            self.epd.init(0)
            self.epd.Clear(0xFF)
            
            # Create new blank image for drawing
            image = Image.new('1', (self.epd.height, self.epd.width), 255)
            draw = ImageDraw.Draw(image)
            
            # Draw title
            draw.text((5, 5), "Next SF Trains:", font=self.font_large, fill=0)
            
            # Draw train times
            y_position = 30
            if trains:
                for train in trains:
                    text = f"{train.destination}: {train.minutes}min"
                    draw.text((5, y_position), text, font=self.font_large, fill=0)
                    y_position += 25
            else:
                draw.text((5, y_position), "No trains found", font=self.font_large, fill=0)
            
            # Draw last updated time at bottom
            current_time = datetime.now().strftime("%I:%M %p")
            draw.text((5, 100), f"Updated: {current_time}", font=self.font_small, fill=0)
            
            # Display the image
            logging.info("Displaying BART times...")
            self.epd.display(self.epd.getbuffer(image))
            
            # Put display to sleep
            logging.info("Done! Putting display to sleep...")
            self.epd.sleep()
            
        except Exception as e:
            logging.error(f"Error updating display: {e}")
            raise

