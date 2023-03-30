from pydantic import BaseModel
from pydantic import Field



class Document_information_resignation(BaseModel):
    Ciudad: str = Field(...,min_length=1,max_length=50,example='Santa Marta')
    fecha_actual: str = Field(...,min_length=1,max_length=20, example="2021-01-01")
    nombre_jefe: str = Field(..., min_length=1,max_length=50,example='Alfonso Rivera')
    cargo_jefe: str = Field(...,min_length=1,max_length=50, example='Gerente')
    empresa: str = Field(..., min_length=1,max_length=50,example='Empresa ejemplo S.A.S')
    cargo_persona: str = Field(...,min_length=1,max_length=50, example='Analista')
    fecha_renuncia: str = Field(..., min_length=1,max_length=50,example="viernes 01 de enero de 2021")
    nombre_empleado: str = Field(..., example='Manuel Manjarres')
    id_empleado: str = Field(..., min_length=1,max_length=20,example='123456789')


class Response_information_resignation(Document_information_resignation):
    image_firma_path: str = Field(..., example="images/firma_example.jpeg")