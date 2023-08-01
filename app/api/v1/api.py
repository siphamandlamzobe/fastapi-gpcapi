from fastapi import APIRouter

from app.api.v1.endpoints import service_report, service_report_type, uploads

api_router = APIRouter()
api_router.include_router(service_report.router, prefix="/servicereport", tags=["ServiceReports"])
api_router.include_router(service_report_type.router, prefix="/servicereporttypes", tags=["ServiceReportTypes"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])