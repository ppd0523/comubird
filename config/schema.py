from graphene import *
from stock.schema import *
from member.schema import *


class PageInfo(InputObjectType):
    pass


class Query(ObjectType):
    stock = Field(StockType, code=String(required=True))
    FilterByNickname = Field(FilterType, nickname=String(required=True))


    @staticmethod
    def resolve_stock(root, info, code):
        try:
            return Stock.objects.get(code=code)
        except Stock.DoesNotExist:
            return None

    @staticmethod
    def resolve_users(root, info, nickname):
        try:
            return User.objects.all()
        except Stock.DoesNotExist:
            return []


schemas = Schema(query=Query)
