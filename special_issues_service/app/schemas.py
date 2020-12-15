from pydantic import BaseModel, Field
from typing import List


class SpecialIssue(BaseModel):
    """
    Represents attributes appended to a claim that are related to the type of claim.
    """

    text: str = Field(None, description="Special issue text")