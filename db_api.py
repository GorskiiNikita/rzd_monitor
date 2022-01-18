from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBAPI:
    def __init__(self):
        self.engine = create_engine('postgresql://nikita:pass@localhost/rzd_monitor', echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def get_or_create(self, session):
        pass

