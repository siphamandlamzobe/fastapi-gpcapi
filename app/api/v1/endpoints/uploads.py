import os
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlmodel import Session
import pandas as pd

from app.api.dependencies.database import get_db
from app.models.service_report import ServiceReport, ServiceReportStats

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "uploads")

PROCESSED_DIR = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "processed")

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/process/")
async def process_uploads(*, session: Session = Depends(get_db)):
    try:
        os.makedirs(PROCESSED_DIR, exist_ok=True)

        file_path = os.path.relpath(UPLOAD_DIR)
        uploaded_file_names = get_files_in_directory(file_path)

        for file_name in uploaded_file_names:
            path_with_file_name = os.path.join(UPLOAD_DIR, file_name)
            
            service_report_df = pd.read_excel(path_with_file_name, sheet_name='Sheet1')
            
            service_report_df['service_date'] = pd.to_datetime(service_report_df['service_date'])
            service_report_df.sort_values(by='service_date', inplace=True)
            
            if service_report_df.duplicated().any():
                service_report_df.drop_duplicates(inplace=True)
            
            # service_report_df.dropna(inplace=True)
            
            add_service_reports(service_report_df, session)

            add_service_report_stats(service_report_df, session)

            session.commit()
            session.close()

            # move_file_to_processed_dir(path_with_file_name)

        return JSONResponse(content={"message": "Files processed successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def get_files_in_directory(dir_path):
    res = []

    for file_path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file_path)):
            res.append(file_path)
    return res

def add_service_reports(service_report_df: pd.DataFrame, session: Session):
    for index, row in service_report_df.iterrows():
        new_data = ServiceReport(
            attendance=row['attendance'], first_timers=row['first_timers'],
            souls_saved=row["souls_saved"], service_review=row["service_review"],
            service_type_id=row["service_type_id"], created_on=row["created_on"], 
            updated_on=row["updated_on"], service_date=row["service_date"],)

        session.add(new_data)
        
def add_service_report_stats(service_report_df: pd.DataFrame, session: Session):
    stats = service_report_df[['attendance','first_timers', 'souls_saved']].describe()
    stats = stats.reset_index()
    stats['sum'] = stats[['attendance','first_timers', 'souls_saved']].sum()
    
    for index, row in stats.iterrows():
        service_report_stats = ServiceReportStats(
            index=row['index'],
            attendance=row['attendance'],
            first_timers=row['first_timers'],
            souls_saved=row['souls_saved']
        )
        session.add(service_report_stats)

def move_file_to_processed_dir(file_path):
    processed_file = os.path.join(PROCESSED_DIR, os.path.basename(file_path))
    os.rename(file_path, processed_file)
