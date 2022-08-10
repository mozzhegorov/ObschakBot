from sqlalchemy import ForeignKey, Column, Integer, Table, Float, Boolean, select
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from settings import DATABASE


engine = create_engine(DATABASE, echo=True)

DeclarativeBase = declarative_base()
persons_in_receipts = Table(
    'persons_in_receipts',
    DeclarativeBase.metadata,
    Column(
        'person_id',
        ForeignKey("person.id"),
        primary_key=True,
    ),
    Column(
        'receipt_id',
        ForeignKey("receipt.id"),
        primary_key=True,
    )
)


class Person(DeclarativeBase):
    __tablename__ = "person"

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(
        String(64),
        nullable=False,
    )
    receipts = relationship(
        "Receipt",
        secondary=persons_in_receipts,
        back_populates="consumers",
    )

    def __repr__(self):
        return f"{self.name!r}"


class Receipt(DeclarativeBase):
    __tablename__ = "receipt"

    id = Column(
        Integer,
        primary_key=True,
    )
    user_id = Column(
        Integer,
        nullable=False,
    )
    calc_id = Column(
        Integer,
        nullable=False,
    )
    calc_alias = Column(
        String(64),
        nullable=True,
    )
    receipt_id = Column(
        Integer,
        nullable=False,
    )
    sponsor_id = Column(Integer, ForeignKey('person.id'), )
    sponsor = relationship("Person")
    sum = Column(
        Float,
        nullable=False,
    )
    consumers = relationship(
        "Person",
        secondary=persons_in_receipts,
        # backref=backref("persons", uselist=False),
    )

    def __repr__(self):
        return f"Receipt(id={self.id!r})"


class Calculation(DeclarativeBase):
    __tablename__ = "now_calculation"

    id = Column(
        Integer,
        primary_key=True,
    )
    user_id = Column(
        Integer,
        nullable=False,
    )
    calc_id = Column(
        Integer,
        nullable=False,
    )
    calc_alias = Column(
        String(64),
        nullable=True,
    )
    active = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    def __repr__(self):
        return f"NowCalculation(id={self.id!r})"


if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()
