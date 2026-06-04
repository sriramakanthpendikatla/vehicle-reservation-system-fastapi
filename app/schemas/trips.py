from pydantic import BaseModel
from datetime import datetime

class TripCheckout(BaseModel):
    reservation_id:int
    fuel_level_before:int
    expected_end_time :datetime
    
    

class TripCheckin(BaseModel):
     trip_id:int
     end_odometer:int
     fuel_level_after:int
