from email import message
from venv import create
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from matplotlib.pyplot import cla
from sympy import ordered

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(blank=True, null=True)  # set on first publish
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def _generate_unique_slug(self):
        base = slugify(self.title)[:210] or "post"
        candidate = base
        counter = 1
        # ensure unique (excluding self when updating)
        while Post.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
            candidate = f"{base}-{counter}"
            counter += 1
            # still enforce max length
            candidate = candidate[:220]
        return candidate

    def save(self, *args, **kwargs):
        # slug
        if not self.slug:
            self.slug = self._generate_unique_slug()

        # published_at: set only when moving from draft->published first time
        if self.status == 'published' and self.published_at is None:
            self.published_at = timezone.now()

        # if switching back to draft, keep published_at as-is (history)
        super().save(*args, **kwargs)
        
        
class ContactMessage(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20,blank=True, null=True)
    email=models.EmailField()
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.name} - {self.email}"
