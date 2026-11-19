from pydantic import BaseModel, Field
from Inconsistency import Inconsistency
from typing import List
class InconsistencyReport(BaseModel):
    inconsistencies: List[Inconsistency] = Field(description="A list of inconsistencies found in the csv")
    