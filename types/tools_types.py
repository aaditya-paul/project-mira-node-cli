from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Parameters(BaseModel):
    type: str
    properties: Dict[str, Any]
    required: List[str]

class Tool(BaseModel):
    name: str
    description: str
    parameters: Parameters