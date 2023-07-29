import os
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlmodel import Session
import pandas as pd

from app.api.dependencies.database import get_db
from app.models.service_report import ServiceReport

router = APIRouter(prefix="/uploads", tags=["uploads"])

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

            move_file_to_processed_dir(path_with_file_name)

        return JSONResponse(content={"message": "Files processed successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def get_files_in_directory(dir_path):
    res = []

    for file_path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file_path)):
            res.append(file_path)
    return res

def move_file_to_processed_dir(file_path):
    processed_file = os.path.join(PROCESSED_DIR, os.path.basename(file_path))
    os.rename(file_path, processed_file)