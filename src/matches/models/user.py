from pydantic import BaseModel, ConfigDict, Field
import pendulum


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    user_id: int = Field(..., alias="userNum")
    nickname: str = Field(..., alias="nickname")
    last_retrieval: pendulum.DateTime = Field(default_factory=pendulum.now)
