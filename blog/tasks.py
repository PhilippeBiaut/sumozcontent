from celery import shared_task
from .models import Blog
import random
import string

@shared_task
def create_random_blog_post():
    # Generate random title and description
    title = 'Article ' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    description = 'Description automatique pour ' + title + '. ' + ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=100))
    
    # Create the blog post
    Blog.objects.create(title=title, description=description)
    return f'Created blog post: {title}'
