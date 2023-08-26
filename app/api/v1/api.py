from fastapi import APIRouter

from app.api.v1.endpoints import process_hop_report_uploads, service_report, service_report_type, uploads, hop_report

api_router = APIRouter()
api_router.include_router(service_report.router, prefix="/servicereport", tags=["Service Reports"])
api_router.include_router(service_report_type.router, prefix="/servicereporttypes", tags=["Service Report Types"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["Upload Files"])
api_router.include_router(hop_report.router, prefix="/hopreport", tags=["Hop Reports"])
api_router.include_router(process_hop_report_uploads.router, prefix="/processhopreports", tags=["Process Hop Reports File Uploads"])