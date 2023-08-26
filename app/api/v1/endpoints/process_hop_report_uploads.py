import os
import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.api.dependencies.database import get_db
from app.models.hop_report import HopReport


router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "uploads")

PROCESSED_DIR = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "processed")

@router.post("/process/hopreports")
async def process_uploads(*, session: Session = Depends(get_db)):
    try:
        os.makedirs(PROCESSED_DIR, exist_ok=True)

        file_path = os.path.relpath(UPLOAD_DIR)
        uploaded_file_names = get_files_in_directory(file_path)

        for file_name in uploaded_file_names:
            path_with_file_name = os.path.join(UPLOAD_DIR, file_name)
            
            hop_report_df = pd.read_excel(path_with_file_name, sheet_name='Sheet1')
            
            # hop_report_df['hop_date'] = pd.to_datetime(hop_report_df['hop_date'])
            # hop_report_df.sort_values(by='hop_date', inplace=True)
            
            if hop_report_df.duplicated().any():
                hop_report_df.drop_duplicates(inplace=True)
            
            add_hop_reports(hop_report_df, session)

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

def add_hop_reports(hop_report_df: pd.DataFrame, session: Session):
    for index, row in hop_report_df.iterrows():
        new_data = HopReport(
            expected_physical_attendance=row['expected_physical_attendance'], 
            actual_online_attendance=row['actual_online_attendance'],
            actual_physical_attendance=row['actual_physical_attendance'],
            expected_online_attendance=row['expected_online_attendance'],
            expected_first_timers=row['expected_first_timers'],
            actual_first_timers=row['actual_first_timers'],
            souls_saved=row["souls_saved"], 
            hop_review=row["hop_review"],
            created_on=row["created_on"], 
            updated_on=row["updated_on"], 
            hop_date=row["hop_date"],)

        session.add(new_data)