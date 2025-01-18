# main.py - Main program logic
import logging
import logging.handlers
import os
from datetime import datetime
import time
from bart_api import get_next_trains
from display import Display

def setup_logging():
    """Configure logging with monthly rotation."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "bart_clock.log")
    
    # Set up monthly rotating file handler
    handler = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when='MIDNIGHT',
        interval=30,  # Monthly rotation
        backupCount=12  # Keep a year of logs
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    root_logger.addHandler(console_handler)

def main():
    try:
        display = Display()
        while True:
            logging.info("Starting update cycle...")
            trains = get_next_trains()
            display.show_trains(trains)
            logging.info("Update cycle complete, sleeping for 1 minute...")
            time.sleep(60)  # Wait 1 minute before next update
            
    except KeyboardInterrupt:
        logging.info("Program terminated by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    setup_logging()
    main()

