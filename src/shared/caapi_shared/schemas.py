from pydantic import BaseModel, Field
from typing import List


class ClaimInput(BaseModel):
    """
    User input for claimed disabilities.
    """

    claim_text: List[str] = Field(
        None,
        description="""
        An array of strings representing claimed disabilities. These will be classified on a per-disability basis in the output.
        """,
    )


class Classification(BaseModel):
    """
    Attributes that correspond to the VA classification code for this claimed disability.
    """

    text: str = Field(
        None, description="Text associated with the classified response code"
    )
    code: str = Field(None, description="The VA classification response code")
    confidence: float = Field(
        None, description="The confidence percentage of the prediction"
    )


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
    Represents a single claimed disability from the original list
    """

    originalText: str = Field(
        None, description="The original text of the inputted claimed disability"
    )
    classification: Classification = Field(
        None, description="The VA classification code for this claimed disability"
    )
    flashes: List[Flash] = Field(
        None,
        description="List of flashes that may apply based on disabilities claimed.",
    )
    specialIssues: List[SpecialIssue] = Field(
        None,
        description="A list of special issues that may apply based on the disabilities claimed",
    )


class Prediction(BaseModel):
    """
    Represents a per-claim response to a list of claimed disability inputs
    """

    contentions: List[Contention] = Field(
        None,
        description="""Lists all inputted claimed disabilities and related data for each""",
    )

class SpecialIssueServiceOutput(BaseModel):
    """
    Represents the output of a call to the Special Issue Service
    """

    special_issues: List[List[SpecialIssue]] = Field(
        None,
        description="""A list of special issues that may apply based on the disabilities claimed""",
    )

class FlashesServiceOutput(BaseModel):
    """
    Represents the output of a call to the Flashes Service
    """

    flashes: List[List[SpecialIssue]] = Field(
        None,
        description="""A list of flashes that may apply based on the disabilities claimed""",
    )

class ClassifierServiceOutput(BaseModel):
    """
    Represents the output of a call to the Classifier Service
    """

    classifications: List[Classification] = Field(
        None,
        description="""A list of classifications that may apply based on the disabilities claimed""",
    )

