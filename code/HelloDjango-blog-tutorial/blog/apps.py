from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    # TODO 修改 app 在 admin 后台的显示名字
    verbose_name = '博客'

