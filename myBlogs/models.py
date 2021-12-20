from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Post(models.Model):

    # author is connected with the superuser from the website
    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """ published_date var from Post will log the curent time when
        called through publish fun for Post & comments """
        self.published_date = timezone.now()
        self.save()

    # RENAME TO ATTACH COMMENT LATER
    def approve_comment(self):
        """ This fun is connected with fun approve inside the Comment class
        below & attach the comment to the POST once approved """
        self.comment.filter(approved_comment=True)

    def get_absolute_url(self):
        """ built-in fun will return the page to post_detail once the post
        has been posted """
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    # post is the ForeignKey of the POST class
    post = models.ForeignKey(
        'myBlogs.Post', related_name='comment', on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=200, null=True)
    text = models.TextField(null=True)
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    # RENAME TO APPROVE COMMENT OR SUBMIT COMMENT LATER
    def approve(self):
        """ This fun will approve the comment & relates with the
        approve_comment fun inside the Post class """
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.text
