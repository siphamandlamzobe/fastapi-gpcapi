from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Query
from typing import List
from datetime import datetime 
import uvicorn
# from api.app.models import ServiceReportResponse

from models import ServiceReport, ServiceReportRequest, ServiceReportResponse, ServiceReportType, ServiceReportTypeRequest, ServiceReportTypeResponse
from services import engine, create_db_and_tables
from sqlmodel import Session, select

app = FastAPI(title="Service Report")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_session():
    with Session(engine) as session :
        yield session

@app.post("/api/servicereport/", response_model=ServiceReportResponse)
def add_service_report(*, session: Session = Depends(get_session),service_report: ServiceReportRequest):
    new_service_report = ServiceReport.from_orm(service_report)

    session.add(new_service_report)
    session.commit()
    session.refresh(new_service_report)
    return new_service_report

@app.post("/api/servicereporttype/", response_model=ServiceReportTypeResponse)
def add_service_report_type(*, session: Session = Depends(get_session),servicereporttype: ServiceReportTypeRequest) -> ServiceReportTypeResponse:
        new_service_type = ServiceReportType.from_orm(servicereporttype)

        session.add(new_service_type)
        session.commit()
        session.refresh(new_service_type)
        return new_service_type
    
@app.get("/api/servicereporttype/{id}")
def service_report_type_by_id(*, session: Session = Depends(get_session),id: int):
        reporttype = session.get(ServiceReportType, id)
        if not reporttype:
            raise HTTPException(status_code=404, detail=f"No service report type with id = {id}")
        return reporttype
        
@app.get("/api/servicereporttypes")
def service_report_types(*, session: Session = Depends(get_session),): 
        query = select(ServiceReportType)
        return session.exec(query).all()

@app.get("/api/servicereports/", response_model=List[ServiceReportResponse])
def get_service_reports(*, session: Session = Depends(get_session),offset:int = 0, limit:int = Query(default=100, lte=100)):
        service_reports = session.exec(select(ServiceReport).offset(offset).limit(limit)).all()
        return service_reports

@app.patch("/api/servicereports/{id}", response_model=ServiceReportResponse)
def update_service_report(*, session: Session = Depends(get_session),id: int, service_report: ServiceReportRequest):
        db_service_report = session.get(ServiceReport, id)

        if not db_service_report:
            raise HTTPException(status_code=404, detail="Service report not found")
        service_report.updated_on = datetime.utcnow()
        service_report_data = service_report.dict(exclude_unset=True)
        
        for key, value in service_report_data.items():
            setattr(db_service_report, key, value)
        session.add(db_service_report)
        session.commit()
        session.refresh(db_service_report)
        return db_service_report

@app.delete("/api/servicereports/{id}")
def delete_service_report(*, session: Session = Depends(get_session),int: int):
        service_report = session.get(ServiceReport, int)
        if not service_report:
            raise HTTPException(status_code=404, detail="Service report not found")
        session.delete(service_report)
        session.commit()
        return {"ok": True}

@app.get("/api/servicereport/{id}", response_model=ServiceReportResponse)
def service_report_by_id(*, session: Session = Depends(get_session),id: int) -> ServiceReportResponse:
        service_report = session.get(ServiceReport, id)
        if not service_report:
            raise HTTPException(status_code=404, detail=f"No service report type with id = {id}")
        return service_report

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)