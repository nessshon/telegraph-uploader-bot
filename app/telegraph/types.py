from __future__ import annotations

from pydantic import Field, BaseModel, validator

from . import config


class File(BaseModel):
    url: str = Field(..., alias="src")

    @validator("url")
    def url_validator(cls, value: str):
        return config.BASE_URL.format(endpoint=value)
