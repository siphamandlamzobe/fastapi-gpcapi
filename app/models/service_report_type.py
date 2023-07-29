from sqlmodel import Field, SQLModel

class ServiceReportType(SQLModel, table=True):
    id: int = Field(default=None,primary_key=True)
    service_type: str
    
class ServiceReportTypeRequest(SQLModel):
    service_type: str

class ServiceReportTypeResponse(ServiceReportTypeRequest):
    id: int