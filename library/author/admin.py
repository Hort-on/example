from django.contrib import admin
from author.models import Author
from book.models import Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    search_fields = ['surname', 'name']
    ordering = ['surname']
    readonly_fields = ('author_books', 'full_name')

    fieldsets =[
        ('Author', {'fields': ['surname', 'name', 'patronymic']}),
        ('Books', {'fields': ['author_books']}),
    ]

    def author_books(self, obj):
        return '\n '.join([f"{book}" for book in Book.objects.filter(authors=obj.id)])

    def full_name(self, obj):
        return f"{obj.surname} {obj.name} {obj.patronymic}"



admin.site.register(Author, AuthorAdmin)
