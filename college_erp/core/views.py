# college_erp/core/views.py
from django.shortcuts import render, redirect
from datetime import datetime
from .models import User, Book, BookIssue  # ensure these models exist in core/models.py
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
            return redirect('core:login')  # namespaced redirect (see note)
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
            # Use namespaced names if you included core urls with namespace='core'
            if user.role == 'student':
                return redirect('core:student_dashboard')
            elif user.role == 'teacher':
                return redirect('core:teacher_dashboard')
            elif user.role == 'admin':
                return redirect('core:admin_dashboard')
            elif user.role == 'clerk':
                return redirect('core:clerk_dashboard')
            elif user.role == 'librarian':
                return redirect('core:librarian_dashboard')
            else:
                return redirect('core:home')  # fallback

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def library(request):
    return render(request, 'library.html')

def logout_view(request):
    auth_logout(request)
    return redirect('core:home')

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

# ----------------------------
# Library related views below
# ----------------------------

# Student issued books view — ensure BookIssue model exists
@login_required
def student_issued_books(request):
    try:
        books = BookIssue.objects.filter(student=request.user)
    except Exception:
        # If BookIssue model is missing or query fails, return empty list and a message
        messages.error(request, "BookIssue model not found or query failed.")
        books = []
    return render(request, 'student_issued_books.html', {'books': books})

# All book issue history (admin/librarian)
@login_required
def all_book_issue_history(request):
    try:
        issues = BookIssue.objects.all()
    except Exception:
        messages.error(request, "BookIssue model not found or query failed.")
        issues = []
    return render(request, 'all_book_issue_history.html', {'issues': issues})

# ----------------------------
# Missing view stubs that caused your server to crash
# ----------------------------

@login_required
def add_book(request):
    """
    Simple add-book view stub.
    - If you have a Book model form, you can replace this with real create logic.
    """
    if request.method == "POST":
        # minimal create logic (adjust according to your Book model fields)
        title = request.POST.get('title')
        author = request.POST.get('author')
        if title:
            try:
                Book.objects.create(title=title, author=author or "")
                messages.success(request, "Book added.")
                return redirect('core:library')
            except Exception as e:
                messages.error(request, f"Could not create book: {e}")
        else:
            messages.error(request, "Title is required.")
    # Render a simple template (create core/templates/add_book.html) or redirect if template missing
    try:
        return render(request, 'add_book.html')
    except Exception:
        return redirect('core:library')

@login_required
def manage_issues(request):
    """
    Manage issues stub — list all issues and optionally mark returned.
    """
    try:
        issues = BookIssue.objects.all()
    except Exception:
        issues = []
    # Render a manage issues template (create core/templates/manage_issues.html)
    try:
        return render(request, 'manage_issues.html', {'issues': issues})
    except Exception:
        return redirect('core:library')
