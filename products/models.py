import os, string, random
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save

from sorl.thumbnail import ImageField

from ecommerce.utils import unique_slug_generator
from category.models import SubCategory, Category

def get_filepath_ext(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name, ext  

def upload_filename_ext(instance, filename):
    newFilename = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits , 7)
    newFilename = ''.join(newFilename)
    name, ext = get_filepath_ext(filename)
    return f'{newFilename}{ext}'


class Product(models.Model):
    title               = models.CharField(max_length=200)
    brand_name          = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING, blank=True, null=True)
    department_name     = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    slug                = models.SlugField(blank=True, unique=True)
    description         = models.TextField()
    price               = models.DecimalField(default=199.99, max_digits=20, decimal_places=2)
    stock               = models.PositiveIntegerField(default=0)
    image_main          = models.ImageField(upload_to=upload_filename_ext)
    image_1             = models.ImageField(upload_to=upload_filename_ext, blank=True, null=True)
    image_2             = models.ImageField(upload_to=upload_filename_ext, blank=True, null=True)
    image_3             = models.ImageField(upload_to=upload_filename_ext, blank=True, null=True)
    
    class Meta:
        verbose_name = "product list"
        verbose_name_plural = "product's list"

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title
    
    def get_absolute_url(self, *args, **kwargs):
        return reverse('products:detail',kwargs={'slug':self.slug})


def slug_pre_save_receiver(instance, sender, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_pre_save_receiver, sender=Product)





    







