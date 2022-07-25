import graphene
from graphene import *
from stock.schema import *
from member.schema import *


class PageInfo(graphene.ObjectType):
    begin = graphene.Int()
    size = graphene.Int()
    has_next = graphene.Boolean()

    @staticmethod
    def resolve_page_info(root, info, begin, size, has_next):
        return {'begin': begin, 'size': size, 'has_next': has_next}


class PageInfoInput(graphene.InputObjectType):
    begin = graphene.Int()
    page_size = graphene.Int()


class ReportInput(graphene.InputObjectType):
    date = graphene.Date(required=True)
    stock_codes = graphene.List(graphene.NonNull(String), name='stock_codes')


class PostReports(graphene.Mutation):
    class Arguments:
        report_input = ReportInput(required=True, name='report_input')
        page_info = PageInfoInput(name='page_info')

    result = graphene.Boolean()
    page_info = graphene.Field(PageInfo)

    def mutate(self, info, report_input, page_info=None):
        print(report_input, page_info)

        if not page_info:
            page_info = PageInfo(begin=0, size=10, has_next=False)

        page_info = PageInfo(begin=0, size=10, has_next=False)
        return PostReports(result=True, page_info=page_info)


class Mutation(ObjectType):
    post_reports = PostReports.Field()


class Query(ObjectType):
    stock = Field(StockType, code=String(required=True))
    filter_by_owner_nickname = Field(FilterType, nickname=String(required=True))
    filter_by_name = Field(FilterType, name=String(required=True))

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


schemas = Schema(query=Query, mutation=Mutation)
