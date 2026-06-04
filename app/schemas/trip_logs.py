from pydantic import BaseModel

class CreateTriplogs(BaseModel):
    reservation_id :int

class TriplogsResponse(BaseModel):
    reservation_id : int

