# touch_handler.py - Handles touch input monitoring
import logging
import sys
import os
from lib.TP_lib import gt1151
import time

class TouchHandler:
    def __init__(self):
        self.touch = gt1151.GT1151()
        self.touch_dev = gt1151.GT_Development()
        self.touch_old = gt1151.GT_Development()

        logging.info("Initializing touch controller...")
        self.touch.GT_Init()

    def wait_for_touch(self) -> tuple[int, int]:
        """
        Blocks until touch is detected, then returns touch coordinates.
        Returns (x, y) coordinates of touch point.
        """
        self.touch_dev.Touch = 1
        last_x = 0
        last_y = 0

        while True:
            self.touch.GT_Scan(self.touch_dev, self.touch_old)

            # Only consider it a touch if:
            # 1. TouchpointFlag is set
            # 2. Coordinates are non-zero
            # 3. Coordinates have changed significantly from last position
            if (self.touch_dev.TouchpointFlag and
                self.touch_dev.X[0] > 0 and
                self.touch_dev.Y[0] > 0 and
                (abs(self.touch_dev.X[0] - last_x) > 5 or
                 abs(self.touch_dev.Y[0] - last_y) > 5)):

                x, y = self.touch_dev.X[0], self.touch_dev.Y[0]
                last_x = x
                last_y = y
                logging.info(f"Touch detected at ({x}, {y})")
                return (x, y)

            time.sleep(0.1)  # Short sleep to prevent busy-waiting
