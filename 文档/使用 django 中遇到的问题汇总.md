# 使用 django 中遇到的问题汇总

[TOC]

### 问题1

在 django 项目中，使用服务器 IP 地址打开，出现 `Invalid HTTP_HOST header: 'xxx.xx.xxx.xxx:8000'. You may need to add 'xxx.xx' to ALLOWED_HOSTS！`，需要修改创建项目时生成的 setting.py 文件，将 `ALLOWED_HOSTS = []` 改为 `ALLOWED_HOSTS = ['*']` ，再次运行即可成功访问，这表示所有 ip 都能访问。也可以指定一个 ip.

### 问题2

如果在 url.py 中，将 urlpatterns 写成了如下形式，会报错：`TYPEERROR: 'SET' OBJECT IS NOT REVERSIBLE`

```python
urlpatterns = {
    path('admin/', admin.site.urls),
}
```

这里应该是列表，即：

```python
urlpatterns = [
    path('admin/', admin.site.urls),
]
```

### 问题3

如果输入完 ip 地址，打开项目，出现 `Internal Server Error` 错误，说明是你的业务代码出现了问题。