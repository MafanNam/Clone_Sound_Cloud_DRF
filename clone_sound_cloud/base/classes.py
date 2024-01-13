from rest_framework.pagination import PageNumberPagination


class MixedSerializer:
    """Serializer action's mixin"""

    def get_serializer(self, *args, **kwargs):
        try:
            serializer_class = self.serializer_classes_by_action[self.action]
        except KeyError:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class TrackAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 10000
