from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.api.auth import get_current_active_user
from app.models.service_report import ServiceReport, ServiceReportRequest, ServiceReportResponse, ServiceReportStats
from app.api.dependencies.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ServiceReportResponse) 
def add_service_report(*, session: Session = Depends(get_db), service_report: ServiceReportRequest, user: User = Depends(get_current_active_user)):
    new_service_report = ServiceReport.from_orm(service_report)

    session.add(new_service_report)
    session.commit()
    session.refresh(new_service_report)
    return new_service_report

@router.get("/", response_model=List[ServiceReportResponse])
def get_service_reports(*, session: Session = Depends(get_db), offset: int = 0, limit: int = Query(default=100, lte=100),  user: User = Depends(get_current_active_user)):
    service_reports = session.exec(
        select(ServiceReport).offset(offset).limit(limit)).all()
    return service_reports

@router.patch("/{id}", response_model=ServiceReportResponse)
def update_service_report(*, session: Session = Depends(get_db), id: int, service_report: ServiceReportRequest, user: User = Depends(get_current_active_user)):
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
def delete_service_report(*, session: Session = Depends(get_db), int: int, user: User = Depends(get_current_active_user)):
    service_report = session.get(ServiceReport, int)
    if not service_report:
        raise HTTPException(status_code=404, detail="Service report not found")
    session.delete(service_report)
    session.commit()
    return {"ok": True}

@router.delete("/")
def delete_all_service_reports(*, session: Session = Depends(get_db), user: User = Depends(get_current_active_user)):
    service_reports = session.exec(select(ServiceReport))
    if not service_reports:
        raise HTTPException(status_code=404, detail="Service report not found")
    
    deleted_report_count = 0
    for service_report in service_reports:
        session.delete(service_report)
        deleted_report_count += 1
        
    session.commit()
    return JSONResponse(content={"message": str(deleted_report_count) + " Reports Deleted"})

@router.delete("/removestats/")
def delete_all_service_report_stats(*, session: Session = Depends(get_db), user: User = Depends(get_current_active_user)):
    service_report_stats = session.exec(select(ServiceReportStats))
    if not service_report_stats:
        raise HTTPException(status_code=404, detail="Service report stats not found")
    
    deleted_report_count = 0
    for service_report_stat in service_report_stats:
        session.delete(service_report_stat)
        deleted_report_count += 1
        
    session.commit()
    return JSONResponse(content={"message": str(deleted_report_count) + " Reports Stats Deleted"})

@router.get("/{id}")
def get_service_report(*, session: Session = Depends(get_db), int: int, user: User = Depends(get_current_active_user)):
    service_report = session.get(ServiceReport, int)
    if not service_report:
        raise HTTPException(status_code=404, detail="Service report not found")
    
    return service_report