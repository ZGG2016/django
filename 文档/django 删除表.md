# django 删除表

1. 在数据库里删表 drop table 
  
2. 删掉 model.py 里对应的表

3. 执行以下命令

		python manage.py makemigrations
	
		python manage.py migrate --fake