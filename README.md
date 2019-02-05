# PythonDjangoTest
## Windows 10 で確認
## Django 大まかな流れ
### 仮想環境準備
例えば djangoenv という名前の仮想環境を作成するには、目的のフォルダに移動して次のコマンドを実行  
python -m venv djangoenv

仮想環境を有効化するには  
djangoenv\Scripts\activate

環境を抜けるには  
deactivate

最初はpipをアップデートする  
python -m pip install --upgrade pip

### Django インストール
pip install django

バージョン確認  
python -m django --version  
2.1.5

## プロジェクト作成
任意のフォルダ内で  
django-admin startproject プロジェクト名

startproject で指定された名称で作成されますが、適当な名称へ変更可能

cd プロジェクト名/

プロジェクト名フォルダ内に移動（ manage.py と同階層に移動）  
この後は　`python manage.py *******`　というコマンドをたくさん使うことになる

## アプリケーション作成
python manage.py startapp アプリ名

### settings.py 変更箇所
```
LANGUAGE_CODE = 'ja-JP'

TIME_ZONE = 'Asia/Tokyo'
```

templates をアプリ外に置く場合  
os.path.join(BASE_DIR, "templates")

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
```
static をアプリ外に置く場合
```
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
```

## メイクマイグレーションズとマイグレート
メイクマイグレーションズ
python manage.py makemigrations

マイグレート  
python manage.py migrate

**makemigrations と migrate は何度も使うコマンド**

### スーパーユーザー作成
python manage.py createsuperuser

### 開発用サーバー起動
python manage.py runserver

http://127.0.0.1:8000/  
インストールは成功しました！おめでとうございます！

http://127.0.0.1:8000/admin  
先程作成したスーパーユーザーでログインしてみる

### 既存データベースを紐付ける方法
デフォルトの db.sqlite3 を削除して、既存のデータベースを使いたい場合  
例えば以下のようなテーブルがあり、そのデータを使いたい場合
```
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
```
### settings.pyファイルのDATABASESを変更
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'notes3.db'),#ファイル名を変更
    }
}
```
このコマンドで一度確認  
python manage.py dbshell

```
(djangoenv) C:\Users\User名\Desktop\PythonNotes\PythonDjangoTest>python manage.py dbshell  
SQLite version 3.23.1 2018-04-10 17:39:29  
Enter ".help" for usage hints.  
sqlite> .table  
category  memo  
```
テーブルがあるのがわかった  

このコマンドでモデル定義の構造がわかる  
python manage.py inspectdb   

```
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
```
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
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
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
python manage.py makemigrations memo

ここではmemoアプリケーションのテーブルは変更されない  
python manage.py migrate

### admin.pyファイルにモデルを追加
```
from django.contrib import admin

from .models import Category, Memo

admin.site.register(Category)
admin.site.register(Memo)
```

### スーパーユーザーが消えたので再登録  
python manage.py createsuperuser

### 開発用サーバー起動
python manage.py runserver  
  
http://127.0.0.1:8000/admin   
スーパーユーザーでログインして  
Category  
Memo  
が増えていることを確認  
