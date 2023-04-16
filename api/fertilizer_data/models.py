from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
    

class FertilizerData(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    nitrogen        = models.IntegerField(verbose_name="Nitrogen",blank=True,null=True)
    phosphorus      = models.IntegerField(verbose_name="Phosphorus",blank=True,null=True)
    potassium       = models.IntegerField(verbose_name="Potassium",blank=True,null=True)
    temperature     = models.IntegerField(verbose_name="Temperature",blank=True,null=True)
    humidity        = models.IntegerField(verbose_name="Humidity",blank=True,null=True)
    soil_moisture   = models.IntegerField(verbose_name="Soil Moisture",blank=True,null=True)
    soil_type       = models.TextField(verbose_name="Soil Type",blank=True,null=True)
    crop_type       = models.TextField(verbose_name="Crop Type",blank=True,null=True)
    result          = models.TextField(verbose_name="Result",blank=True,null=True)


    def __str__(self):
        return str(f"{self.user.name}")