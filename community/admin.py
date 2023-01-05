from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    """"""
    pass

@admin.register(models.FreeBoard)
class FreeBoardAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BoardPhoto)
class BoardPhotoAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BoardComment)
class BoardCommentAdmin(admin.ModelAdmin):

    """ """

    pass

@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):

    """ """

    pass