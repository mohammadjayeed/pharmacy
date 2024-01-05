from django.http import FileResponse
import io
from reportlab.pdfgen import canvas 
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def pdf_generate(name,description,price,image=None):

    price = str(price)
    
    buffer = io.BytesIO()

    if not image:
        c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
    else:
        c = canvas.Canvas(buffer, pagesize=letter)
        
    text_start_y = 300

    object = c.beginText()
    object.setTextOrigin(inch, text_start_y)
    object.setFont("Helvetica", 14)

    object.textLine("-" * 50)  

    object.textLine(f"Product Name: {name}")
    object.textLine("-" * 50)  # Add a line of dashes between lines

    object.textLine(f"Product Description: {description}")
    object.textLine("-" * 50)  # Add a line of dashes between lines

    object.textLine(f"Product Price: {price}")
    object.textLine("-" * 50)  # Add a line of dashes after the last line



    c.drawText(object)
    if image:
       
        c.drawImage(image, 100, 400, width=200, height=300, preserveAspectRatio=True, anchor='s')
    

    c.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f'{name}.pdf')