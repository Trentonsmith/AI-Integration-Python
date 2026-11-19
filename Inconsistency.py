from pydantic import BaseModel, Field
from Issue import Issue
from typing import List
class Inconsistency(BaseModel):
    line_nums: List[int] = Field(description="Line numbers of the inconsistency, line 1 being the header row")
    category: Issue = Field(description="The type of issue that is being announced")
    evidence: str = Field(description="The raw data from the csv that shows the issue")
    description: str = Field(description="A brief description of why this data inconsistency could be an issue")
