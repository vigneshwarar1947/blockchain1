# certification/forms.py
from django import forms

class CertificateForm(forms.Form):
    student_name = forms.CharField(max_length=100, label="Student Name")
    certificate_file = forms.FileField(label="Certificate File")

class VerifyCertificateForm(forms.Form):
    certificate_file = forms.FileField(label="Upload Certificate for Verification")
