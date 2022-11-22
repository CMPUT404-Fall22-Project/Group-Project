from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Author
        # currently not including followers or isAuthorized
        fields = ["id","type","host","url","displayName","github","profileImage"]


    def get_id(self, obj: Author):
        return obj.get_full_path()

    def get_url(self, obj: Author):
        return self.get_id(obj)
