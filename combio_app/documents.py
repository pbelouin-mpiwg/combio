from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Record, Collection


@registry.register_document
class RecordDocument(Document):
    collection = fields.ObjectField(properties={"pk": fields.KeywordField(), "name": fields.TextField()})
    metadata = fields.NestedField()
    title = fields.TextField()
    permalink = fields.TextField()
    interviewers = fields.ListField(fields.TextField())
    interviewees = fields.ListField(fields.TextField())
    participants = fields.ListField(fields.TextField())

    def prepare_metadata(self, instance):
        return instance.metadata

    def prepare_interviewers(self, instance):
        return [p["name"] for p in instance.metadata["combio"]["participants"] if p["role"] == "interviewer"]

    def prepare_interviewees(self, instance):
        return [p["name"] for p in instance.metadata["combio"]["participants"] if p["role"] == "interviewee"]

    def prepare_participants(self, instance):
        return [p["name"] for p in instance.metadata["combio"]["participants"] if p["role"] == "participant"]

    def prepare_title(self, instance):
        return instance.metadata["combio"]["title"]

    class Index:
        # Name of the Elasticsearch index
        name = "records"
        # See Elasticsearch Indices API reference for available settings
        settings = {"number_of_shards": 1, "number_of_replicas": 0, "max_result_window": 20000}

    class Django:
        model = Record  # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ["id", "transcript"]
        related_models = [Collection]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(RecordDocument, self).get_queryset().select_related("collection")

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Record instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Collection):
            return related_instance.record_set.all()

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True

        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False

        # Paginate the django queryset used to populate the index with the specified size
        # (by default it uses the database driver's default setting)
