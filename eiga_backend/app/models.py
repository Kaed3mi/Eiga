from django.db import models

text_len = 8000


# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=32, verbose_name='id', primary_key=True)
    user_name = models.CharField(max_length=32, verbose_name='用户名')
    email = models.CharField(max_length=32, verbose_name='邮箱')
    password = models.CharField(max_length=32, verbose_name='密码')
    permission = models.CharField(max_length=32, verbose_name='权限', null=True, blank=True)
    avatar = models.CharField(max_length=60, verbose_name='头像', null=True, blank=True, default="default")
    class Meta:
        db_table = 'tb_user'
        verbose_name = '学生'

    def __str__(self):
        return self.user_id


class Bangumi(models.Model):
    bangumi_id = models.CharField(max_length=32, verbose_name='id', primary_key=True)
    bangumi_name = models.CharField(max_length=32, verbose_name='番组名')
    bangumi_intro = models.CharField(max_length=text_len, verbose_name='简介')
    bangumi_score = models.FloatField(verbose_name='评分', null=True, blank=True)
    rank = models.IntegerField(verbose_name='排名', null=True, blank=True)

    class Meta:
        db_table = 'tb_bangumi'
        verbose_name = '番组'

    def __str__(self):
        return self.bangumi_id

# TODO 考虑给这里加一个触发器，每次进行修改(insert,update,delete)的时候重置排名
class Score(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bangumi_id = models.ForeignKey(Bangumi, on_delete=models.CASCADE)
    score = models.FloatField(verbose_name='评分')

    class Meta:
        db_table = 'tb_score'
        verbose_name = '评分'
        unique_together = (("user_id", "bangumi_id"),)

    def __str__(self):
        return f'{self.bangumi_id}{self.user_id}{self.score}'


class Blog(models.Model):
    blog_id = models.CharField(max_length=32, verbose_name='id', primary_key=True)
    blog_title = models.CharField(max_length=32, verbose_name='标题')
    content = models.CharField(max_length=text_len, verbose_name='内容')
    time = models.DateTimeField(verbose_name='时间')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default="default")

    class Meta:
        db_table = 'tb_blog'
        verbose_name = '日志'

    def __str__(self):
        return self.blog_id


class BlogBangumi(models.Model):
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    bangumi_id = models.ForeignKey(Bangumi, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_blogbangumi'
        verbose_name = '番组-日志'

    def __str__(self):
        return f'{self.blog_id}{self.bangumi_id}'


class Character(models.Model):
    character_id = models.CharField(max_length=32, verbose_name='id', primary_key=True)
    character_name = models.CharField(max_length=32, verbose_name='角色名')
    intro = models.CharField(max_length=text_len, verbose_name='简介')
    image = models.CharField(max_length=32, verbose_name='图片')

    class Meta:
        db_table = 'tb_character'
        verbose_name = '角色'

    def __str__(self):
        return self.character_id


class Comment(models.Model):
    comment_id = models.CharField(max_length=32, verbose_name='id', primary_key=True)
    content = models.CharField(max_length=text_len, verbose_name='内容')
    time = models.DateTimeField(verbose_name='时间')
    bangumi_id = models.ForeignKey(Bangumi, on_delete=models.SET_NULL, null=True, blank=True)
    blog_id = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True, blank=True)
    character_id = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'tb_comment'
        verbose_name = '评论'

    def __str__(self):
        return self.comment_id


class BangumiRelationship(models.Model):
    a_id = models.ForeignKey(Bangumi, on_delete=models.CASCADE, related_name='a_relationships')
    b_id = models.ForeignKey(Bangumi, on_delete=models.CASCADE, related_name='b_relationships')
    relation = models.CharField(max_length=32, verbose_name='关系')

    class Meta:
        db_table = 'tb_bangumibangumi'
        verbose_name = '番组关系'
        unique_together = (("a_id", "b_id"),)

    def __str__(self):
        return f'{self.a_id}{self.b_id}'


class CharacterBangumi(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    bangumi_id = models.ForeignKey(Bangumi, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_characterbangumi'
        verbose_name = '角色-番组'

    def __str__(self):
        return f'{self.character_id}{self.bangumi_id}'
