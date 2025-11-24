from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Blog
from .tasks import create_random_blog_post
import subprocess
from datetime import datetime, timedelta

# Register your models here.

admin.site.register(Blog)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate/', self.generate_articles_view, name='generate_articles'),
            path('scheduled/', self.scheduled_tasks_view, name='scheduled_tasks'),
        ]
        return custom_urls + urls
    
    def generate_articles_view(self, request):
        if request.method == 'POST':
            count = int(request.POST.get('count', 1))
            interval = int(request.POST.get('interval', 10))
            for i in range(count):
                eta = datetime.now() + timedelta(seconds=i*interval)
                create_random_blog_post.apply_async(eta=eta)
            messages.success(request, f'{count} article(s) en cours de génération (intervalle: {interval}s, durée: {(count-1)*interval}s).')
            return redirect('..')
        return render(request, 'admin/generate_articles.html', {'title': 'Générer des articles'})
    
    def scheduled_tasks_view(self, request):
        try:
            # Run celery inspect scheduled
            result = subprocess.run(['celery', '-A', 'myproject', 'inspect', 'scheduled'], capture_output=True, text=True, timeout=10)
            scheduled_output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            scheduled_output = f"Erreur: {str(e)}"
        
        try:
            # Run celery inspect active
            result = subprocess.run(['celery', '-A', 'myproject', 'inspect', 'active'], capture_output=True, text=True, timeout=10)
            active_output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            active_output = f"Erreur: {str(e)}"
        
        context = {
            'title': 'Tâches Celery',
            'scheduled': scheduled_output,
            'active': active_output,
        }
        return render(request, 'admin/scheduled_tasks.html', context)

# Unregister and register with custom admin
admin.site.unregister(Blog)
admin.site.register(Blog, BlogAdmin)
