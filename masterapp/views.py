from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadData

from masterapp.models import Couser, UnverifiedCouser
from masterapp.serializers import CouserSerializer

import jwt
import json
from rest_framework.response import Response
from django.core.mail import send_mail
key = 'abhishek'
url_safe_serializer_obj = URLSafeTimedSerializer(key)

# Create your views here.

# class Loaduser(APIView):

    # def get()
    # """
    # List all snippets, or create a new snippet.
    # """
    # def get(self, request, format=None):
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)


class SignIn(APIView):
    def post(self, request, format=None):

        try:
            email = request.data['email']
            password = request.password['password']

            #TODO encrypted password task
            #check if user exist with these credentials

            try:
                print("hello"*100)
                couser = Couser.objects.get(email=email, password=password)
                payload = {
                'id': couser.id,
                'email': couser.email,
                'username': couser.username
                }

                token =  jwt.encode(payload, key)
                message = "Signed In successfuly"
                severity = "success"
                custom_status = "201"
                data = {
                    
                    'token':token,
                    "message": message,
                    "severity": severity,
                    "custom_status":custom_status
                }
                return Response(data)
            except Couser.DoesNotExist:
                message = "Invalid Username or Password"
                severity = "error"
                custom_status:"400"
                data = {
                    "message": message,
                    "severity": severity,
                    "custom_status":"400"
                }
                return Response(data)

class LoadUser(APIView):
    def get(self, request, *args, **kwargs):
        message = ""
        severity = ""
        custom_status = ""
        auth_status = ""
        auth_status_detail = ""
        data = {}
        # token = request.headers["Token"]
        id = request.id

        try:
            couser_obj = Couser.objects.get(id=id)
            serializer = CouserSerializer(couser_obj)
            data = {
                "couser":serializer.data,
                "message":"successful",
                "custom_status":"201",
                "severity":"success"
            }
            return Response(data)
        except:
            data = {
                'couser': "",
                'message': message,
                'severity': severity,
                'custom_status': custom_status,
                'auth_status':auth_status,
                'auth_status_detail':auth_status_detail
                }
            return Response(data)
