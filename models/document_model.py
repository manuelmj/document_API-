from pydantic import BaseModel
from pydantic import Field



class Document_information_resignation(BaseModel):
    Ciudad: str = Field(..., example='Bogota')
    fecha_actual: str = Field(..., example="2021-01-01")
    nombre_jefe: str = Field(..., example='Juan Perez')
    cargo_jefe: str = Field(..., example='Gerente')
    empresa: str = Field(..., example='Empresa S.A.S')
    cargo_persona: str = Field(..., example='Analista')
    fecha_renuncia: str = Field(..., example="2021-01-01")
    nombre_empleado: str = Field(..., example='pepito mendoza')
    id_empleado: str = Field(..., example='123456789')


class Response_information_resignation(Document_information_resignation):
    image_firma_path: str = Field(..., example="images/firma_example.jpeg")