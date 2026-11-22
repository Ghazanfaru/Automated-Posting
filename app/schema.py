import re
from datetime import date, time
from typing import Literal

from pydantic import(
BaseModel,
Field,
HttpUrl,
TypeAdapter,
field_validator
)

class PostingRequest(BaseModel):


    message: str = Field(
        ...,
        min_length = 1,
        max_length = 200,
        description = "Message to publish across platforms"
    )
    
    @field_validator("message")

    @classmethod
    def validate_message(cls,value:str) -> str :
         
         # Find all HTTP/HTTPS URLs

         urls = re.findall(
              r"https?://[^\s]+",
              value
         )

         # Exactly one URL is required

         if len(urls) != 1:
              raise ValueError(
                   "Message must contain exactly one URL"
              )
         
         # Remove common trailing punctuation

         url = urls[0].rstrip(".,!?;:)]}")

         #validate URL format

         try:
              TypeAdapter(HttpUrl).validate_python(url)
         except Exception:
              raise ValueError("Invalid URL provided")
         return value

class PlatformResult(BaseModel):
     platform : str
     status : Literal["success","failed"]
     posted_url : str | None = None
     public_access: bool = False
     d: date | None = None
     t : time | None = None
     error : str | None = None


class PostingResponse(BaseModel):
     success : bool
     results : list [PlatformResult]

