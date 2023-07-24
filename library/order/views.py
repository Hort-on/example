from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from order.models import Order
from book.models import Book
from authentication.models import CustomUser
from datetime import datetime
from .forms import OrderForm


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('/orders/')
        else:
            return render(request, 'add_order.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'add_order.html', {'form': form})


@login_required
def order_view(request):
    # if user want to add new order:
    if request.method == 'POST' and request.user.role == 0:
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order:order_view')
        else:
            context = {'all_orders': Order.objects.exclude(end_at__isnull=False).filter(user=request.user.id),
                       'all_books': Book.get_all(),
                       'form': form}
            return render(request, template_name='order/order_list.html',
                          context=context)

    elif request.method == 'GET':
        form = OrderForm()

        # Show the admin all open order
        if request.user.role == 1:
            users = CustomUser.objects.all()
            context = {'all_orders': Order.objects.exclude(end_at__isnull=False).order_by('plated_end_at'),
                       'users': users,
                       'form': form}
            return render(request, template_name='order/order_list.html',
                          context=context)

        # Show the user his unclosed orders
        else:
            available_books = []
            for book in Book.objects.all():
                # count the number of each book in open order (end_at=None)
                book_in_order = Order.objects.filter(end_at=None).filter(book__name=book.name).count()
                # if count of book more than current book in order than add this book to available list
                if book.count > book_in_order:
                    available_books.append(book)

            context = {'all_orders': Order.objects.exclude(end_at__isnull=False).filter(user=request.user.id),
                       'all_books': available_books,
                       'form': form}
            return render(request, template_name='order/order_list.html',
                          context=context)


def close_order(request):
    if request.method == 'POST':
        select_list = request.POST.get('close_order')
        order_to_close = Order.get_by_id(select_list)
        order_to_close.end_at = datetime.now()
        order_to_close.save()
        return redirect('order:order_view')


def show_books_for_user(request):
    user_id = request.GET['user_id']
    email = CustomUser.get_by_id(user_id).email
    orders = Order.objects.filter(user__id=user_id).exclude(end_at__isnull=False)
    return render(request, template_name='order/users_order.html',
                  context={'orders': orders,
                           'email': email})
