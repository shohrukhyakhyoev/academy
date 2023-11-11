from django.contrib import admin
from config import settings
from django.urls import include, path
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from community.forms import CustomAuthForm
from community.views import (
    register, 
    questions,
    question,    
    create_question,
    update_question,
    update_answer,
    update_answer_comment
)

from blog.views import (
    PostDetailView,
    create_post,
    update_post,
    delete_post,
    get_posts,

    contact,
    about,
    index
)

from course.views import (
    tutorials
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', index, name='index'),


    path('community/login/', auth_views.LoginView.as_view(template_name='auth/login.html', authentication_form=CustomAuthForm), name='login'),
    path('community/signup/', register, name='signup'),
    path('community/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('community/questions/', questions, name='questions'),
    path('community/questions/<pk>/<slug:slug>/', question, name='question'),
    path('community/questions/<pk>/<slug:slug>/update/', update_question, name='edit_question'),
    path('community/question/create/', create_question, name='create_question'),
    path('community/answers/<pk>/update/', update_answer, name='edit_answer'),
    path('community/answers/comments/<pk>/update/', update_answer_comment, name='edit_answer_comment'),

    path('posts/', get_posts, name='posts'),
    path('posts/<pk>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/<pk>/<slug:slug>/update/', update_post, name='post_update'),
    path('posts/<pk>/<slug:slug>/delete/', delete_post, name='post_delete'),

    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),

    path('tutorials/', tutorials, name='tutorials'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)