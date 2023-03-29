import os 
import shutil
from fastapi import HTTPException

class ErrorDeleteFileException(HTTPException):
    def __init__(self, e: Exception):
        detail = f"Error: Something went wrong while deleting files. Reason: {str(e)}"
        super().__init__(status_code=500, detail=detail)

def delete_image(file_path: str) -> str:
    try :
        os.remove(file_path)
    except OSError as e:
        assert ErrorDeleteFileException(e)
    return "OK"


def delete_pdf(file_path: str) -> str:
    try:
        os.remove(file_path)
    except OSError as e:
        assert ErrorDeleteFileException(e)
    return "OK"
