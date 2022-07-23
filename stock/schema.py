from graphene_django import DjangoObjectType
from .models import *


class StockType(DjangoObjectType):
    class Meta:
        model = Stock
        fields = ('code', 'name')


class ReportType(DjangoObjectType):
    class Meta:
        model = Report
        fields = ('filter', 'stock', 'date')


class FilterType(DjangoObjectType):
    class Meta:
        model = Filter
        fields = ('owner', 'name', 'description')
