from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class GetOrCreateMixin:
    @classmethod
    def get_or_create(cls, session, filter_query):
        instance = session.query(cls).filter_by(**filter_query).first()
        if instance:
            return instance
        else:
            instance = cls(**filter_query)
            session.add(instance)
            session.commit()
            return instance


class Chat(Base, GetOrCreateMixin):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f'Chat {self.id}'


class InitSQLAlchemy:
    def __init__(self):
        self.engine = create_engine('postgresql://nikita:pass@localhost/rzd_monitor', echo=True)
        self.session = sessionmaker(bind=self.engine)()


if __name__ == '__main__':
    engine = create_engine('postgresql://nikita:pass@localhost/rzd_monitor', echo=True)
    Base.metadata.create_all(engine)
