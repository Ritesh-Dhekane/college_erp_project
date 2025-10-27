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


    # Helpful endpoints referenced from templates (add if missing in views.py)
    path('books/add/', views.add_book, name='add-book'),
    path('issues/manage/', views.manage_issues, name='manage-issues'),

    path('profile/', views.profile, name='profile'),
]
