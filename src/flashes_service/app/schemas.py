from pydantic import BaseModel, Field
from typing import List


class Flash(BaseModel):
    """
    Represents attributes appended to a claim that are related to the claimant.
    """

    text: str = Field(None, description="Flash text")