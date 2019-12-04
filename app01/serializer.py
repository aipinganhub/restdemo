#!/usr/bin/python
# -*- coding:utf-8 -*-
#
#Filename:

from rest_framework import serializers
from app01.models import *

# 为quseryset做序列化的类，用的是restframework中的serializers
class PublishSerializers(serializers.ModelSerializer):

    class Meta:
        model = Publish
        fields = "__all__"


# class BookSerializers(serializers.Serializer):
#     title=serializers.CharField(max_length=32)
#     price=serializers.IntegerField()
#     pub_date=serializers.DateField()
#     publish=serializers.CharField(source="publish.name")
#     authors=serializers.SerializerMethodField()
#     def get_authors(self,obj):
#         temp = []
#         for obj in obj.authors.all():
#             temp.append(obj.pk)
#         return temp

class BookModelSerializers(serializers.ModelSerializer):
    # 显示超级链接
    publish=serializers.HyperlinkedIdentityField(
        view_name="publish_detail",
        lookup_field="publish_id",
        lookup_url_kwarg="id",
    )
    class Meta:
        model = Book
        fields = "__all__"
    # publish=serializers.CharField(source="publish.pk")
    # authors=serializers.SerializerMethodField()
    # def get_authors(self,obj):
    #     temp = []
    #     for obj in obj.authors.all():
    #         temp.append(obj.pk)
    #     return temp

    # 如果定制了modelserialiszers的字段，就需要重写create方法，不然会按照默认的方法写就无法写入数据
    # def create(self,validated_data):
    #     print("validated_data:",validated_data)
    #     book = Book.objects.create(title=validated_data["title"],
    #                         price=validated_data["price"],
    #                         pub_date=validated_data['pub_date'],
    #                         publish_id=validated_data["publish"]['pk'],
    #                         )
    #     book.authors.add(*validated_data["authors"])
    #     return book

class AuthorModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
