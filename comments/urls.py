from django.urls import path
from . import views

urlpatterns = [
    path(
        'add_comment/<int:product_id>/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        'edit_comment/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment'
    ),
    path(
        'delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment'
    ),
]
