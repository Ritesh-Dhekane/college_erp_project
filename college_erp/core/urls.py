from django.urls import path
from . import views


app_name = "core"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('library/', views.library, name='library'),

     # Dashboards for each role
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/clerk/', views.clerk_dashboard, name='clerk_dashboard'),
    path('dashboard/librarian/', views.librarian_dashboard, name='librarian_dashboard'),

    # Library management URLs
    path('library/my-books/', views.student_issued_books, name='student_issued_books'),
    path('library/all-issues/', views.all_book_issue_history, name='all_book_issue_history'),
    path('library/available-books/', views.available_books, name='available_books'),
    path('books/issue/<int:book_id>/', views.issue_book, name='issue_book'),
    path('books/return/<int:issue_id>/', views.return_book, name='return_book'),
    path('analytics/', views.librarian_analytics, name='librarian_analytics'),


    # Helpful endpoints referenced from templates (add if missing in views.py)
    path('books/add/', views.add_book, name='books_add'),
    path('books/', views.available_books, name='books_list'),
    path('issues/manage/', views.manage_issues, name='issues_manage'),

    path('profile/', views.profile, name='profile'),
]
