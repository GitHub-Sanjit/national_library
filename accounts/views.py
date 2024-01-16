from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import UserRegistrationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from book.models import BorrowBook
from book.models import WishListBook

# Create your views here.


class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        print("token  ", token)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print("uid  ", uid)
        confirm_link = f"http://127.0.0.1:8000/books/active/{uid}/{token}"
        email_subject = "Confirm Your Email"
        email_body = render_to_string(
            "accounts/confirm_email.html", {"confirm_link": confirm_link})
        email = EmailMultiAlternatives(email_subject, "", to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        messages.success(
            self.request, 'Please Check Your Mail To Confirm.')
        return redirect('register')
        # login(self.request, user)
        # messages.success(
        #     self.request, "After registration , autoLogin successfully done")
        return super().form_valid(form)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'

    def get_success_url(self):
        messages.success(self.request, "Login successfully")
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    http_method_names = ['post']

    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'accounts/profile.html'
    balance = 0

    def get(self, request):
        user_purchases = BorrowBook.objects.filter(user=request.user)
        user_wishlist = WishListBook.objects.filter(user=request.user)
        print(user_wishlist)
        account_balance = request.user.account.balance

        form = UserUpdateForm(instance=request.user)
        print(request.user)
        return render(request, self.template_name, {
            'user_purchases': user_purchases,
            'user_wishlist': user_wishlist,
            'account_balance': account_balance,
            'form': form,
        })

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
