from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from rest_framework import status, exceptions
from django.http import HttpResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from masterapp.models import Couser
import jwt
import json
from django.http import JsonResponse
import re
key = 'abhishek'
from django.urls import resolve



class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.



    def __call__(self, request):

        print("request path-------------->", request.path)
        protected_request_list = []

        protected_request_list.extend([
            'load-user',
            'get-profile',
            'people',
            'update-contacts',
            'followers'
            'followings',
            'edit-profile',
            "posts-list",
            "update-like",
            "update-bookmark",
            "report",
            "delete-postlists-post",
            "delete-postlists-comment",
            "post-detail",
            "post-detail-comment",
            "post-detail-comment-detail",
            "add-comment-detail-post",
            "comment-post-list",
            "timeline-post",
            "bookmark-posts-list",
            "update-like-for-bookmark-list",
            "update-bookmark-for-bookmark-list",
            "comment-on-bookmark-post-list",
            "delete-post-from-bookmark-post-list",
            ])
        namespaces_ = resolve(request.path)
        if namespaces_.url_name in protected_request_list:

            # if token is present
            if 'X-Auth-Token' in request.headers:
                token = request.headers["X-Auth-Token"]
                try:
                    payload = jwt.decode(token, key)
                    request.id = payload["id"]
                    request.email = payload["email"]
                    request.username = payload["username"]
                    response = self.get_response(request)
                    return response
                except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
                    auth_status = ""
                    auth_status_detail = ""
                    custom_status = "400"
                    message = "Token is invalid"
                    severity = "error"
                    data = {}
                    return Response({'Error': "Token is invalid"})

            else:
                return JsonResponse({'Error': "Tokenva re is not found"}, status="401")
        else:

            print("fall"*200)
            response = self.get_response(request)
            return response