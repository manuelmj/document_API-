import os 
from fastapi import HTTPException


def validate_image_file_name():
    paths = ("images/firma.jpg", "images/firma.png", "images/firma.jpeg")
    image_path = None
    for path in paths:
        if os.path.exists(path):
            image_path = path
            break
    if not image_path:
        raise HTTPException(status_code=400, detail="No se ha cargado una firma")
    
    return image_path

def validate_pdf_file_name():
    directory_path = "/home/manuel/Visualstudio/Document_API/pdfs"
    pdf_path = os.listdir(directory_path)
    if len(pdf_path) == 0:
        raise HTTPException(status_code=400, detail="No se ha encontrado un archivo PDF")
    
    return os.path.join(directory_path, pdf_path[0])



def validate_pdf_file_content_delete():
    directory_path = "/home/manuel/Visualstudio/Document_API/pdfs"
    
    try:
        contents = os.listdir(directory_path)
        
        for content in contents:
            path = os.path.join(directory_path, content)
            if os.path.isfile(path):
                os.remove(path)
   #NOTA CREAR LAS EXCEPTIONS PERSONALIZADAS PARA CADA UNO DE LOS CASOS
    except FileNotFoundError as e:
        print(f"Error: {e}. Directory path not found.")
    except PermissionError as e:
        print(f"Error: {e}. Permission denied to delete files.")
    except Exception as e:
        print(f"Error: {e}. Something went wrong while deleting files.")

    return "OK"



def validate_image_file_content_delete():
    directory_path = "/home/manuel/Visualstudio/Document_API/images"
    try:
        contents = os.listdir(directory_path)
        for content in contents:
            path = os.path.join(directory_path, content)
            if os.path.isfile(path):
                os.remove(path)
    except FileNotFoundError as e:
        print(f"Error: {e}. Directory path not found.")
    except PermissionError as e:
        print(f"Error: {e}. Permission denied to delete files.")
    except Exception as e:
        print(f"Error: {e}. Something went wrong while deleting files.")
    
    return "OK"



