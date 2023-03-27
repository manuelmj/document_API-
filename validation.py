import os 
from fastapi import HTTPException



class DirectoryPathNotFoundException(HTTPException):
    def __init__(self, e: Exception):
        detail = "Error: Directory path not found. Reason: " + str(e)
        super().__init__(status_code=404, detail=detail)

class PermissionDeniedException(HTTPException):
    def __init__(self,e: Exception):
        detail = "Error: Permission denied to delete files. Reason" + str(e)
        super().__init__(status_code=403, detail=detail)

class OtherDeleteException(HTTPException):
    def __init__(self, e: Exception):
        detail = "Error: Something went wrong while deleting files. Reason" + str(e)
        super().__init__(status_code=500, detail=detail)


def validate_image_file_name() -> str:
    paths = ("images/firma.jpg", "images/firma.png", "images/firma.jpeg")
    image_path = None
    for path in paths:
        if os.path.exists(path):
            image_path = path
            break
    if not image_path:
        raise HTTPException(status_code=400, detail="No signature has been uploaded")
    
    return image_path

def validate_pdf_file_name() -> str:
    directory_path = "pdfs"
    pdf_path = os.listdir(directory_path)
    if len(pdf_path) == 0:
        raise HTTPException(status_code=400, detail="PDF file not found")
    
    return os.path.join(directory_path, pdf_path[0])



def validate_pdf_file_content_delete() -> str:
    directory_path = "pdfs"
    
    try:
        contents = os.listdir(directory_path)
        
        for content in contents:
            path = os.path.join(directory_path, content)
            if os.path.isfile(path):
                os.remove(path)

    except FileNotFoundError as e:
        raise DirectoryPathNotFoundException(e)
    except PermissionError as e:
        raise PermissionDeniedException(e)
    except Exception as e:
        raise OtherDeleteException(e)

    return "OK"



def validate_image_file_content_delete() -> str:
    directory_path = "images"
    try:
        contents = os.listdir(directory_path)
        for content in contents:
            path = os.path.join(directory_path, content)
            if os.path.isfile(path) and content != "firma_example.jpeg":
                os.remove(path)
    except FileNotFoundError as e:
        raise DirectoryPathNotFoundException(e)
    except PermissionError as e:
        raise PermissionDeniedException(e)
    except Exception as e:
        raise OtherDeleteException(e)
        
    return "OK"



