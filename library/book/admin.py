from django.contrib import admin
from book.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_authors', 'count']
    list_filter = ['id', 'name', 'authors']
    search_fields = ['name']
    filter_horizontal = ('authors', )

    readonly_fields = ('name', 'description', 'authors', 'year_of_publication')
    fieldsets = [
        ('Book information', {'fields': ['name', 'description', 'authors', 'year_of_publication']}),
        ('Other information', {'fields': ['count', 'date_of_issue']})
    ]

    def display_authors(self, obj):
        return ', '.join([f"{author.surname} {author.name} {author.patronymic}" for author in obj.authors.all()])

    display_authors.short_description = 'Authors'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Book already exists, fields should be read-only
            return ['name', 'description', 'authors', 'year_of_publication']
        else:  # New book being added, all fields should be editable
            return []





admin.site.register(Book, BookAdmin)
