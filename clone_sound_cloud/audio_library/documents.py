from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from audio_library.models import Track


@registry.register_document
class TrackDocument(Document):
    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    # user = fields.ObjectField(
    #     attr='user',
    #     properties={
    #         'id': fields.IntegerField(),
    #         'email': fields.TextField(
    #             attr='email',
    #             fields={
    #                 'raw': fields.KeywordField(),
    #             }
    #         )
    #     }
    # )

    class Index:
        name = 'tracks'

    class Django:
        model = Track
