from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
    

class YieldData(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    image           = models.ImageField(verbose_name="Image",upload_to="image",blank=True,null=True)
    description     = models.TextField(verbose_name="Description",blank=True,null=True)
    created_at      = models.DateField(auto_now_add=True, null=True, blank=True)
    is_sold         = models.BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return str(f"{self.user.name}")
    

class Query(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    yield_data      = models.ForeignKey(YieldData, on_delete=models.CASCADE)
    query           = models.TextField(verbose_name="Query",blank=True,null=True)
    created_at      = models.DateField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return str(f"{self.user.name}")
    

class ChatBot(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    query    = models.TextField(verbose_name="Query",blank=True,null=True)
    answer      = models.TextField(verbose_name="Answer",blank=True,null=True)
    created_at      = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(f"{self.user.name}")
