from pyexpat import model
from tkinter import Widget
from turtle import mode
from unittest.util import _MAX_LENGTH
from xml.dom import ValidationErr
from django.db import models
from django.core.validators import RegexValidator

class Construction(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=250)
    zip_code = models.CharField(
        max_length=5,
        validators=[RegexValidator(r'^\d{5}$', message="The ZIP code you entered is not valid in France")]
    )
    city = models.CharField(max_length=50)
    demolished = models.BooleanField(default=False)

    CONSTRUCTION_TYPE = [
        ("HOUSE", "House"),
        ("CATHEDRAL", "Cathedral"),
        ("CASTLE", "Castle"),
    ]
    type = models.CharField(max_length=20, choices=CONSTRUCTION_TYPE)
    
    def __str__(self):
        return f"{self.get_type_display()} at {self.address}"
        