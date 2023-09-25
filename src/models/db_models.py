from .base import Base
from sqlalchemy import Column, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import relationship


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    url_full = Column(String)
    url_short = Column(String, unique=True)
    actions = relationship("Action")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "Link(url_short='%s')" % (self.url_short,)


class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    link_id = Column(ForeignKey("links.id"))
    link = relationship("Link", back_populates="actions")

    __mapper_args__ = {"eager_defaults": True}
