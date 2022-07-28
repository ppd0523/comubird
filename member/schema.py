from graphene_django import DjangoObjectType
from .models import User
from graphene import *
from stock.schema import FilterType
from stock.models import Filter, ToSubscribe


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('email', 'nickname')

    filters = Field(NonNull(List(FilterType)))
    subscribe = Field(NonNull(List(FilterType)))

    def resolve_filters(self, info, *args):
        return Filter.objects.filter(owner=self)

    # def resolve_subscribe(self, info, *args):
    #     return map(lambda obj: obj.filter, ToSubscribe.objects.filter(subscriber=self))
