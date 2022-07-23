from graphene_django import DjangoObjectType
from .models import *


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('email', 'nickname')

