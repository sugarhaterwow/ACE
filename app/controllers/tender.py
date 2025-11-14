from typing import Optional

from app.core.crud import CRUDBase
from app.models.admin import Tender
from app.schemas.tenders import TenderCreate, TenderUpdate


class TenderController(CRUDBase[Tender, TenderCreate, TenderUpdate]):
    def __init__(self):
        super().__init__(model=Tender)


tender_controller = TenderController()
