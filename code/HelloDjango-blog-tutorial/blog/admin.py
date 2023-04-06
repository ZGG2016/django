from django.contrib import admin
from .models import Post, Category, Tag


# TODO PostAdmin 来配置 Post 在 admin 后台的一些展现形式
class PostAdmin(admin.ModelAdmin):
    # TODO list_display 属性控制在admin页面的 Post 列表页展示文章的更多信息
    list_display = ['title', 'created_time', 'modified_time', 'views', 'category', 'author']
    # TODO 控制在admin页面表单展现的字段
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        # TODO 文章作者自动设定为登录后台发布此文章的管理员用户
        obj.author = request.user
        # TODO Call super().save_model() to save the object using Model.save().
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
