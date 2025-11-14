from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    pass

class AuthorDB(Base):
    __tablename__="authors"

    id: Mapped[Integer]=mapped_column(primary_key=True, index=True)
    name: Mapped[String]=mapped_column(String, len<=100, len>0, index=True)
    email: Mapped[String]=mapped_column(str, email=True, index=True)
    year_started: Mapped[Integer]=mapped_column(Integer, int>=1900, int<=2100, index=True)

class BookDB(Base):
    __tablename__="Books"

    author_id: Mapped[Integer]=mapped_column(primary_key=True, index=True)
    title: Mapped[String]=mapped_column(String, len<=255, len>0, index=True)
    pages: Mapped[Integer]=mapped_column(Integer, int<=10000, int>0, index=True)
    id: Mapped[Integer]=mapped_column(Integer, ForeignKey, index=True)