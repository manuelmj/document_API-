import jinja2
import pdfkit 
from datetime import datetime


def create_renuncia_PDF(template_path, data,name):
    template_name = template_path.split('/')[-1]
    template_path = template_path.replace(template_name, '')

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
    template = env.get_template(template_name)
    
    html = template.render(data)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
    }

    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    output_path = f"/home/manuel/Visualstudio/Document_API/pdfs/{name}.pdf"
    pdfkit.from_string(html, output_path, configuration=config, options=options)


data_example ={
    "Ciudad": 'Bogota',
    "fecha_actual": datetime.now(),
    "nombre_jefe": 'Juan Perez',
    "cargo_jefe": 'Gerente',
    "empresa": 'Empresa S.A.S',
    "cargo_persona": 'Analista',
    "fecha_renuncia":datetime.now(),
    "nombre_empleado": 'pepito mendoza',
    "id_empleado": '123456789',
}

template_renuncia_path = '/home/manuel/Visualstudio/Document_API/templates/renuncia_template.html'