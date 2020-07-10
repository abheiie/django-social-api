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

from masterapp.models import (Couser, Contact, Category, Post, Like, Bookmark, Comment, EntityType, ReportType, Report, UnverifiedCouser)
from masterapp.serializers import CouserSerializer, CommentSerializer, PostSerializer

import jwt
import json
from rest_framework.response import Response
from django.core.mail import send_mail
key = 'abhishek'
url_safe_serializer_obj = URLSafeTimedSerializer(key)

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


class SignUp(APIView):
    def post(self, request, *args, **kwargs):

        message = ""
        severity = ""
        custom_status = ""
        auth_status = ""
        auth_status_detail = ""
        data = {}
        try:
            fullname = request.data['fullname']
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']

            username_obj = Couser.objects.filter(username=username)
            username_obj_unverified = UnverifiedCouser.objects.filter(
                username=username)

            email_obj = Couser.objects.filter(email=email)

            if username_obj.count() != 0 and username_obj_unverified.count() != 0:
                message = "This username is already taken, Please choose another username "
                severity = "error"
                custom_status = "400"

            elif email_obj.count() != 0:
                message = "This email is already registered, please go to login page if you are already registered"
                severity = "error"
                custom_status = "400"
            else:
                unverified_couser = UnverifiedCouser(
                    fullname=fullname, username=username, email=email)

                # TODO save encrypted password
                unverified_couser.password = password
                unverified_couser.save()

                # sent email confirmation link
                unverified_couser_id = str(unverified_couser.id)
                token = url_safe_serializer_obj.dumps(unverified_couser_id)
                link = "http://localhost:3000/sign-up-email-confirmation/" + token

                # link = "http://127.0.0.1:8000/auth/email-confirmation/"+token
                send_mail(
                    'Signedup successfuly on vismrita.com',
                    link,
                    'colorles7@gmail.com',
                    [email],
                    fail_silently=False,
                )
                message = "Signed up successfully, please check your email inbox and verify email"
                severity = 'success'
                custom_status = "201"
                auth_status = "Sign Up Successful"
                auth_status_detail = "Singned up successfully, please check your email inbox to verify your email, thanks"

            data = {
                'message': message,
                'severity': severity,
                'custom_status': custom_status,
                'auth_status':auth_status,
                'auth_status_detail':auth_status_detail
                }
            return Response(data)
        except:
            message = "Some thing went wrong, please try again"
            severity = "error"
            custom_status = "400"
            data = {'message': message, 'severity': severity,
                    'custom_status': custom_status}
            return Response(data)


class EmailConfirmation(APIView):

    def get(self, request, token, *args, **kwargs):

        auth_status = ""
        auth_status_detail = ""
        data = {}
        custom_status = ""

        try:
            user_id = url_safe_serializer_obj.loads(token, max_age=60*60)
            unverified_couser_obj = UnverifiedCouser.objects.get(id=user_id)
            couser_obj = Couser(
                fullname=unverified_couser_obj.fullname,
                username=unverified_couser_obj.username,
                email=unverified_couser_obj.email,
                password=unverified_couser_obj.password)
            couser_obj.save()
            unverified_couser_obj.is_email_verified = True
            unverified_couser_obj.save()
            auth_status = "Email Verification Successful"
            auth_status_detail = " Your email address " + \
                str(couser_obj.email) + \
                " is verified, please go to SignIn page and login with this email"

        except SignatureExpired:
            auth_status = "Email Confirmation Unsuccessful"
            auth_status_detail = "Token in the link got expired, please go to Sign up page and request again"

        except BadData:
            auth_status = "Email Confirmation Unsuccessful"
            auth_status_detail = "Token in the link is not valid, please make sure you have clicked right link or goto to signup page to request again"

        data = {"auth_status": auth_status,
                "auth_status_detail": auth_status_detail, "custom_status": "200"}
        return Response(data)


class SignIn(APIView):
    def post(self, request, *args, **kwargs):
        

        print("name"*100)

        auth_status = ""
        auth_status_detail = ""
        data = {}
        custom_status = ""
        message = ""
        severity = ""

        try:
            print("===============request================>", request)
            print("==============================>", request.data)

            # handle incomplete data soituation here
            # if not request.data:
            #     return Response({'Error': "Please provide email or mobile and password"}, status="400")

            email = request.data['email']
            password = request.data['password']

            print(email, password)

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

        except:
            message = "Some thing went wrong"
            severity = "error"
            custom_status:"400"
            data = {
                "message": message,
                "severity": severity,
                "custom_status": custom_status
            }
            return Response(data)




class ForgotPassword(APIView):
    def post(self, request):
        message = ""
        severity = ""
        custom_status = ""
        forgot_password_token = ""
        auth_status = ""
        auth_status_detail = ""
        data = {}

        try:
            print("get the request in forget password")
            email = request.data["email"].strip()

            # check if user exist with this email or not
            couser_obj = Couser.objects.filter(email=email)
            unverified_couser_obj = UnverifiedCouser.objects.filter(
                email=email)

            if couser_obj.count() == 0 and unverified_couser_obj.count() == 0:
                message = "User with this email address does not exist, please got to signup page and Signup"
                severity = "error"
                custom_status = "400"
                forgot_password_token = ""

            elif unverified_couser_obj.count() != 0 and couser_obj.count() == 0:
                message = "A account with this email address is registerd but email is not verified, please check youe email inbox\
                or got to Signup page and sign up again"
                severity = "error"
                custom_status = "400"
                forgot_password_token = ""
            else:
                # generate a new token for forget password that will contain
                # the email that request forgot password
                forgot_password_token = url_safe_serializer_obj.dumps(email)
                link = "http://localhost:3000/forgot-password-reset/"+forgot_password_token
                send_mail(
                    'Please click on link to reset your password',
                    link,
                    'colorles7@gmail.com',
                    [email],
                    fail_silently=False,
                )
                auth_status = "Forget Password Successful"
                auth_status_detail = "Please check your email inbox, click on the link to reset password"

                message = "Please create a new password for this" + \
                    str(email) + "address"
                severity = "success"
                custom_status = "201"
            data = {
                "message": message,
                "severity": severity,
                'custom_status': custom_status,
                "forgot_password_token": forgot_password_token,
                "auth_status":auth_status,
                "auth_status_detail": auth_status_detail
                }
            return Response(data)

        except:
            message = "Some thing went wrong"
            severity = "error"
            custom_status = "500"
            forgot_password_token = ""
            data = {"message": message, "severity": severity,
                    "custom_status": custom_status, "forgot_password_token": forgot_password_token}
            return Response(data)


class ForgotPasswordReset(APIView):
    def post(self, request, token, *args, **kwargs):
        message = ""
        severity = ""
        custom_status = ""
        data = {}
        try:
            password = request.data['password']
            email = url_safe_serializer_obj.loads(token, max_age=60*60)
            couser_obj = Couser.objects.get(email=email)

            # TODO save encrypted password
            couser_obj.password = password
            couser_obj.save()
            auth_status = "Password Reset Successful"
            auth_status_detail = "Your password for " + \
                str(email)+" has been changed successfully, please goto login page and login with new password"

        except SignatureExpired:
            auth_status = "Password Reset Unsuccessful"
            auth_status_detail = "Token in the link got expired, please go to Forgot password page and request again"

        except BadData:
            auth_status = "Password Reset Unsuccessful"
            auth_status_detail = "Token in the link is not valid, please make sure you have clicked right link or goto to Forgot password page and request again"

        data = {"auth_status": auth_status,
                "auth_status_detail": auth_status_detail, "custom_status": "200"}
        return Response(data)



class BookmarkPostList(APIView):
    def get(self, request,format=None):
        data = {}
        current_username = request.username
        current_user_obj = Couser.objects.get(username = current_username)


        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))

        has_more = False
        if offset > current_user_obj.bookmarks.all().count():
            has_more = False
        else:
            has_more = True

        bookmarks = current_user_obj.bookmarks.all()[offset: offset+limit]
        bookmarks_list = []


        for bookmark in bookmarks:
            post_obj = bookmark.post
            craeter_id = post_obj.couser_id
            post = PostSerializer(post_obj).data


            # try:
            #     couser_obj = Couser.objects.get(id=craeter_id)
            #     post["fullname"] = couser_obj.fullname
            #     post["username"] = couser_obj.username
            # except:
            #     post["fullname"] = ""
            #     post["username"] = ""

            # like function===========================================
            liked = False
            try:
                like_object = Like.objects.filter(
                    couser__username = current_username, post_id=post["id"])
                if like_object.count() > 0:
                    print("likeed"*100)
                    liked = True
            except:
                pass
            post["liked"] = liked

            # bookmark function=======================================
            bookmarked = False
            try:
                bookmark_object = Bookmark.objects.filter(
                    couser__username=current_username, post_id=post["id"])
                if bookmark_object.count() > 0:
                    bookmarked = True
                    print("bookmarked"*100)
            except:
                pass
            post["bookmarked"] = bookmarked

            post["comments"] = []

            # comment function==========================================
            comments_qs = Comment.objects.filter(post_id=post["id"])[:3]
            for comment_obj in comments_qs:
                comment = {}
                commenter = Couser.objects.get(id=comment_obj.couser_id)
                comment["fullname"] = commenter.fullname
                comment["body"] = comment_obj.body
                comment["couser_id"] = comment_obj.couser_id
                comment["id"] = comment_obj.id
                comment["created_at"] = comment_obj.created_at
                post["comments"].append(comment)
            
            bookmarks_list.append(post)

        data = {
            "posts": bookmarks_list,
            "has_more": has_more
            }
        return Response(data)



class TimelinePost(APIView):
    def get(self, request, username, format=None):

        data = {}

        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))

        has_more = False
        if offset + limit > Post.objects.filter(couser__username = username).count():
            has_more = False
        else:
            has_more = True

        posts = Post.objects.filter(couser__username = username)[offset: offset+limit]
        current_user_id = request.id

        posts = PostSerializer(posts, many = True).data



        # for post in posts:
        #     craeter_id = post["couser_id"]

        #     try:
        #         couser_obj = Couser.objects.get(id=craeter_id)
        #         post["fullname"] = couser_obj.fullname
        #         post["username"] = couser_obj.username
        #     except:
        #         post["fullname"] = ""
        #         post["username"] = ""

            # # like function===========================================
            # liked = False
            # try:
            #     like_object = Like.objects.filter(
            #         couser_id=current_user_id, post_id=post["id"])
            #     if like_object.count() > 0:
            #         print("likeed"*100)
            #         liked = True
            # except:
            #     pass
            # post["liked"] = liked

            # # bookmark function=======================================
            # bookmarked = False
            # try:
            #     bookmark_object = Bookmark.objects.filter(
            #         couser_id=current_user_id, post_id=post["id"])
            #     if bookmark_object.count() > 0:
            #         bookmarked = True
            #         print("bookmarked"*100)
            # except:
            #     pass
            # post["bookmarked"] = bookmarked

            # post["comments"] = []

            # # comment function==========================================
            # comments_qs = Comment.objects.filter(post_id=post["id"])[:3]
            # for comment_obj in comments_qs:
            #     comment = {}
            #     commenter = Couser.objects.get(id=comment_obj.couser_id)
            #     comment["fullname"] = commenter.fullname
            #     comment["body"] = comment_obj.body
            #     comment["couser_id"] = comment_obj.couser_id
            #     comment["id"] = comment_obj.id
            #     comment["created_at"] = comment_obj.created_at
            #     post["comments"].append(comment)

        data = {
            "posts": posts,
            "has_more": has_more
        }
        return Response(data)

















        posts = Post.objects.filter(couser__username = username)    
        serializer = PostSerializer(posts, many = True)
        data = serializer.data
        return Response(data)
    

class AddCommentListPost(APIView):
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            print("inside"*100)
            serializer.save()
        data = serializer.data
        post = Post.objects.get(id=data["post"])
        post.comments_count = post.comments_count+1
        post.save()
        couser = Couser.objects.get(id=data["couser"])
        data["fullname"] = couser.fullname
        data["username"] = couser.username
        comments_count = Comment.objects.filter(post_id=data["post"]).count()
        return Response({"data": data, "comments_count": comments_count})


class AddCommentDetailPost(APIView):
    def post(self, request, format=None):

        print("5555"*20, request.data)
        d = request.data.copy()
        data = request.data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            print("inside"*100)
            serializer.save()
        data = serializer.data
        couser = Couser.objects.get(id=data["couser"])
        data["fullname"] = couser.fullname
        data["username"] = couser.username
        data["couser_id"] = couser.id
        comments_count = Comment.objects.filter(post_id=data["post"]).count()
        return Response({"data": data, "comments_count": comments_count})


class CommentDetailPost(APIView):
    def delete(self, request, comment_id, format=None):
        print("TTTTT"*100)
        comment = Comment.objects.get(id=comment_id)
        post_id = comment.post.id
        comment.delete()
        data = {}
        data["post_id"] = post_id
        data["comment_id"] = comment_id
        data["comments_count"] = Comment.objects.filter(
            post_id=post_id).count()
        return Response(data)

# get comments for detail post


class CommentList(APIView):
    def get(self, request, post_id, format=None):

        print("--------------limit-------->", request.GET.get('limit'))
        print("--------------offset-------->", request.GET.get('offset'))


        data = {}
        current_user_id = request.id

        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))

        has_more = False

        comments_count = Comment.objects.filter(post_id=post_id).count()

        if offset > comments_count:
            has_more = False
        else:
            has_more = True

        comments = Comment.objects.filter(post_id=post_id)[
            offset: offset+limit].values()
        for comment in comments:
            couser = Couser.objects.get(id=comment["couser_id"])
            comment["fullname"] = couser.fullname
            comment["username"] = couser.username

        data = {
            "comments": comments,
            "has_more": has_more,
            "comments_count":comments_count
        }

        return Response(data)


class Report(APIView):
    def post(self, request, format=None):
        # data = request.data.copy()
        # data["couser"] = request.id

        serializer = ReportSerializer(data=request.data)
        print("---------------->", request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get all the posts along with comment likes and bookmark


class PostsList(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):

        data = {}

        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))

        has_more = False
        if offset+limit > Post.objects.all().count():
            has_more = False
        else:
            has_more = True

        posts = Post.objects.all()[offset: offset+limit].values()
        current_user_id = request.id

        print("********"*30, current_user_id)

        for post in posts:
            craeter_id = post["couser_id"]

            try:
                couser_obj = Couser.objects.get(id=craeter_id)
                post["fullname"] = couser_obj.fullname
                post["username"] = couser_obj.username
            except:
                post["fullname"] = ""
                post["username"] = ""

            # like function===========================================
            liked = False
            try:
                like_object = Like.objects.filter(
                    couser_id=current_user_id, post_id=post["id"])
                if like_object.count() > 0:
                    print("likeed"*100)
                    liked = True
            except:
                pass
            post["liked"] = liked

            # bookmark function=======================================
            bookmarked = False
            try:
                bookmark_object = Bookmark.objects.filter(
                    couser_id=current_user_id, post_id=post["id"])
                if bookmark_object.count() > 0:
                    bookmarked = True
                    print("bookmarked"*100)
            except:
                pass
            post["bookmarked"] = bookmarked

            post["comments"] = []

            # comment function==========================================
            comments_qs = Comment.objects.filter(post_id=post["id"])[:3]
            for comment_obj in comments_qs:
                comment = {}
                commenter = Couser.objects.get(id=comment_obj.couser_id)
                comment["fullname"] = commenter.fullname
                comment["body"] = comment_obj.body
                comment["couser_id"] = comment_obj.couser_id
                comment["id"] = comment_obj.id
                comment["created_at"] = comment_obj.created_at
                post["comments"].append(comment)

        data = {
            "posts": posts,
            "has_more": has_more
        }
        return Response(data)

    def post(self, request, format=None):
        data = request.data.copy()
        data["couser"] = request.id
        serializer = PostSerializer(data=data)

        print("---------------->", request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update like ========================================================
class UpdateLike(APIView):
    def post(self, request, post_id, format=None):
        data = {}
        current_user_id = request.id

        try:
            like = Like.objects.get(post_id=post_id, couser_id=current_user_id)
        except:
            like = None

        # if already liked
        if like is not None:
            like.delete()
            post = Post.objects.get(id=post_id)
            post.likes_count = post.likes_count - 1
            post.save()

            data["post_id"] = post.id
            data["liked"] = False
            data["likes_count"] = post.likes_count

        # if not already liked
        else:

            print("================> if not already liked ")

            like = Like(couser_id=current_user_id, post_id=post_id)
            like.save()
            post = Post.objects.get(id=post_id)
            post.likes_count = post.likes_count + 1
            post.save()
            # self.notification(sender_id = current_user_id, receiver_id = post.couser_id, entity_id_username = post.id, entity_type = "post", notification_type = "like"  )
            data["post_id"] = post.id
            data["liked"] = True
            data["likes_count"] = post.likes_count
        return Response(data)

    def notification(self, sender_id, receiver_id, entity_id_username, entity_type, notification_type, format=None):
        notification_qs = Notification.objects.filter(receiver_id=receiver_id)
        if notification_qs.count() > 30:
            notification_qs.last().delete()
            notification_obj = Notification(
                sender_id=sender_id,
                receiver_id=receiver_id,
                entity_id_username=entity_id_username,
                entity_type=entity_type,
                notification_type=notification_type)
            notification_obj.save()
        else:
            notification_obj = Notification(
                sendePostDetailr_id=sender_id,
                receiver_id=receiver_id,
                entity_id_username=entity_id_username,
                entity_type=entity_type,
                notification_type=notification_type)
            notification_obj.save()

# update bookmark ========================================================


class UpdateBookmark(APIView):
    def post(self, request, post_id, format=None):
        data = {}
        current_user_id = request.id

        try:
            bookmark = Bookmark.objects.get(
                post_id=post_id, couser_id=current_user_id)
        except:
            bookmark = None

        # if already bookmarked
        if bookmark is not None:
            bookmark.delete()
            post = Post.objects.get(id=post_id)
            post.bookmarks_count = post.bookmarks_count - 1
            post.save()

            data["post_id"] = post.id
            data["bookmarked"] = False
            data["bookmarks_count"] = post.bookmarks_count

        # if not already liked
        else:

            bookmark = Bookmark(couser_id=current_user_id, post_id=post_id)
            bookmark.save()
            post = Post.objects.get(id=post_id)
            post.bookmarks_count = post.bookmarks_count + 1
            post.save()
            data["post_id"] = post.id
            data["bookmarked"] = True
            data["bookmarks_count"] = post.bookmarks_count
        return Response(data)


class PostListDetail(APIView):
    def delete(self, request, post_id, format=None):
        post = Post.objects.get(id=post_id)
        post.delete()
        data = {}
        data["post_id"] = post_id

        return Response(data)


class CommentDetail(APIView):
    def delete(self, request, comment_id, format=None):
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        data = {}
        post_id = comment.post.id
        data["post_id"] = post_id
        data["comment_id"] = comment_id
        return Response(data)


class PostDetail(APIView):
    def get(self, request, post_id, format=None):
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        data = serializer.data
        current_user_id = request.id

    # like function===========================================
        liked = False
        try:
            like_object = Like.objects.filter(
                couser_id=current_user_id, post_id=post.id)
            if like_object.count() > 0:
                print("likeed"*5)
                liked = True
        except:
            pass
        data["liked"] = liked

        # bookmark functGET_POST_ERRORion=======================================
        bookmarked = False
        try:
            bookmark_object = Bookmark.objects.filter(
                couser_id=current_user_id, post_id=post.id)
            if bookmark_object.count() > 0:
                bookmarked = True
                print("bookmarked"*100)
        except:
            pass
        data["bookmarked"] = bookmarked
        return Response(data)




class Profile(APIView):
    """
    get individual profile
    """

    def get_object(self, username):
        try:
            return Couser.objects.get(username = username)
        except Couser.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        couser = self.get_object(username)
        serializer = CouserSerializer(couser)
        # TODO username instead of id
        #     try:
        #         check = Contact.objects.get(
        #             follower_id=request.id, following_id=id)
        #     except:
        #         check = None

        #     is_following_this = False
        #     if check is not None:
        #         is_following_this = True
        #         data["is_following_this"] = is_following_this
        return Response(serializer.data)

class People(APIView):
    def get(self, request, *args, **kwargs):

        data = {}
        current_user_id = request.id

        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))

        has_more = False

        if offset+limit > Couser.objects.exclude(id=current_user_id).count():
            has_more = False
        else:
            has_more = True

        people = Couser.objects.exclude(id=current_user_id)[offset: offset+limit].values()
        for person in people:
            follower_id = current_user_id
            following_id = person["id"]

            check = None

            try:
                check = Contact.objects.get(follower_id= current_user_id , following_id = person["id"])
            except:
                check = None
            
            is_following_this  = False
            if check is not None:
                is_following_this = True
            person["is_following_this"] = is_following_this
        data = {
            "people":people,
            "has_more":has_more
        }
        return Response(data)


class Follower(APIView):
    ''' get the follower of user whome user_id is passed here, 
        this gives all followers of user with user_id provide '''

    def get(self, request, username, format=None):

        data = {}
        current_user_id = request.id

        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))

        has_more = False

        if offset+limit > Couser.objects.exclude(id=current_user_id).count():
            has_more = False
        else:
            has_more = True

        followers = Contact.objects.filter(following__username = username )[offset: offset+limit].values()

        for follower in followers:
            follower_id = follower["follower_id"]
            following_id = follower["following_id"]
            couser = Couser.objects.get(id = follower_id)
            follower["username"] = couser.username
            follower["fullname"] = couser.fullname
            follower["avatar"] = "avatar"

            check = None

            #to check if current user is following this user or not
            try:
                check = Contact.objects.get(follower_id= current_user_id, following_id = follower_id)
            except:
                check = None
            
            is_following_this  = False
            if check is not None:
                is_following_this = True
            follower["is_following_this"] = is_following_this
        data = {
            "followers":followers,
            "has_more":has_more
        }
        return Response(data)

        


class Following(APIView):
    ''' 
    get the following of user whome username is passed here
    '''
    def get(self, request, username, format=None):

        data = {}
        current_user_id = request.id

        limit = int(request.GET.get('limit'))
        offset = int(request.GET.get('offset'))

        has_more = False
        if offset+1 > Couser.objects.exclude(id=current_user_id).count():
            has_more = False
        else:
            has_more = True

        followings = Contact.objects.filter(follower__username = username )[offset: offset+limit].values()
        

        for following in followings:
            follower_id = following["follower_id"]
            following_id = following["following_id"]
            couser = Couser.objects.get(id = following_id)
            following["username"] = couser.username
            following["fullname"] = couser.fullname

            check = None

            #to check if current user is following this user or not
            try:
                check = Contact.objects.get(follower_id= current_user_id, following_id = following_id)
            except:
                check = None
            

            is_following_this  = False
            if check is not None:
                is_following_this = True
            following["is_following_this"] = is_following_this

        data = {
            "followings":followings,
            "has_more":has_more
        }

        return Response(data)


class UpdateContacts(APIView):
    def post(self, request, username, format=None):
        couser_id = request.id

        try:
            contact = Contact.objects.get(
                follower_id=couser_id, following__username=username)
        except:
            contact = None


        # if already following
        if contact is not None:
            contact.delete()

            follower = Couser.objects.get(id=couser_id)
            follower.followings_count = follower.followings_count - 1
            follower.save()

            following = Couser.objects.get(username = username)
            following.followers_count = following.followers_count - 1
            following.save()

            serializer = CouserSerializer(following)
            data = serializer.data
            data["is_following_this"] = False


        # if not already following
        else:
            following_id = Couser.objects.get(username = username).id
            contact = Contact(follower_id=couser_id, following_id=following_id)
            follower = Couser.objects.get(id=couser_id)
            follower.followings_count = follower.followings_count + 1
            follower.save()

            following = Couser.objects.get(username = username)
            following.followers_count = following.followers_count + 1
            following.save()
            contact.save()

            serializer = CouserSerializer(following)
            data = serializer.data
            data["is_following_this"] = True
            
        return Response(data)

class EditProfile(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, format=None):
        couser = Couser.objects.get(id = request.id)
        serializer = CouserSerializer(couser)
        return Response(serializer.data)


    def put(self, request, format=None,*args, **kwargs):

        id = request.id
        print("==============================>", request.data)

        couser = Couser.objects.get(pk=id)
        serializer = CouserSerializer(couser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



