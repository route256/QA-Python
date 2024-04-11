from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from framework.sql.act_device_api_models import DevicesEvent


class Alchemy:
    def __init__(self, dsn: str):
        engine = create_engine(dsn)
        self.session_factory = sessionmaker(bind=engine)

    def entries_by_id(self, device_id: int) -> List[DevicesEvent]:
        session = self.session_factory()
        return session.query(DevicesEvent).filter_by(device_id=device_id).all()
