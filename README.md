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
(djangoenv) C:\Users\xxx\Desktop\PythonNotes>where python  
C:\Users\xxx\Desktop\PythonNotes\djangoenv\Scripts\python.exe  
C:\Users\xxx\Anaconda3\python.exe

最初はpipをアップデートする  
python -m pip install --upgrade pip

Django インストール  
pip install django

バージョン確認  
python -m django --version  
2.1.5

現在 pip にあるものを確認してみる  
(djangoenv) C:\Users\xxx\Desktop\PythonNotes>pip list

    Package    Version
    ---------- -------
    Django     2.1.5
    pip        19.0.1
    pytz       2018.9
    setuptools 39.0.1

## Django 初期設定

