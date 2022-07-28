from graphene import *
from stock.schema import *
from member.schema import *


class PageInfo(ObjectType):
    begin = Int()
    size = Int()
    has_next = Boolean()

    @staticmethod
    def resolve_page_info(root, info, begin, size, has_next):
        return {'begin': begin, 'size': size, 'has_next': has_next}


class PageInfoInput(InputObjectType):
    begin = Int()
    page_size = Int()


class ReportInput(InputObjectType):
    date = Date(required=True)
    stock_codes = List(NonNull(String), name='stock_codes')


class PostReports(Mutation):
    class Arguments:
        report_input = ReportInput(required=True, name='report_input')
        page_info = PageInfoInput(name='page_info')

    result = Boolean()
    page_info = Field(PageInfo)

    def mutate(self, info, report_input, page_info=None):
        print(report_input, page_info)

        if not page_info:
            page_info = PageInfo(begin=0, size=10, has_next=False)

        page_info = PageInfo(begin=0, size=10, has_next=False)
        return PostReports(result=True, page_info=page_info)


class Mutation(ObjectType):
    post_reports = PostReports.Field()


class Query(ObjectType):
    filters = Field(List(NonNull(FilterType)), title=String(), owner=String(), required=True)
    filter = Field(FilterType, id=ID(required=True, name='id'))
    user = Field(UserType, nickname=String())

    @staticmethod
    def resolve_user(root, info, nickname):
        try:
            return User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return None

    @staticmethod
    def resolve_filters(root, info, title=None, owner=None):
        if title and owner:
            try:
                user = User.objects.get(nickname=owner)
                filters = Filter.objects.filter(owner=user, title=title)
                return filters
            except User.DoesNotExist:
                return []
            except Filter.DoseNotExist:
                return []
        elif title:
            try:
                filters = Filter.objects.filter(title=title)
                return filters
            except Filter.DoseNotExist:
                return []
        elif owner:
            try:
                user = User.objects.get(nickname=owner)
                filters = Filter.objects.filter(owner=user)
                return filters
            except User.DoesNotExist:
                return []
            except Filter.DoseNotExist:
                return []
        else:
            return []

    @staticmethod
    def resolve_filter(root, info, id):
        try:
            _filter = Filter.objects.get(pk=id)
            return _filter
        except Filter.DoesNotExist:
            return None


schemas = Schema(query=Query, mutation=Mutation)
