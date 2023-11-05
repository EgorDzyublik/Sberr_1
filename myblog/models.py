from django.db import models
from .validators import validate_file_extension
class Input(models.Model):
    texts = models.FileField(upload_to='texts/', validators=[validate_file_extension])

