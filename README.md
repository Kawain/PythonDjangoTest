# PythonDjangoTest

Windows 10

仮想環境に Django をインストール  
例えば djangoenv という名前の仮想環境を作成するには、目的のフォルダに移動して次のコマンドを実行  
python -m venv djangoenv

仮想環境を有効化するには  
djangoenv\Scripts\activate

環境を抜けるには  
deactivate

確認のために仮想環境に入り where python してみる  
(djangoenv) C:\Users\User名\Desktop\PythonNotes>where python  
C:\Users\User名\Desktop\PythonNotes\djangoenv\Scripts\python.exe  
C:\Users\User名\Anaconda3\python.exe

最初はpipをアップデートする  
python -m pip install --upgrade pip

Django インストール  
pip install django

バージョン確認  
python -m django --version  
2.1.5

現在 pip にあるものを確認してみる  
(djangoenv) C:\Users\User名\Desktop\PythonNotes>pip list

    Package    Version
    ---------- -------
    Django     2.1.5
    pip        19.0.1
    pytz       2018.9
    setuptools 39.0.1

## Django 初期設定

プロジェクトを作成する  
django-admin startproject PythonDjangoTest

ここまでのフォルダ構成  

    PythonDjangoTest
    │  manage.py
    │
    └─PythonDjangoTest
            settings.py
            urls.py
            wsgi.py
            __init__.py

Visual Studio Code のパスが通っていれば以下で起動する  
(djangoenv) C:\Users\User名\Desktop\PythonNotes\PythonDjangoTest>code .

settings.py の日本語と時間を変更  
LANGUAGE_CODE = 'ja'  
TIME_ZONE = 'Asia/Tokyo'  

初期のデータベースは sqlite だが、そのまま使用  

開発用サーバー起動  
python manage.py runserver  

http://127.0.0.1:8000/  
インストールは成功しました！おめでとうございます！  

Visual Studio Code で何度もフォーマット（Shift + Alt + F）するので autopep8 を入れておく  
pip install autopep8

## アプリケーションの作成

memo という名のアプリケーションを作成  
python manage.py startapp memo  

現在のフォルダ構成（pycacheは省略）  

    PythonDjangoTest
    │  db.sqlite3（これは後に削除する）
    │  manage.py
    │
    ├─memo
    │  │  admin.py
    │  │  apps.py
    │  │  models.py
    │  │  tests.py
    │  │  views.py
    │  │  __init__.py
    │  │
    │  └─migrations
    │          __init__.py
    │
    └─PythonDjangoTest
        │  settings.py
        │  urls.py
        │  wsgi.py
        │  __init__.py
        │
        └─__pycache__


### 既存データベースを紐付ける方法

デフォルトの db.sqlite3 を削除して、既存のデータベースを使いたい場合  
例えば以下のようなテーブルがあり、何百レコードも入っているとする  

    CREATE TABLE `category` (
    	`id`	integer,
    	`name`	text,
    	PRIMARY KEY(`id`)
    );
    
    CREATE TABLE `memo` (
    	`id`	integer,
    	`category_id`	integer,
    	`title`	text,
    	`detail`	text,
    	PRIMARY KEY(`id`)
    );

このデータを使いたい…  

### settings.pyファイルのDATABASESを変更

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'notes3.db'),#ファイル名を変更
        }
    }

このコマンドで一度確認  
python manage.py dbshell

(djangoenv) C:\Users\User名\Desktop\PythonNotes\PythonDjangoTest>python manage.py dbshell  
SQLite version 3.23.1 2018-04-10 17:39:29  
Enter ".help" for usage hints.  
sqlite> .table  
category  memo  
  
テーブルがあるのがわかった  

このコマンドでモデル定義の構造がわかる  
python manage.py inspectdb   

    class Category(models.Model):
        id = models.IntegerField(blank=True, null=True)
        name = models.TextField(blank=True, null=True)
    
        class Meta:
            managed = False
            db_table = 'category'
    
    class Memo(models.Model):
        id = models.IntegerField(blank=True, null=True)
        category_id = models.IntegerField(blank=True, null=True)
        title = models.TextField(blank=True, null=True)
        detail = models.TextField(blank=True, null=True)
    
        class Meta:
            managed = False
            db_table = 'memo'
		

### memo\models.py で多少変更したモデルを作成

PRIMARY KEYとなるクラス変数を定義しない場合、idが自動的に定義される  
また、外部キー制約を追加したモデルにします  

```
from django.db import models


class Category(models.Model):
    """カテゴリ"""

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'category'


class Memo(models.Model):
    """内容"""

    # 外部キー制約
    # models.CASCADE - 一緒に削除される
    # models.PROTECT - 参照されてたら、削除ができない
    # models.SET_NULL - NULLをセットする
    # カラム名はcategory_idだが、ForeignKey設定したら自動で_idが付くのでcategoryだけにした
    category = models.ForeignKey(
        'Category',
        verbose_name="id",
        on_delete=models.PROTECT
    )
    title = models.CharField(max_length=255)
    detail = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'memo'

```
	
### settings.pyファイルにアプリケーションを追加

INSTALLED_APPS に追加  
'memo.apps.MemoConfig'  
または  
'memo'  

### データベースに反映させる

モデル変更のためのマイグレーション   
python manage.py makemigrations memo   

データベースにこれらの変更を適用するためにマイグレート実行   
ここではmemoアプリケーションのテーブルは変更されない   
python manage.py migrate

### admin.pyファイルにモデルを追加
```
from django.contrib import admin

from .models import Category
from .models import Memo

admin.site.register(Category)
admin.site.register(Memo)
```

スーパーユーザーがいないので登録  
python manage.py createsuperuser

### 開発用サーバー起動
python manage.py runserver  
  
http://127.0.0.1:8000/admin   
スーパーユーザーでログインして  
Category  
Memo  
が増えていることを確認  

その他は Python Django の情報を検索すればOK

