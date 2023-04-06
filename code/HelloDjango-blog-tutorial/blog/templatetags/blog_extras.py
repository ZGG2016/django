from django import template
from django.db.models.aggregates import Count

from ..models import Post, Category, Tag

register = template.Library()


# TODO takes_context 设置为 True 时将告诉 django，在渲染 _recent_posts.html 模板时，
#  不仅传入show_recent_posts 返回的模板变量，同时会传入父模板（即使用 {% show_recent_posts %} 模板标签的模板）上下文
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):  # TODO 显示5篇文章
    # TODO 返回的字典中的值将作为模板变量，传入由 inclusion_tag 装饰器第一个参数指定的模板
    return {
        'recent_post_list': Post.objects.all()[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        # TODO 一个是 created_time ，即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }
