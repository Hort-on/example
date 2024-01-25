from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from book.models import Book
from django.views.generic import DetailView
from book.forms import BookAddForms, BookSearchForms


@login_required
def books_page(request):
    book = Book.objects.all()
    if request.method == 'POST':
        form = BookSearchForms(request.POST)
        if form.is_valid():
            select_fields = form.cleaned_data['select_fields']
            search_fields = form.cleaned_data['search_fields']
            if select_fields == '0':
                book = Book.objects.filter(authors__surname__icontains=search_fields).values()
            elif select_fields == '1':
                book = Book.objects.filter(name__icontains=search_fields).values()
            return render(request, template_name='book/book.html',
                          context={'books': book,
                                   'parameter': BookSearchForms.choice[int(select_fields)][1],
                                   'value': search_fields,
                                   'form': form})
        else:
            return render(request, template_name='book/book.html',
                          context={'books': book,
                                   'form': form})
    else:
        form = BookSearchForms()
        return render(request, template_name='book/book.html',
                      context={'books': book,
                               'form': form})


@method_decorator(login_required, name='dispatch')
class BookDetails(DetailView):
    model = Book
    template_name = 'book/book_details.html'


@login_required
def add_book_view(request):
    if request.method == 'POST':
        form = BookAddForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book:book')
        else:
            return render(request, template_name='book/add_book.html',
                          context={'form': form})
    else:
        form = BookAddForms()
        return render(request, template_name='book/add_book.html',
                      context={'form': form})


@login_required
def remove_book(request, book_id):
    if request.method == 'POST':
        book_to_remove = Book.get_by_id(book_id)
        book_to_remove.delete()
        return redirect('book:book')
