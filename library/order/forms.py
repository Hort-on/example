from django import forms
from order.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'plated_end_at']

    def post(self, request):
        if request.user.is_authenticated:
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                return redirect('/orders/')
            else:
                return render(request, 'order_form.html', {'form': form})
        else:
            return redirect('/login/')



