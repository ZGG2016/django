from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        # TODO 表明这个表单对应的数据库模型是 Comment 类
        model = Comment
        # TODO 表单需要显示的字段
        fields = ['name', 'email', 'url', 'text']
