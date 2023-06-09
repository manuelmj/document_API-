from fastapi import (APIRouter,
                     UploadFile,
                     HTTPException,
                     status,
                     BackgroundTasks,
                     Request)

from fastapi import (File,
                     Body, 
                     Query,
                     Depends)
from fastapi.responses import FileResponse

from backgound_task import (delete_image,
                            delete_pdf)


from validation.file_validation import (validate_image_file_name,
                        validate_pdf_file_name,
                        validate_image_file_content_delete,
                        validate_pdf_file_content_delete)

from models.example_models import (Document_information_resignation_example, 
                                   template_resignation_path)
from models.document_model import (Document_information_resignation,
                                   Response_information_resignation)
from createPDF import create_resignation_PDF
import shutil
import os

from validation.cookie_validation import  session_cookie_id_validator

router = APIRouter(
    prefix="/document/resignation",
    tags=["document/resignation"],
    dependencies=[Depends( session_cookie_id_validator)]
)


@router.get("/", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def get_renuncia_example(background_tasks: BackgroundTasks,
                               pdf_file_delete : str = Depends(validate_pdf_file_content_delete),):
    """
    ## Description
    This endpoint generates a sample resignation letter in PDF format using the provided template and document information. 
    The generated PDF file is returned as the response.

    ## Responses
    - 200: The generated PDF file is returned as a `FileResponse` object.
    - 500: An error occurred while creating the document.

    ## Return
    - A `FileResponse` object containing the generated PDF file.

    ## Raises
    - `HTTPException`: If an error occurs while creating the PDF document.

    ## Dependencies 
    - `pdf_file_delete` (str): A string representation of the PDF file to delete.
    - `session_cookie_id_validator` (str): A string representation of the session cookie id.
    
    ## Background Tasks
    - `delete_pdf` (function): Deletes the specified PDF file.
    
    """

    try:
        create_resignation_PDF(template_resignation_path, Document_information_resignation_example, "example_resignation")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the document: " + str(e))
    
    background_tasks.add_task(delete_pdf,"pdfs/example_resignation.pdf")
    return FileResponse("pdfs/example_resignation.pdf", media_type='application/pdf', filename="example_resignation.pdf")




@router.get("/downloadFile", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def download_renuncia(background_tasks: BackgroundTasks,
                            pdf_file_path: str = Depends(validate_pdf_file_name)):
                                   
    """
    ## Description
    This endpoint returns the PDF file that was previously generated using the `POST /document/resignation` endpoint.

    ## Responses
    - 200: The PDF file is returned as a `FileResponse` object.
    - 404: The PDF file was not found.

    ## Return
    - A `FileResponse` object containing the PDF file.

    ## Raises
    - `HTTPException`: If the PDF file was not found.

    ## Dependencies
    - `pdf_file_path` (str): A string representation of the PDF file path.
    - `session_cookie_id_validator` (str): A string representation of the session cookie id.
    
    ## Background Tasks
    - `delete_pdf` (function): Deletes the specified PDF file.
    """
    if not os.path.exists(pdf_file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Document not found ")
    
    background_tasks.add_task(delete_pdf,pdf_file_path)    
    
    return FileResponse(pdf_file_path, media_type='application/pdf', filename=pdf_file_path.split("/")[-1].split("_")[0]+".pdf") 




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Response_information_resignation)
async def create_resignation_document( background_tasks: BackgroundTasks,
                                    request:Request,
                                    document_information: Document_information_resignation = Body(...,description="An instance of the Document_information_resignation Pydantic model which contains the necessary data to create the renunciation document."),
                                    file_name: str = Query(...,min_length=1, max_length=50,example="prueba", description="The desired name of the PDF file to be created. This value will be used as the prefix of the generated file name."),
                                    image_path: str = Depends(validate_image_file_name),
                                    pdf_file_delete : str = Depends(validate_pdf_file_content_delete),
                                   ):

    """
    ## Description 
    This endpoint generates a resignation letter in PDF format using the provided template and document information.
    The generated PDF file is saved in the `pdfs` directory and the path to the file is returned as the response.

    ## Responses
    - 201: The path to the generated PDF file is returned as a `Response_information_resignation` object.
    - 400: The provided file name is invalid.
    - 500: An error occurred while creating the document.

    ## Return
    - A `Response_information_resignation` object containing the information  of the generated PDF file.
    
    ## Raises
    - `HTTPException`: If the provided file name is invalid or an error occurs while creating the PDF document.
    
    ## arguments
    - `document_information` (Document_information_resignation): An instance of the Document_information_resignation Pydantic model which contains the necessary data to create the renunciation document.
    - `file_name` (str): The desired name of the PDF file to be created. This value will be used as the prefix of the generated file name.
    
    ## Dependencies
    - `image_path` (str): A string representation of the image file path.
    - `pdf_file_delete` (str): this dependency is used to delete the previous pdf file that was generated using the `POST /document/resignation` or other endpoint.
    - `session_cookie_id_validator` (str): A string representation of the session cookie id.
   
    ## Background Tasks
    - `delete_image` (function): Deletes the specified image file.

    """

    document_information = document_information.dict()
    document_information['image_firma_path'] = image_path
    cookie_id = request.cookies.get("session_id")
    file_name = "{}_{}".format(file_name,cookie_id) 
    try:
        create_resignation_PDF(template_resignation_path, document_information, file_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the document: " + str(e))
    
    background_tasks.add_task(delete_image,image_path)
    
    return document_information




@router.post("/loadImage",response_class=FileResponse,status_code=status.HTTP_202_ACCEPTED)
async def load_image(request:Request,
                     image: UploadFile = File(...,
                                              max_size=10_000_000, 
                                              content_type=["image/png", "image/jpg", "image/jpeg"], 
                                              description="The image file to be uploaded."),
                                              delete_image: str = Depends(validate_image_file_content_delete)):
    """
    ## Description
    This endpoint uploads an image file to the `images` directory.

    ## Responses
    - 202: The image file is uploaded to the `images` directory.
    - 204: The image file is empty.
    - 400: The image file size exceeds the maximum allowed limit (10MB) or the image file is not in png, jpg, or jpeg format.
    - 404: The image file was not found.
    - 500: An error occurred while uploading the image file.

    ## Return
    - A `FileResponse` object containing the uploaded image file.

    ## Raises
    - `HTTPException`: If the image file size exceeds the maximum allowed limit (10MB) or the image file is not in png, jpg, or jpeg format or the image file was not found or an error occurred while uploading the image file.

    ## Arguments
    - `image` (UploadFile): The image file to be uploaded.

    ## Dependencies
    - `delete_image` (str): this dependency is used to delete the previous image file that was generated using the `POST /document/resignation/loadImage` or other endpoint.
    - `session_cookie_id_validator` (str): A string representation of the session cookie id.
    """
    
    if image.size > 10_000_000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File size exceeds the maximum allowed limit (1MB)")

    if image.filename.split('.')[-1] not in ['png','jpg','jpeg']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image must be in png, jpg, or jpeg format")

    image_path = f"images/{image.filename}"
    with open(image_path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer) 

    if not os.path.exists(f"images/{image.filename}"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error occurred while uploading image")
    
    cookie_id = request.cookies.get("session_id")
    new_image_path = f"images/firma_{cookie_id}.{image.filename.split('.')[-1]}"
    
    try:
        os.rename(image_path, new_image_path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error occurred while renaming image")
    
    if not os.path.exists(new_image_path):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error occurred while renaming image")
    
    return FileResponse(new_image_path, media_type='image/png')




#punto 1. se podria usar usa cookie para crear una sesion personalizada
#punto 2. agregar ese id a la cookie 
#punto 3. revisr pagina 189 del libro de fastapi
#punto 4. usar la cookie para eliminar los elementos residuo
#punto 5. cuando la cookie expire la tarea de segundo plano elimne las sesiones 
#revisar usar un pront para generar el doby 