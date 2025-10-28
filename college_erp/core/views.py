# college_erp/core/views.py
from django.shortcuts import render, redirect
from datetime import datetime
from .models import User, Book, BookIssue  # ensure these models exist in core/models.py
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import models # Added missing import for models


def role_required(required_role: str):
    """Decorator to restrict a view to users with a specific role."""
    def decorator(view_func):
        @login_required
        def _wrapped(request, *args, **kwargs):
            if getattr(request.user, "role", None) != required_role:
                messages.error(request, "You do not have permission to access this page.")
                return redirect("core:home")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def home(request):
    # If already authenticated, redirect to relevant dashboard
    if request.user.is_authenticated:
        role = getattr(request.user, 'role', None)
        if role == 'student':
            return redirect('core:student_dashboard')
        if role == 'teacher':
            return redirect('core:teacher_dashboard')
        if role == 'admin':
            return redirect('core:admin_dashboard')
        if role == 'clerk':
            return redirect('core:clerk_dashboard')
        if role == 'librarian':
            return redirect('core:librarian_dashboard')
        return redirect('core:home')
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

@role_required('librarian')
def librarian_dashboard(request):
    # Compute quick stats
    try:
        total_books = Book.objects.count()
    except Exception:
        total_books = 0

    try:
        issued_books = BookIssue.objects.filter(action='issued').count()
    except Exception:
        issued_books = 0

    try:
        students_count = User.objects.filter(role='student').count()
    except Exception:
        students_count = 0

    # Recent transactions (map issued_at to 'date' key for template)
    try:
        recent = (
            BookIssue.objects.select_related('book', 'student')
            .order_by('-issued_at')[:10]
        )
        transactions = [
            {
                'book': bi.book,
                'student': bi.student,
                'action': bi.action,
                'date': bi.issued_at,
            }
            for bi in recent
        ]
    except Exception:
        transactions = []

    context = {
        'user': request.user,
        'total_books': total_books,
        'issued_books': issued_books,
        'students_count': students_count,
        'transactions': transactions,
    }
    return render(request, 'dashboard/librarian.html', context)

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

@role_required('librarian')
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
                copies_total_str = request.POST.get('copies_total')
                try:
                    copies_total = int(copies_total_str) if copies_total_str else 1
                    if copies_total < 1:
                        copies_total = 1
                except ValueError:
                    copies_total = 1

                book = Book.objects.create(
                    title=title,
                    author=author or "",
                    copies_total=copies_total,
                    copies_available=copies_total,
                )
                messages.success(request, f"Book '{book.title}' added successfully.")
                return redirect('core:add-book')
            except Exception as e:
                messages.error(request, f"Could not create book: {e}")
        else:
            messages.error(request, "Title is required.")
    # Render a simple template (create core/templates/add_book.html) or redirect if template missing
    try:
        books = Book.objects.all().order_by('title')
        return render(request, 'add_book.html', { 'books': books })
    except Exception:
        return redirect('core:librarian_dashboard')

@role_required('librarian')
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
        return redirect('core:librarian_dashboard')

@role_required('librarian')
def available_books(request):
    """List all books with copies info and issued counts."""
    try:
        # Efficiently prefetch related issues for counting
        books = list(Book.objects.all())
        # Build a map of book_id to issued count
        issued_counts_qs = (
            BookIssue.objects.filter(action='issued')
            .values('book')
            .order_by()
            .annotate(count=models.Count('id'))
        )
        book_id_to_issued = {row['book']: row['count'] for row in issued_counts_qs}

        rows = []
        for book in books:
            issued_count = book_id_to_issued.get(book.id, 0)
            rows.append({
                'book': book,
                'copies_total': book.copies_total,
                'copies_available': book.copies_available,
                'copies_issued': issued_count,
            })
    except Exception:
        rows = []
    return render(request, 'available_books.html', { 'rows': rows })


@role_required('librarian')
def issue_book(request, book_id):
    """Issue a book to a student."""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Book not found.")
        return redirect('core:books_list')
    
    if request.method == "POST":
        student_email = request.POST.get('student_email')
        due_date_str = request.POST.get('due_date')
        
        if not student_email:
            messages.error(request, "Student email is required.")
            return render(request, 'issue_book.html', {'book': book, 'students': User.objects.filter(role='student')})
        
        try:
            student = User.objects.get(username=student_email, role='student')
        except User.DoesNotExist:
            messages.error(request, "Student not found.")
            return render(request, 'issue_book.html', {'book': book, 'students': User.objects.filter(role='student')})
        
        # Check if book is available
        if book.copies_available <= 0:
            messages.error(request, "No copies available for this book.")
            return render(request, 'issue_book.html', {'book': book, 'students': User.objects.filter(role='student')})
        
        # Check if student already has this book issued
        existing_issue = BookIssue.objects.filter(
            book=book, 
            student=student, 
            action='issued'
        ).exists()
        
        if existing_issue:
            messages.error(request, f"{student.get_full_name()} already has this book issued.")
            return render(request, 'issue_book.html', {'book': book, 'students': User.objects.filter(role='student')})
        
        # Create the issue
        try:
            from datetime import datetime, timedelta
            due_date = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            else:
                # Default due date: 14 days from now
                due_date = datetime.now().date() + timedelta(days=14)
            
            BookIssue.objects.create(
                book=book,
                student=student,
                action='issued',
                due_date=due_date
            )
            
            # Update available copies
            book.copies_available -= 1
            book.save()
            
            messages.success(request, f"Book '{book.title}' issued to {student.get_full_name()} successfully.")
            return redirect('core:books_list')
            
        except Exception as e:
            messages.error(request, f"Error issuing book: {e}")
    
    # GET request - show form
    students = User.objects.filter(role='student').order_by('first_name', 'last_name')
    return render(request, 'issue_book.html', {'book': book, 'students': students})
