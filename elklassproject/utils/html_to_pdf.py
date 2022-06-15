# encoding: utf-8
from django.http import HttpResponse
from django.template.loader import get_template
import os
import pdfkit
from django.template import loader

def render_to_pdf(template_name, context={}):
    template = get_template(template_name)
    html = template.render(context)
    # path_wkthmltopdf = os.environ.get('WKHTMLTOPDF_BIN')
    path_wkthmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit_options = {
            'page-size': 'A4',
            'encoding': "UTF-8"
        }
    pdf = pdfkit.from_string(html, False, configuration=config)
    return pdf
