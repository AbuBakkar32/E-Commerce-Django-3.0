from django.db import models

from sorl.thumbnail import ImageField

import os, random, string

def get_filepath_ext(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name, ext  

def upload_filename_ext(instance, filename):
    newFilename = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits , 7)
    newFilename = ''.join(newFilename)
    name, ext = get_filepath_ext(filename)
    return f'{newFilename}{ext}'

    

class Category(models.Model):
    name        = models.CharField(max_length=200, unique=True, help_text="Unique one")
    image       = models.ImageField(upload_to=upload_filename_ext, blank=True, null=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)


    
    def __str__(self):
        return self.name 
    
# limit_choices_to={
#         id__in=BaseModel._product_list,
#     },

    
class SubCategory(models.Model):
    name        = models.CharField(max_length=200, unique=True, help_text="Unique one")
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, limit_choices_to={'active':True,})
    image       = models.ImageField(upload_to=upload_filename_ext, blank=True, null=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name 
     


