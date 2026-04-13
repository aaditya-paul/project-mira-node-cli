from typing import Optional

from pydantic import BaseModel, Field


class ActionPlan(BaseModel):
    type: str = Field(
        description="Whether the model is returning a tool action or plain text response."
    )
    tool: Optional[str] = Field(
        default=None,
        description="Tool name when type is 'tool', otherwise null.",
    )
    args: Optional[dict] = Field(
        default=None,
        description="Tool arguments when type is 'tool', otherwise null.",
    )
    response: Optional[str] = Field(
        default=None,
        description="Text response when type is 'text', otherwise null.",
    )
