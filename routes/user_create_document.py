from fastapi import (APIRouter,
                     UploadFile,
                     HTTPException,
                     status,
                     BackgroundTasks)

from fastapi import (File,
                     Body, 
                     Query,
                     Depends)
from fastapi.responses import FileResponse

from backgound_task import (delete_image,
                            delete_pdf)


from validation import (validate_image_file_name,
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



router = APIRouter(
    prefix="/document/resignation",
    tags=["document/resignation"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_renuncia_example(background_tasks: BackgroundTasks,
                               pdf_file_delete : str = Depends(validate_pdf_file_content_delete),):
    
    try:
        create_resignation_PDF(template_resignation_path, Document_information_resignation_example, "example_resignation")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the document: " + str(e))
    
    background_tasks.add_task(delete_pdf,"pdfs/example_resignation.pdf")
    return FileResponse("pdfs/example_resignation.pdf", media_type='application/pdf', filename="example_resignation.pdf")




@router.get("/downloadFile", status_code=status.HTTP_200_OK, response_class=FileResponse)
async def download_renuncia(background_tasks: BackgroundTasks,
                                    pdf_file_path: str = Depends(validate_pdf_file_name)):
                                   
   
    if not os.path.exists(pdf_file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Document not found ")
    
    background_tasks.add_task(delete_pdf,pdf_file_path)    
    
    return FileResponse(pdf_file_path, media_type='application/pdf', filename=f"{pdf_file_path}")




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Response_information_resignation)
async def create_resignation_document( background_tasks: BackgroundTasks,
                                    document_information: Document_information_resignation = Body(...,description="An instance of the Document_information_resignation Pydantic model which contains the necessary data to create the renunciation document."),
                                    file_name: str = Query(...,min_length=1, max_length=50, description="The desired name of the PDF file to be created. This value will be used as the prefix of the generated file name."),
                                    image_path: str = Depends(validate_image_file_name),
                                    pdf_file_delete : str = Depends(validate_pdf_file_content_delete),
                                   ):


    document_information = document_information.dict()
    document_information['image_firma_path'] = image_path

    try:
        create_resignation_PDF(template_resignation_path, document_information, file_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the document: " + str(e))
    
    background_tasks.add_task(delete_image,image_path)
    
    return document_information




@router.post("/loadImage",response_class=FileResponse,status_code=status.HTTP_200_OK)
async def load_image(image: UploadFile = File(...,
                                              max_size=10_000_000, 
                                              content_type=["image/png", "image/jpg", "image/jpeg"], 
                                              description="The image file to be uploaded."),
                                              delete_image: str = Depends(validate_image_file_content_delete)):


    if image.size > 10_000_000:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum allowed limit (1MB)")

    if image.filename.split('.')[-1] not in ['png','jpg','jpeg']:
        raise HTTPException(status_code=400, detail="Image must be in png, jpg, or jpeg format")

    image_path = f"images/{image.filename}"
    with open(image_path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer) 

    if not os.path.exists(f"images/{image.filename}"):
        raise HTTPException(status_code=400, detail="Error occurred while uploading image")
    
    new_image_path = f"images/firma.{image.filename.split('.')[-1]}"
    os.rename(image_path, new_image_path)
    
    if not os.path.exists(f"images/firma.{image.filename.split('.')[-1]}"):
        raise HTTPException(status_code=400, detail="Error occurred while renaming image")
    
    #NOTA: debe devolver el archivo insertado
    
    return FileResponse(f"images/firma.{image.filename.split('.')[-1]}", media_type='image/png')
