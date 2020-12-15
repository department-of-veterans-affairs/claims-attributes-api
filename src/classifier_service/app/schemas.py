from pydantic import BaseModel, Field
from typing import List


class Classification(BaseModel):
    """
    Attributes that correspond to the
    VA classification code for this claimed disability.
    """

    text: str = Field(
        None, description="Text associated with the classified response code"
    )
    code: str = Field(None, description="The VA classification response code")
    confidence: float = Field(
        None, description="The confidence percentage of the prediction"
    )


class ClaimInput(BaseModel):
    """
    User input for claimed disabilities.
    """

    claim_text: List[str] = Field(
        None,
        description="""
        An array of strings representing claimed disabilities. 
        These will be classified on a per-disability basis in the output.
        """,
    )