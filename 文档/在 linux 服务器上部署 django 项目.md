# 在linux 服务器上部署 django 项目 

[TOC]

部署架构

```
Python-3.8 + Centos7 + Nginx-1.6.2 + uWSGI-2.0.20 + Django-3.2.7
```

### 1 安装 nginx 

安装编译工具及库文件

```
yum -y install make zlib zlib-devel gcc-c++ libtool  openssl openssl-devel
```

安装 PCRE, 其作用是让 Nginx 支持 Rewrite 功能

下载地址：[https://sourceforge.net/projects/pcre/files/](https://sourceforge.net/projects/pcre/files/)

解压后，进入解压目录下，执行如下命令

使用的版本是 pcre-8.45

```sh
./configure

make && make install
```

查看 pcre 版本

```sh
pcre-config --version
```

下载、安装 nginx

注意: nginx 版本和 openssl 版本的兼容。

地址：[https://nginx.org/en/download.html](https://nginx.org/en/download.html)

解压后，进入解压目录下，执行如下命令

使用的版本是 nginx-1.6.2

```sh
./configure --prefix=/usr/local/webserver/nginx --with-http_stub_status_module --with-http_ssl_module --with-pcre=/opt/modules/pcre-8.45

make

make install
```

查看 nginx 版本

```sh
/usr/local/webserver/nginx/sbin/nginx -v
```

编辑 `/usr/local/webserver/nginx/conf/nginx.conf` 文件，进行配置。在默认配置项下，添加修改如下配置

```sh
user zgg zns;
worker_processes 2; #设置值和CPU核心数一致
listen 80; #监听端口
server_name localhost; #服务器ip地址
```

检查配置文件 `nginx.conf` 的正确性命令

```sh
[root@node module]# /usr/local/webserver/nginx/sbin/nginx -t
nginx: the configuration file /usr/local/webserver/nginx/conf/nginx.conf syntax is ok
nginx: configuration file /usr/local/webserver/nginx/conf/nginx.conf test is successful
```

启动 nginx 

```sh
/usr/local/webserver/nginx/sbin/nginx
```

查看启动情况

```sh
ps -ef | grep nginx
```

在浏览器输入服务器地址，可以看到 `Welcome to nginx!` 字样，即成功。

nginx 常用的几个命令：

```sh
/usr/local/webserver/nginx/sbin/nginx -s reload     # 重新载入配置文件  修改配置文件后一定要执行这条命令
/usr/local/webserver/nginx/sbin/nginx -s reopen     # 重启 Nginx
/usr/local/webserver/nginx/sbin/nginx -s stop       # 停止 Nginx
```

### 2 安装 uWSGI

点击 [https://uwsgi-docs.readthedocs.io/en/latest/Download.html](https://uwsgi-docs.readthedocs.io/en/latest/Download.html) 下载 Stable/LTS 版本的源文件。

解压后，进入解压目录下，执行如下命令

```sh
sudo python3 setup.py install
```

如果你的 django 项目使用的是虚拟环境，那么就使用虚拟环境的 python 解释器安装 uWSGI

如果使用的是在系统安装的解释器，那么就使用系统解释器安装

这里使用的是在系统安装的解释器

如果没有建立软链接，那么运行 uwsgi 就会出现 `[uwsgi: command not found]` 错误

执行如下命令建立软连接：

```sh
ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi
```

### 3 配置 uwsgi

在配置 uwsgi 之前，需要在 django 项目中修改 setting.py 文件的如下几项：

```python
import os
DEBUG = False

ALLOWED_HOSTS = ['192.168.xx.xx']  # 服务器ip

STATIC_ROOT = os.path.join(BASE_DIR, 'collect_static')
```

将所有静态文件都复制到 `STATIC_ROOT` 目录下

```sh
# 1. 在项目根目录下，新建目录 collect_static
# 2. 执行如下命令，迁移静态文件
python3 manage.py collectstatic
```

由于是用 pip3 安装的 django, 如果使用 `python manage.py collectstatic` 迁移静态文件，那么会使用系统自带的 python2.7，就报 `File “manage.py“, line 17 ) from exc ^ SyntaxError: invalid syntax` 错。

然后在 `manage.py` 的目录下，新建一个 `uwsgi.ini` 文件

```ini
[uwsgi]
chdir = /home/zgg/project/YOURPROJECTNAME  # 项目根目录
module = YOURPROJECTNAME.wsgi:application  # 指定wsgi模块，与Nginx连接时用
socket = 192.168.84.57:8000            # 应用服务IP端口
master = true

vacuum = true  #退出、重启时清理文件
pidfile = /var/run/uwsgi9090.pid
daemonize = /home/zgg/project/YOURPROJECTNAME/run.log  #日志文件，一般会自动创建
disable-logging = true   #不记录正常信息，只记录错误信息
```

各配置项的解释见第二个参考链接。

### 4 配置 nginx

修改 `/usr/local/webserver/nginx/conf` 目录下的 `nginx.conf` 文件的以下几项

```conf
user zgg zns;
worker_processes  2;
server {
        listen       80;
        server_name  192.168.xx.xx;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
           include  uwsgi_params;
           uwsgi_pass  192.168.xx.xx:8000;   # 和uWSGI配置中的socket要一样
        }

        location /static {
           alias /home/zgg/project/YOURPROJECTNAME/collect_static;
        }
```

修改完毕，保存退出，然后重启 nginx 服务

```sh
/usr/local/webserver/nginx/sbin/nginx -s reopen
```

### 5 启动服务

在项目根目录，执行如下命令

```sh
sudo uwsgi uwsgi.ini
# 会出现：
# [uWSGI] getting INI configuration from uwsgi.ini
```

然后在浏览器中输入你的服务器 ip 地址，跳转你的页面就成功

常用的 uwsgi 操作命令

```sh
# 启动uwsgi
uwsgi --ini uwsgi.ini

# 关闭uwsgi
uwsgi --stop ./uwsgi.pid

# 重启
uwsgi --reload ./uwsgi.pid

#查看确认是否uwsgi启动
ps -ef|grep uwsgi 

#查看端口是否起来
netstat -anp|grep 9527
```

--------------------------------------

参考：

[https://www.runoob.com/linux/nginx-install-setup.html](https://www.runoob.com/linux/nginx-install-setup.html)

[https://www.cnblogs.com/liudinglong/p/12185180.html#auto-id-5](https://www.cnblogs.com/liudinglong/p/12185180.html#auto-id-5)

[https://www.liujiangblog.com/course/django/181](https://www.liujiangblog.com/course/django/181)