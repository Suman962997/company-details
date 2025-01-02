from django.db import models

from django.contrib.postgres.fields import ArrayField


class Company(models.Model):

    company_name = models.CharField(max_length=800)
    address =models.JSONField(default=list)
    contact_number = models.CharField(max_length=800)
    email = models.CharField(max_length=800)
    website = models.CharField(max_length=800)

    def __str__(self):
        return self.company_name
