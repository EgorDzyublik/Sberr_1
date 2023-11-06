from django.db import models
from .validators import validate_file_extension
class Input(models.Model):
    file = models.FileField(upload_to='texts/', validators=[validate_file_extension])

