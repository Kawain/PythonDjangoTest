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

