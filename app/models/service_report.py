from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class ServiceReportBase(SQLModel):
    attendance: int
    first_timers: int
    souls_saved: int
    service_review: str
    service_type_id: int = Field(foreign_key="servicereporttype.id")
    created_on: datetime
    updated_on: Optional[datetime] | None
    service_date: datetime


class ServiceReport(ServiceReportBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ServiceReportRequest(ServiceReportBase):
    pass


class ServiceReportResponse(ServiceReportBase):
    id: int


class ServiceReportTypeRequest(SQLModel):
    service_type: str


class ServiceReportTypeResponse(ServiceReportTypeRequest):
    id: int


class ServiceReportStatsBase(SQLModel):
    index: str
    attendance: int
    first_timers: int
    souls_saved: int


class ServiceReportStats(ServiceReportStatsBase):
    pass

class ServiceReportStats(ServiceReportStatsBase, table=True):
    id: int = Field(default=None, primary_key=True)
