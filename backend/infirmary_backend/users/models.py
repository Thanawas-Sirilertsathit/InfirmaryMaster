from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_PATIENT = 'patient'
    ROLE_STAFF = 'staff'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_PATIENT, 'Patient'),
        (ROLE_STAFF, 'Staff'),
        (ROLE_ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_PATIENT)
    verified = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def is_patient(self):
        return self.role == self.ROLE_PATIENT

    @property
    def is_staff_role(self):
        return self.role == self.ROLE_STAFF

    @property
    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN
