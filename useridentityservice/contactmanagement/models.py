from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Contact(models.Model):
    phoneNumber=PhoneNumberField()
    email=models.EmailField()
    linkedId=models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True)
    contact_type=(('primary','primary'),('secondary','secondary'))
    linkPrecedence=models.CharField(max_length=12,choices=contact_type,default='secondary')
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    deletedAt=models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table='Contact'