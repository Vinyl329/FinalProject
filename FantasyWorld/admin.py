from django.contrib import admin
from .models import Category, Subclass, Response
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class SubclassAdminForm(forms.ModelForm):
    text_subclass = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Subclass
        fields = '__all__'


class SubclassAdmin(admin.ModelAdmin):
    form = SubclassAdminForm


admin.site.register(Subclass, SubclassAdmin)
admin.site.register(Response)
admin.site.register(Category)