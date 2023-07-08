from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, BookForm
from .models import *

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Registration successful. Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'books/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'books/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def book_list(request):
    books = Book.objects.filter(author=request.user)
    return render(request, 'books/book_list.html', {'books': books})

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

@login_required
def book_update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form})

@login_required
def book_delete(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect('book_list')
