from django.shortcuts import render,HttpResponse
import json
# Create your views here.
from django.views import View
from app01.models import *
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from app01.serializer import *


class PublishView(APIView):
    def get(self,request):
        # 序列化方法一
        # publisth_list = list(Publish.objects.all().values("id","name","email"))
        # return HttpResponse(json.dumps(publisth_list))

        # 序列化方法二
        # publish_list = Publish.objects.all()
        # temp = []
        # for publish in publish_list:
        #     temp.append({"id":publish.id,
        #                  "name":publish.name,
        #                  "email":publish.email,
        #                  })
        # return HttpResponse(json.dumps(temp))

        # 序列化方法三
        # from django.forms.models import model_to_dict
        # publish_list = Publish.objects.all()
        # temp = []
        # for obj in publish_list:
        #     temp.append(model_to_dict(obj))
        # return HttpResponse(json.dumps(temp))
        #
        # 序列化方法四
        # from django.core import serializers
        # publish_list = Publish.objects.all()
        # ret = serializers.serialize("json",publish_list)
        # return HttpResponse(ret)

        # 序列化方式四 restframwork
        # publish_list = Publish.objects.all()
        # ps = PublishSerializers(publish_list,many=True)
        # return HttpResponse(ps.data)
        publish_list = Publish.objects.all()
        ps = PublishSerializers(publish_list,many=True)
        return Response(ps.data)

    def post(self,request):
        # 取数据
        # print("request.POST",request.POST)
        # print("request.BODY",request.body)
        # print("request.DATA",request.data)
        # print("request.DATA type",type(request.data))
        ps = PublishSerializers(data=request.data)
        if ps.is_valid():
            ps.save()
        return Response(ps.data)

class PublishDetailVies(APIView):
    def get(self,request,id):
        publish = Publish.objects.filter(pk=id).first()
        ps = PublishSerializers(publish)
        return Response(ps.data)

    def put(self,request,id):
        publish = Publish.objects.filter(pk=id).first()
        ps = PublishSerializers(publish,data=request.data)
        if ps.is_valid():
            ps.save()
            return Response(ps.data)
        else:
            return Response(ps.errors)

    def delete(self,request,id):
        Publish.objects.filter(pk=id).delete()
        return Response()

# class TokenAuth(object):
#     pass
from .utils import TokenAuth

class BookView(APIView):
    # 定义认证类
    # authentication_classes = [TokenAuth]

    def get(self,request):
        book_list = Book.objects.all()
        bs = BookModelSerializers(book_list,many=True,context={'request': request})
        return Response(bs.data)
    def post(self,request):
        # post 请求的数据
        bs = BookModelSerializers(data = request.data)
        if bs.is_valid():
            print(bs.validated_data)
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)

class BookDetailView(APIView):
    def get(self,request,id):
        book = Book.objects.filter(pk=id).first()
        bs = BookModelSerializers(book,context={'request': request})
        return Response(bs.data)

    def put(self,request,id):
        book = Book.objects.filter(pk=id).first()
        bs = BookModelSerializers(book,request.data)
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)

    def delete(self,request,id):
        Book.objects.filter(pk=id).delete()
        return Response()

from rest_framework import viewsets
class AuthorModelView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorModelSerializers

def get_random_str(user):
    import random,time,hashlib
    ctime = str(time.time())
    md5 = hashlib.md5(bytes(user,encoding='utf8'))
    md5.update(bytes(ctime,encoding='utf8'))
    return md5.hexdigest()


from django.http import JsonResponse
class LoginView(APIView):
    def post(self,request):
        name = request.data.get("name")
        password = request.data.get("password")
        response = {"state_code":1000,"msg":None}
        user = User.objects.filter(name=name,password=password).first()
        print(user)
        if user:
            random_str = get_random_str(user.name)
            token = Token.objects.update_or_create(user=user,defaults={"token":random_str})
            response["token"] = random_str
            response["msg"] = "登入成功"
        else:
            response["state_code"] = 1001
            response["msg"] = "用户名或者密码错误"
        # return Response(json.dumps(response,ensure_ascii=False))
        return JsonResponse(response, json_dumps_params={"ensure_ascii": False})