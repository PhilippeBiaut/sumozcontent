from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Blog
from .tasks import create_random_blog_post
from django_celery_results.models import TaskResult

# Register your models here.

admin.site.register(Blog)
admin.site.register(TaskResult)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate/', self.generate_articles_view, name='generate_articles'),
        ]
        return custom_urls + urls
    
    def generate_articles_view(self, request):
        if request.method == 'POST':
            count = int(request.POST.get('count', 1))
            interval = int(request.POST.get('interval', 10))
            for i in range(count):
                create_random_blog_post.apply_async(countdown=i*interval)
            messages.success(request, f'{count} article(s) en cours de génération (intervalle: {interval}s, durée: {(count-1)*interval}s).')
            return redirect('..')
        return render(request, 'admin/generate_articles.html', {'title': 'Générer des articles'})

# Unregister and register with custom admin
admin.site.unregister(Blog)
admin.site.register(Blog, BlogAdmin)
