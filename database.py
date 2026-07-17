from datetime import datetime
from pathlib import Path

from sqlmodel import SQLModel, Field, Session, create_engine


Path("data").mkdir(exist_ok=True)

engine = create_engine(
    "sqlite:///data/bot.db",
    echo=False,
)

class Link(SQLModel, table=True):
    code: str = Field(primary_key=True)
    chat_id: int
    message_id: int
    is_video: bool
    created_at: datetime = Field(default_factory=datetime.utcnow)


def init_db():
    SQLModel.metadata.create_all(engine)


def save_link(
    code: str,
    chat_id: int,
    message_id: int,
    is_video: bool,
):
    with Session(engine) as session:
        session.add(
            Link(
                code=code,
                chat_id=chat_id,
                message_id=message_id,
                is_video=is_video,
            )
        )
        session.commit()


def get_link(code: str):
    with Session(engine) as session:
        return session.get(Link, code)
    

def code_exists(code: str) -> bool:
    with Session(engine) as session:
        return session.get(Link, code) is not None
    

