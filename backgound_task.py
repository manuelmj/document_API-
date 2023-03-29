import os 
from fastapi import HTTPException

class ErrorDeleteFileException(HTTPException):
    def __init__(self, e: Exception):
        detail = f"Error: Something went wrong while deleting files. Reason: {str(e)}"
        super().__init__(status_code=500, detail=detail)

def delete_image(file_path: str) -> str:
    """
    This function deletes the image file from the images folder.

    args:
        file_path (str): path of the image file
    returns:
        str: "OK"
    raises:
        ErrorDeleteFileException: 500 if the image file is not found

    """
    try :
        os.remove(file_path)
    except OSError as e:
        assert ErrorDeleteFileException(e)
    return "OK"

def delete_pdf(file_path: str) -> str:
    """
    This function deletes the pdf file from the pdfs folder.

    args:
        file_path (str): path of the pdf file
    returns:
        str: "OK"
    raises:
        ErrorDeleteFileException: 500 if the pdf file is not found
    """
    
    
    try:
        os.remove(file_path)
    except OSError as e:
        assert ErrorDeleteFileException(e)
    return "OK"
