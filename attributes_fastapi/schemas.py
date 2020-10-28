from pydantic import BaseModel, Field
from typing import List


class ClaimInput(BaseModel):
    """
    Input for claims data
    """
    claim_text: List[str] = Field(
        None, description="""
        An array of strings representing claims text. These will be classified
        independently and summarized in the output
        """
    )


class Classification(BaseModel):
    text: str = Field(
        None, description="Text associated with the classified response code")
    code: str = Field(None, description="The classified response code")
    confidence: float = Field(
        None, description="The confidence percentage of the prediction")


class Flash(BaseModel):
    text: str = Field(None, description="Flash text")


class SpecialIssue(BaseModel):
    text: str = Field(None, description="Special issue text")


class Contention(BaseModel):
    originalText: str = Field(None, description="The originally input text")
    classification: Classification = Field(
        None, description="The classification of this text")
    flashes: List[Flash] = Field(
        None, description="A list of flashes found in this claim")
    specialIssues: List[SpecialIssue] = Field(
        None, description="A list of special issues found in this claim")


class Prediction(BaseModel):
    contentions: List[Contention] = Field(
        None, description="""A list of contentions, one per inputted claim text""")
    flashes: List[Flash] = Field(
        None, description="""A list of flashes, representing the union of
         flashes for all claims""")
    specialIssues: List[SpecialIssue] = Field(
        None, description="""A list of special issues, representing the union
         of special issues for all claims""")
