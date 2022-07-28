from graphene import List, NonNull, String, Field, Date
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
        fields = ('id', 'owner', 'title', 'index', 'permission', 'description',)

    url = String()
    reports = Field(List(NonNull(ReportType)), begin=Date(), end=Date(), required=True)

    def resolve_url(self, info):
        return self.file.url

    def resolve_reports(self, info, begin=None, end=None):
        reports = Report.objects.filter(filter=self)
        return reports


class ToSubscribeType(DjangoObjectType):
    class Meta:
        model = ToSubscribe
        fields = ('id', 'subscriber', 'permission', 'filter')
