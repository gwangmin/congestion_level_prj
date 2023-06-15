from django.db import models
from django.contrib.auth.models import AbstractUser
from cctv.models import Facility

# Create your models here.
class FacilityMgr(AbstractUser):
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True)
