from typing import List

from pydantic import BaseModel, Field


class VectorizerOutput(BaseModel):

    vectorized_text: List[List[int]] = Field(
        None, description="""Text vectorized using a Scikit-Learn CountVectorizer"""
    )
