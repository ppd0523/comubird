from django.db import models
from django.utils import timezone
from member.models import User
from django.core.exceptions import ValidationError


class Stock(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return f'{self.name}({self.code})'


def upload_filter(instance, filename):
    return f'{instance.owner.pk}_{filename}'


def validate_file_size(value):
    if value.size > 4096:
        raise ValidationError("The maximum file size can be 4KB")
    else:
        return value


class Filter(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, to_field='email', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.localdate, null=False, blank=False, editable=False)
    deleted_date = models.DateTimeField(default=None, null=True, blank=True)
    permission = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
    file = models.FileField(upload_to=upload_filter, validators=[validate_file_size], )

    def __str__(self):
        return f'{self.owner} {self.name}'


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['filter_id', 'stock', 'date'], name='unique_reporting'),
        ]

    def __str__(self):
        return f'{self.filter} {self.date} {self.stock}'
