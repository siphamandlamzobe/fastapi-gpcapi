import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.api.dependencies.database import get_db

from app.models.hop_report import HopReport, HopReportRequest, HopReportResponse

router = APIRouter()


@router.post("/", response_model=HopReportResponse)
def add_hop_report(*, session: Session = Depends(get_db), hop_report: HopReportRequest):
    new_hop_report = HopReport.from_orm(hop_report)

    session.add(new_hop_report)
    session.commit()
    session.refresh(new_hop_report)
    return new_hop_report


@router.get("/", response_model=List[HopReportResponse])
def get_hop_reports(*, session: Session = Depends(get_db), offset: int = 0, limit: int = Query(default=100, lte=100)):
    hop_reports = session.exec(
        select(HopReport).offset(offset).limit(limit)).all()
    return hop_reports


@router.patch("/{id}", response_model=HopReportResponse)
def update_hop_report(*, session: Session = Depends(get_db), id: int, hop_report: HopReportRequest):
    db_hop_report = session.get(HopReport, id)

    if not db_hop_report:
        raise HTTPException(status_code=404, detail="Hop report not found")
    hop_report.updated_on = datetime.utcnow()
    hop_report_data = hop_report.dict(exclude_unset=True)

    for key, value in hop_report_data.items():
        setattr(db_hop_report, key, value)
    session.add(db_hop_report)
    session.commit()
    session.refresh(db_hop_report)
    return db_hop_report


@router.delete("/{id}")
def delete_hop_report(*, session: Session = Depends(get_db), int: int):
    hop_report = session.get(HopReport, int)
    if not hop_report:
        raise HTTPException(status_code=404, detail="Hop report not found")
    session.delete(hop_report)
    session.commit()
    return {"ok": True}


@router.delete("/")
def delete_all_hop_reports(*, session: Session = Depends(get_db)):
    hop_reports = session.exec(select(HopReport))
    if not hop_reports:
        raise HTTPException(status_code=404, detail="Hop report not found")

    deleted_report_count = 0
    for hop_report in hop_reports:
        session.delete(hop_report)
        deleted_report_count += 1

    session.commit()
    return JSONResponse(content={"message": str(deleted_report_count) + " Reports Deleted"})


@router.get("/{id}")
def get_hop_report(*, session: Session = Depends(get_db), int: int):
    hop_report = session.get(HopReport, int)
    if not hop_report:
        raise HTTPException(status_code=404, detail="hop report not found")

    return hop_report
