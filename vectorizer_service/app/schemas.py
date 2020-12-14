from pydantic import BaseModel, Field
from typing import List


class VectorizerOutput(BaseModel):
    """
    Vectorized Text
    """

    vectorized_text: List[List[int]] = Field(
        None, description="""Text vectorized using a Scikit-Learn CountVectorizer"""
    )
