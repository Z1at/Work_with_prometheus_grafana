from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import INTEGER, UUID, VARCHAR, CHAR
from sqlalchemy.sql import func

from service.db import DeclarativeBase


class HumanStorage(DeclarativeBase):
    __tablename__ = "human_storage"

    id = Column(
        INTEGER,
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique id of the string in table",
    )
    name = Column(
        VARCHAR(100),
        nullable=True,
        doc="Name of human",
    )
    age = Column(
        INTEGER,
        nullable=True,
        doc="Age of human",
    )
    gender = Column(
        CHAR(1),
        nullable=True,
        doc="gender of human",
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
