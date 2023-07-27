import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Query, File, UploadFile
from typing import List
from datetime import datetime
from fastapi.responses import JSONResponse
import uvicorn
import pandas as pd

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
    with Session(engine) as session:
        yield session


@app.post("/api/servicereport/", response_model=ServiceReportResponse)
def add_service_report(*, session: Session = Depends(get_session), service_report: ServiceReportRequest):
    new_service_report = ServiceReport.from_orm(service_report)

    session.add(new_service_report)
    session.commit()
    session.refresh(new_service_report)
    return new_service_report


@app.post("/api/servicereporttype/", response_model=ServiceReportTypeResponse)
def add_service_report_type(*, session: Session = Depends(get_session), servicereporttype: ServiceReportTypeRequest) -> ServiceReportTypeResponse:
    new_service_type = ServiceReportType.from_orm(servicereporttype)

    session.add(new_service_type)
    session.commit()
    session.refresh(new_service_type)
    return new_service_type


@app.get("/api/servicereporttype/{id}")
def service_report_type_by_id(*, session: Session = Depends(get_session), id: int):
    reporttype = session.get(ServiceReportType, id)
    if not reporttype:
        raise HTTPException(
            status_code=404, detail=f"No service report type with id = {id}")
    return reporttype


@app.get("/api/servicereporttypes/")
def service_report_types(*, session: Session = Depends(get_session),):
    query = select(ServiceReportType)
    return session.exec(query).all()


@app.get("/api/servicereports/", response_model=List[ServiceReportResponse])
def get_service_reports(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, lte=100)):
    service_reports = session.exec(
        select(ServiceReport).offset(offset).limit(limit)).all()
    return service_reports


@app.patch("/api/servicereports/{id}", response_model=ServiceReportResponse)
def update_service_report(*, session: Session = Depends(get_session), id: int, service_report: ServiceReportRequest):
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
def delete_service_report(*, session: Session = Depends(get_session), int: int):
    service_report = session.get(ServiceReport, int)
    if not service_report:
        raise HTTPException(status_code=404, detail="Service report not found")
    session.delete(service_report)
    session.commit()
    return {"ok": True}


@app.get("/api/servicereport/{id}", response_model=ServiceReportResponse)
def service_report_by_id(*, session: Session = Depends(get_session), id: int) -> ServiceReportResponse:
    service_report = session.get(ServiceReport, id)
    if not service_report:
        raise HTTPException(
            status_code=404, detail=f"No service report type with id = {id}")
    return service_report


# Directory to save uploaded files
UPLOAD_DIR = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "uploads")


@app.post("/api/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Create the uploads directory if it doesn't exist
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # Save the uploaded file to the uploads directory
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/api/processuploads/")
async def process_uploads(*, session: Session = Depends(get_session)):
    file_path = os.path.relpath(UPLOAD_DIR)
    uploaded_file_names = get_files_in_directory(file_path)

    for file_name in uploaded_file_names:
        path_with_file_name = os.path.join(UPLOAD_DIR, file_name)
        df = pd.read_excel(path_with_file_name, sheet_name='Sheet1')

        for index, row in df.iterrows():
            new_data = ServiceReport(
                attendance=row['attendance'], first_timers=row['first_timers'],
                souls_saved=row["souls_saved"], service_review=row["service_review"],
                service_type_id=row["service_type_id"], created_on=row["created_on"], 
                updated_on=row["updated_on"], service_date=row["service_date"],)

            session.add(new_data)

        session.commit()
        session.close()

def get_files_in_directory(dir_path):
    res = []

    # Iterate directory
    for file_path in os.listdir(dir_path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(dir_path, file_path)):
            # add filename to list
            res.append(file_path)
    return res

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
