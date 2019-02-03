import os
import sqlite3
# setting.py の変数値を取得する場合
from django.conf import settings

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# ページネーター
from django.core.paginator import (
    Paginator,  # ページネーター本体のクラス
    EmptyPage,  # ページ番号が範囲外だった場合に発生する例外クラス
    PageNotAnInteger  # ページ番号が数字でなかった場合に発生する例外クラス
)
from django.shortcuts import (
    render,
    redirect,
)
from django.contrib import messages
from .models import Category, Memo

# データベースファイルのサイズ
file_size = 0
# データベースファイルのパス
file_path = ""


def _get_page(list_, page_no, count=20):
    """
    ページネーターを使い、表示するページ情報を取得する
    count=20 は表示件数
    """

    paginator = Paginator(list_, count)
    try:
        page = paginator.page(page_no)
    except (EmptyPage, PageNotAnInteger):
        # page_noが指定されていない場合、数値で無い場合、範囲外の場合は
        # 先頭のページを表示する
        page = paginator.page(1)
    return page


def home_view(request):
    """
    トップページ
    GETパラメータなし　一覧表示
    GETパラメータあり　カテゴリ抽出と文字列検索を振り分け
    """

    # GETリクエストのクエリパラメータを取得
    category_id = 0
    q = ""

    if "category_id" in request.GET:
        category_id = int(request.GET.get("category_id"))

    if "q" in request.GET:
        q = request.GET.get("q")

    # データベースファイルのサイズの取得　SQLite特有のVACUUM
    global file_size, file_path
    file_path = settings.DATABASES['default']['NAME']
    file_size = os.path.getsize(file_path) / 1024

    # ページネーション用
    if category_id > 0:
        page = _get_page(
            Memo.objects.filter(category__id=category_id).order_by('-id'),
            request.GET.get('page')
        )
    elif q:
        page = _get_page(
            # or はQオブジェクトを使う
            Memo.objects.filter(Q(title__contains=q) | Q(
                detail__contains=q)).order_by('-id'),
            request.GET.get('page')
        )
    else:
        page = _get_page(
            Memo.objects.order_by('-id'),
            request.GET.get('page')
        )

    # #テンプレートに渡す辞書
    contexts = {
        'file_size': file_size,
        'page': page,
        'category_id': category_id,
        'q': q,
    }

    # return HttpResponse("test")
    return render(request, 'home.html', contexts)


def detail_view(request, id):
    """
    詳細ページ
    idで振り分け
    """
    # オブジェクトが存在しない場合には Http404 を送出
    p = get_object_or_404(Memo, pk=id)

    # #テンプレートに渡す辞書
    contexts = {
        'p': p
    }

    return render(request, 'detail.html', contexts)


def vacuum_view(request):
    """
    生のSQLを発行
    SQLiteの空き領域開放
    """
    # もしファイルがなければエラー
    if not os.path.isfile(file_path):
        print("ファイルがありません")
        return

    # あれば
    conn = sqlite3.connect(file_path)
    # Cursor オブジェクトを作り
    cursor = conn.cursor()
    # その execute() メソッドを呼んで SQL コマンドを実行することができます

    try:
        cursor.execute("""VACUUM;""")
        conn.commit()
    except:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    # トップページにリダイレクト
    return redirect("home")
