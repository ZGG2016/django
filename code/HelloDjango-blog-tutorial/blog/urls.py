from django.urls import path

from . import views

# TODO 这个 urls.py 文件将用于 blog 应用相关的 URL 配置，这样便于模块化管理

# TODO 通过 app_name 指定的命名空间来区分各应用下的视图函数
app_name = 'blog'
urlpatterns = [
    # TODO django 会把第一个参数字符串和后面 include 的 urls.py 文件中的 URL 拼接
    path('', views.IndexView.as_view(), name='index'),
    # TODO 路由匹配规则  匹配如 posts/1/、 posts/255/  <int:pk> 匹配 255，那么这个 255 会在调用视图函数 detail 时被传递进去，其参数名就是冒号后面指定的名字 pk
    # path('posts/<int:pk>/', views.detail, name='detail'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    # path('search/', views.search, name='search'),
]
