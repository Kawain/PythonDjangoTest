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
