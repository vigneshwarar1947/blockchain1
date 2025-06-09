
# Create your models here.
# certification/models.py
from django.db import models

class Certificate(models.Model):
    student_name = models.CharField(max_length=100)
    certificate_file = models.FileField(upload_to='certificates/')
    certificate_hash = models.CharField(max_length=66)  # "0x" + 64 hex characters
    blockchain_tx = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.certificate_hash}"
