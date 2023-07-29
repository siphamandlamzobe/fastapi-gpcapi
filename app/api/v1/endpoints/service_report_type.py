from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.api.dependencies.database import get_db
from app.models.service_report_type import ServiceReportTypeRequest, ServiceReportTypeResponse, ServiceReportType

router = APIRouter(prefix="/servicereporttypes", tags=["ServiceReportTypes"])

@router.post("/", response_model=ServiceReportTypeResponse)
def add_service_report_type(*, session: Session = Depends(get_db), servicereporttype: ServiceReportTypeRequest) -> ServiceReportTypeResponse:
    new_service_type = ServiceReportType.from_orm(servicereporttype)

    session.add(new_service_type)
    session.commit()
    session.refresh(new_service_type)
    return new_service_type

@router.get("/{id}")
def service_report_type_by_id(*, session: Session = Depends(get_db), id: int):
    reporttype = session.get(ServiceReportType, id)
    if not reporttype:
        raise HTTPException(
            status_code=404, detail=f"No service report type with id = {id}")
    return reporttype

@router.get("/")
def service_report_types(*, session: Session = Depends(get_db)):
    query = select(ServiceReportType)
    return session.exec(query).all()
