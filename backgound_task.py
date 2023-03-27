import os 
import shutil
from fastapi import HTTPException

def delete_image(file_path: str) -> str:
    try :
        os.remove(file_path)
    except OSError as e:
        assert HTTPException(status_code=500, detail="Ha ocurrido un error al eliminar el archivo: " + str(e))
    
    return "OK"

def delete_pdf(file_path: str) -> str:
    try:
        os.remove(file_path)
    except OSError as e:
        assert HTTPException(status_code=500, detail="Ha ocurrido un error al eliminar el archivo: " + str(e))
    
    return "OK"
