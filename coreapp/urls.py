from django.urls import path
from coreapp.views import SignUp, SignIn, EmailConfirmation, ForgotPassword, ForgotPasswordReset, LoadUser

from coreapp.views import (
    PostsList,
    UpdateLike,
    UpdateBookmark,
    Report, PostListDetail,
    CommentDetail, PostDetail,
    CommentList,
    CommentDetailPost,
    AddCommentDetailPost,
    AddCommentListPost,
    TimelinePost,
    BookmarkPostList,
)

from coreapp.views import Profile, People, UpdateContacts, Follower, Following, EditProfile
from django.conf import settings 


app_name = 'coreapp'

urlpatterns = [
    path('signup/', SignUp.as_view(), name = "sign_up"),
    path('signin/', SignIn.as_view(), name = "sign_in"),
    path('load-user', LoadUser.as_view(), name = "load-user"),
    path('sign-up-email-confirmation/<str:token>', EmailConfirmation.as_view()),
    path('forgot-password/', ForgotPassword.as_view()),
    path('forgot-password-reset/<str:token>/', ForgotPasswordReset.as_view()),


    path('timeline-post/<str:username>/', TimelinePost.as_view(), name = "timeline-post"),
    path('posts/', PostsList.as_view(), name = "posts-list"),
    path('update-like/<int:post_id>/', UpdateLike.as_view(), name = "update-like"),
    path('update-bookmark/<int:post_id>/', UpdateBookmark.as_view(), name = "update-bookmark"),
    path('report/', Report.as_view(), name = "report"),
    path('posts/<int:post_id>/', PostListDetail.as_view(), name = "delete-postlists-post"),
    path('comments/<int:comment_id>/', CommentDetail.as_view(), name = "delete-postlists-comment"),
    path('post/<int:post_id>/', PostDetail.as_view(), name = "post-detail"),
    path('comment/<int:post_id>/', CommentList.as_view(), name = "post-detail-comment"),
    path('comment-detail-post/<int:comment_id>/', CommentDetailPost.as_view(), name = "post-detail-comment-detail"),
    path('add-comment-detail-post/', AddCommentDetailPost.as_view(), name = "add-comment-detail-post"),
    path('comment-post-list/', AddCommentListPost.as_view(), name = "comment-post-list"),
    path('bookmark-posts-list/', BookmarkPostList.as_view(), name = "bookmark-posts-list"),
    path('update-like-for-bookmark-list/<int:post_id>/', UpdateLike.as_view(), name = "update-like-for-bookmark-list"),
    path('update-bookmark-for-bookmark-list/<int:post_id>/', UpdateBookmark.as_view(), name = "update-bookmark-for-bookmark-list"),
    path('comment-on-bookmark-post-list/', AddCommentListPost.as_view(), name = "comment-on-bookmark-post-list"),
    path('delete-post-from-bookmark-post-list/<int:post_id>/', PostListDetail.as_view(), name = "delete-post-from-bookmark-post-list"),


    path('profile/<str:username>/', Profile.as_view(), name = "get-profile"),
    path('people/', People.as_view(), name = "people"),
    path('update-contacts/<str:username>/', UpdateContacts.as_view(), name= "update-contacts"),
    path('followers/<str:username>/', Follower.as_view(), name= "followers"),
    path('followings/<str:username>/', Following.as_view(), name= "followings"),
    path('edit-profile/', EditProfile.as_view(), name= "edit-profile")


]
