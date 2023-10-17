from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        total_post_rating = self.author(models.Sum('rating'))['rating__sum'] or 0
        total_comment_rating = self.user_comments.aggregate(models.Sum('rating'))['rating__sum'] or 0
        self.rating = total_post_rating * 3 + total_comment_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(unique=True)


class Post(models.Model):
    post_or_new = [
        ('post', 'Post'),
        ('new', 'New')
    ]
    choice = models.CharField(max_length='4', choices=post_or_new, default=None)
    time_in = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ManyToManyField(Category, through='PostCategory')
    post_new_header = models.CharField(max_length='256')
    post_new_text = models.TextField()
    rate = models.IntegerField(default=0)

    def preview(self):
        return self.post_new_text[:124] + '...'

    def like(self):
        self.rate += 1
        self.save()
        self.author.update_rating()

    def dislike(self):
        self.rate -= 1
        self.save()
        self.author.update_rating()

    def __str__(self):
        return self.post_new_header


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_category')
    category_rel = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    posted_time = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()

    def __str__(self):
        return self.comment_text
