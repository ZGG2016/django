from haystack import indexes
from .models import Post


# TODO 要相对某个 app 下的数据进行全文检索，就要在该 app 下创建一个 search_indexes.py 文件
#  然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Post），并且继承 SearchIndex 和 Indexable
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    # TODO 每个索引里面必须有且只能有一个字段为 document = True，
    #  这代表 django haystack 和搜索引擎将使用此字段的内容作为索引进行检索(primary field)。
    #  注意，如果使用一个字段设置了document = True，则一般约定此字段名为text
    #  use_template=True允许我们使用数据模板去建立搜索引擎索引的文件
    #   数据模板就是templates/search/indexes/blog/post_text.txt，作用是对 Post.title、Post.body 这两个字段建立索引
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
