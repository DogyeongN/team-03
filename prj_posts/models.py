from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Prj(models.Model):
    post_title = models.CharField(max_length=15)
    user_name = models.CharField(max_length=5)
    user_major = models.CharField(max_length=15)
    user_grade = models.IntegerField(blank=True, validators=[
        MaxValueValidator(6),
        MinValueValidator(1)
    ])
    prj_name = models.CharField(max_length=15)
    prj_membernum = models.IntegerField(default=1, validators=[
        MaxValueValidator(6),
        MinValueValidator(1)
    ])
    post_content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]{self.post_title}'
    
    def get_absolute_url(self):
        return f'/prj/{self.pk}/'