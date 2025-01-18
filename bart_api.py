# bart_api.py - Handles BART API calls
import logging
import requests
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Train:
    destination: str
    minutes: str

def get_next_trains() -> List[Train]:
    """Get next southbound yellow line trains from Rockridge."""
    url = "http://api.bart.gov/api/etd.aspx"
    params = {
        'cmd': 'etd',
        'orig': 'ROCK',
        'key': 'get from 1pass',
        'json': 'y'
    }
    
    try:
        logging.info("Fetching BART times from API...")
        response = requests.get(url, params=params)
        data = response.json()
        
        # Parse the response and get southbound yellow line trains
        trains = []
        etd = data['root']['station'][0]['etd']
        
        for destination in etd:
            dest_name = destination['destination']
            for estimate in destination['estimate']:
                if estimate['color'] == 'YELLOW' and estimate['direction'] == 'South':
                    minutes = estimate['minutes']
                    logging.info(f"Found train to {dest_name}: {minutes} min")
                    trains.append(Train(destination=dest_name, minutes=minutes))
        
        # Sort by minutes
        trains.sort(key=lambda x: int(x.minutes) if x.minutes.isdigit() else 999)
        return trains[:3]  # Get only next 3 trains
        
    except Exception as e:
        logging.error(f"Error fetching BART times: {e}")
        return []

