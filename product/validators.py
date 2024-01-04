import os
from django.core.exceptions import ValidationError

def validate_pdf(value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.pdf']

        if not ext.lower() in valid_extensions:
            raise ValidationError("only pdf files are allowed.")

def validate_image(value):
        valid_extensions = ['.jpg', '.jpeg', '.png']
        ext = os.path.splitext(value.name)[1]
        if ext.lower() not in valid_extensions:
            raise ValidationError("only jpeg and png are allowed.")