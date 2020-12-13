from pydantic import BaseModel

class VectorizerOutput(BaseModel):
    """
    Vectorized Text
    """
    vectorized_text: [str] = Field(
        None, description="""Text vectorized using a Scikit-Learn CountVectorizer"""
    )