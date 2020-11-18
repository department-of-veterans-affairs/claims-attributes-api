from pydantic import BaseModel, Field
from typing import List


class ClaimInput(BaseModel):
    """
    User Input for claims data
    """
    claim_text: List[str] = Field(
        None, description="""
        An array of strings representing claims text. These will be classified
        independently and summarized in the output
        """
    )


class Classification(BaseModel):
    """
    Attributes that correspond to the service-connected condition
    """
    text: str = Field(
        None, description="Text associated with the classified response code")
    code: str = Field(None, description="The classified response code")
    confidence: float = Field(
        None, description="The confidence percentage of the prediction")


class Flash(BaseModel):
    """
    Represents attributes appended to a claim that are related to the claimant.
    """
    text: str = Field(None, description="Flash text")


class SpecialIssue(BaseModel):
    """
    Represents attributes appended to a claim that are related to the type of claim.
    """
    text: str = Field(None, description="Special issue text")


class Contention(BaseModel):
    """
    Represents a single contention from the original list
    """
    originalText: str = Field(None, description="The originally input text")
    classification: Classification = Field(
        None, description="The classification of this text")
    flashes: List[Flash] = Field(
        None, description="A list of flashes found in this claim")
    specialIssues: List[SpecialIssue] = Field(
        None, description="A list of special issues found in this claim")


class Prediction(BaseModel):
    """
    Represents a per-claim response to a list of claims-text inputs
    """
    contentions: List[Contention] = Field(
        None, description="""A list of contentions, one per inputted claim text""")
