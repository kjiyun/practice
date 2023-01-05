from rest_framework import serializers
from community.models import FreeBoard, BoardComment, BoardPhoto, User


class BoardPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardPhoto
        fields = '__all__'


class FreeBoardDetailSerializer(serializers.ModelSerializer):
    photos = BoardPhotoSerializer(many=True, read_only=True)
    nickname = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    
    class Meta:
        model = FreeBoard
        fields = [
            'id',
            'title',
            'nickname',
            'writer',
            'created',
            'updated',
            'photos',
            'content',
        ]

    def get_nickname(self, obj):
        return obj.writer_name.nickname

    def get_writer(self, obj):
        return obj.writer_name.email

class FreeBoardListSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    
    class Meta:
        model = FreeBoard
        fields = [
            'id',
            'title',
            'nickname',
            'writer',
            'created',
            'updated',
            'content',
        ]

    def get_nickname(self, obj):
        return obj.writer_name.nickname

    def get_writer(self, obj):
        return obj.writer_name.email

    # def count_like(self, )
