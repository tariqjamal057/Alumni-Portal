from django.db import models

from portal.models.base import BaseModel


class Batch(BaseModel):
    entry_year = models.IntegerField()
    passed_out = models.IntegerField()
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="batch_created_by"
    )
    updated_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="batch_updated_by"
    )

    def __str__(self):
        return str(self.entry_year) + "-" + str(self.passed_out)


class Degree(BaseModel):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="degree_created_by"
    )
    updated_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="degree_updated_by"
    )

    def __str__(self):
        return self.name


class DegreeSpecialization(BaseModel):
    specialization_degree = models.ForeignKey(
        Degree, on_delete=models.CASCADE, related_name="specialization_degree"
    )
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="degree_specialization_created_by"
    )
    updated_by = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="degree_specialization_updated_by",
    )

    def __str__(self):
        return self.name


class Department(BaseModel):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    degree_specialization = models.ForeignKey(
        DegreeSpecialization,
        on_delete=models.CASCADE,
        related_name="department_degree_specialization",
    )
    created_by = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="department_created_by"
    )
    updated_by = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="department_updated_by",
    )

    def __str__(self):
        return self.name
