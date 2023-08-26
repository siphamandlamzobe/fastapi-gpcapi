from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class HopReportBase(SQLModel):
    expected_physical_attendance: int
    expected_online_attendance: int
    actual_physical_attendance: int
    actual_online_attendance: int
    expected_first_timers: int
    actual_first_timers: int
    souls_saved: int
    hop_review: str
    created_on: datetime
    updated_on: Optional[datetime] | None
    hop_date: datetime


class HopReport(HopReportBase, table=True):
    id: int = Field(default=None, primary_key=True)

class HopReportRequest(HopReportBase):
    pass

class HopReportResponse(HopReportBase):
    id: int
