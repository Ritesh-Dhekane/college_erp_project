from django.shortcuts import render, redirect
from datetime import datetime
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html', {'year': datetime.now().year})

def register(request):
    if request.method == "POST":
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'student')

        # Validate required fields
        if not all([first_name, last_name, email, password, role]):
            messages.error(request, "All fields are required!")
            return render(request, 'register.html')

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, 'register.html')

        # Create the user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            messages.success(request, "User registered successfully!")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return render(request, 'register.html')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate by username (we used email as username)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)  # log the user in

            # Redirect based on role
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'clerk':
                return redirect('clerk_dashboard')
            elif user.role == 'librarian':
                return redirect('librarian_dashboard')
            else:
                return redirect('home')  # fallback

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def library(request):
    return render(request, 'library.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html', {'year': datetime.now().year})

@login_required
def student_dashboard(request):
    return render(request, 'dashboard/student.html', {'user': request.user})

@login_required
def teacher_dashboard(request):
    return render(request, 'dashboard/teacher.html', {'user': request.user})

@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html', {'user': request.user})

@login_required
def clerk_dashboard(request):
    return render(request, 'dashboard/clerk.html', {'user': request.user})

@login_required
def librarian_dashboard(request):
    return render(request, 'dashboard/librarian.html', {'user': request.user})


def student_issued_books(request):
    books = BookIssue.objects.filter(student=request.user)
    return render(request, 'student_issued_books.html', {'books': books})

def all_book_issue_history(request):
    issues = BookIssue.objects.all()
    return render(request, 'all_book_issue_history.html', {'issues': issues})