from rest_framework import serializers
from django.apps import apps

class DynamicModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
        if model:
            self.Meta.model = model
            self.Meta.fields = '__all__'

    class Meta:
        fields = '__all__'