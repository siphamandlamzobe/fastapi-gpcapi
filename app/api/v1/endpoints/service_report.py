from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select

from app.models.service_report import ServiceReport, ServiceReportRequest, ServiceReportResponse
from app.api.dependencies.database import get_db


router = APIRouter(prefix="/servicereports", tags=["ServiceReports"])

@router.post("/", response_model=ServiceReportResponse) 
def add_service_report(*, session: Session = Depends(get_db), service_report: ServiceReportRequest):
    new_service_report = ServiceReport.from_orm(service_report)

    session.add(new_service_report)
    session.commit()
    session.refresh(new_service_report)
    return new_service_report

@router.get("/", response_model=List[ServiceReportResponse])
def get_service_reports(*, session: Session = Depends(get_db), offset: int = 0, limit: int = Query(default=100, lte=100)):
    service_reports = session.exec(
        select(ServiceReport).offset(offset).limit(limit)).all()
    return service_reports

@router.patch("/{id}", response_model=ServiceReportResponse)
def update_service_report(*, session: Session = Depends(get_db), id: int, service_report: ServiceReportRequest):
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


@router.delete("/{id}")
def delete_service_report(*, session: Session = Depends(get_db), int: int):
    service_report = session.get(ServiceReport, int)
    if not service_report:
        raise HTTPException(status_code=404, detail="Service report not found")
    session.delete(service_report)
    session.commit()
    return {"ok": True}