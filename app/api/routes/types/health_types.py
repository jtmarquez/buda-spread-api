from pydantic import BaseModel


class GetHealthResponseType(BaseModel):
    health_status: str
