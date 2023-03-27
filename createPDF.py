import jinja2
import pdfkit 


def create_resignation_PDF(template_path, data,name):
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
    output_path = f"pdfs/{name}.pdf"
    pdfkit.from_string(html, output_path, configuration=config, options=options)

