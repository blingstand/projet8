# from django.contrib import admin
# from .models import Profile

# # Register your models here.

# class ProfileInline(admin.TabularInline):
# 	model = Profile

# class ProfileAdmin(admin.ModelAdmin):
#     inlines = [ProfileInline]
#     list_display = ('username', 'password', 'timestamp')
#     list_filter = ['timestamp']
#     search_fields = ['username']

# admin.site.register(Profile)