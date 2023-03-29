import os 
from fastapi import HTTPException, status, Request


class DirectoryPathNotFoundException(HTTPException):
    def __init__(self, e: Exception):
        detail = "Error: Directory path not found. Reason: " + str(e)
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PermissionDeniedException(HTTPException):
    def __init__(self,e: Exception):
        detail = "Error: Permission denied to delete files. Reason" + str(e)
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class OtherDeleteException(HTTPException):
    def __init__(self, e: Exception):
        detail = "Error: Something went wrong while deleting files. Reason" + str(e)
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


def validate_image_file_name(request:Request) -> str:

    cookie_id = request.cookies.get("session_id")
    paths = (f"images/firma_{cookie_id}.jpg", f"images/firma_{cookie_id}.png", f"images/firma_{cookie_id}.jpeg")
    image_path = None
    for path in paths:
        if os.path.exists(path):
            image_path = path
            break
    if not image_path:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No signature has been uploaded")
    
    return image_path

def validate_pdf_file_name(request:Request) -> str:
    directory_path = "pdfs"
    pdf_path = os.listdir(directory_path)
    if len(pdf_path) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PDF file not found")
    cookie_id = request.cookies.get("session_id")
    pdf_to_return = [pdf for pdf in pdf_path if pdf.find(cookie_id) != -1]
    return os.path.join(directory_path, pdf_to_return[0])



def validate_pdf_file_content_delete(request:Request) -> str:
    ##ponerlo para que elimine solo los arcvhivos pdf de un usuario en especifico
    #concatenar el toker para solo sobreescribir el que tenga el token 
    directory_path = "pdfs"
    cookie_id = request.cookies.get("session_id")
    
    try:
        contents = os.listdir(directory_path)
        
        for content in contents:
            path = os.path.join(directory_path, content)
            if os.path.isfile(path) and content.find(cookie_id) != -1:
                os.remove(path)

    except FileNotFoundError as e:
        raise DirectoryPathNotFoundException(e)
    except PermissionError as e:
        raise PermissionDeniedException(e)
    except Exception as e:
        raise OtherDeleteException(e)

    return "OK"



def validate_image_file_content_delete(request:Request) -> str:
    directory_path = "images"
    cookie_id = request.cookies.get("session_id")
    try:
        contents = os.listdir(directory_path)
        for content in contents:
            path = os.path.join(directory_path, content)
            if os.path.isfile(path) and content.find(cookie_id) != -1 and content != "firma_example.jpeg":
                os.remove(path)

    except FileNotFoundError as e:
        raise DirectoryPathNotFoundException(e)
    except PermissionError as e:
        raise PermissionDeniedException(e)
    except Exception as e:
        raise OtherDeleteException(e)
        
    return "OK"




async def pdf_file_sessionClose_delete(cookie_expired:str):
    directory_path = "pdfs"
    try:
        contents = os.listdir(directory_path)
        for content in contents:
            path = os.path.join(directory_path, content)
            if os.path.isfile(path) and content.find(cookie_expired) != -1 :
                os.remove(path)

    except FileNotFoundError as e:
        raise DirectoryPathNotFoundException(e)
    except PermissionError as e:
        raise PermissionDeniedException(e)
    except Exception as e:
        raise OtherDeleteException(e)
        
    return "OK"
 
    _   

async def image_file_sessionClose_delete(cookie_expired:str):
    directory_path = "images"
    try:
        contents = os.listdir(directory_path)
        for content in contents:
            path = os.path.join(directory_path, content)
            if os.path.isfile(path) and content.find(cookie_expired) != -1 and content != "firma_example.jpeg":
                os.remove(path)

    except FileNotFoundError as e:
        raise DirectoryPathNotFoundException(e)
    except PermissionError as e:
        raise PermissionDeniedException(e)
    except Exception as e:
        raise OtherDeleteException(e)
        
    return "OK"
 
    _



async def delete_zombies_pdf_files():
    #note: create function for delete zombie file
    # a zombie file is a file that is not associated
    #  with a session and there is not a session active
    pass

