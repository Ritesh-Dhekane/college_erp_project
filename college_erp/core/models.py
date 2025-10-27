from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
        ("clerk", "Clerk"),
        ("librarian", "Librarian"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    # Avoid clashes with auth.User
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


# ---------------------------
# Library models
# ---------------------------
class Book(models.Model):
    """Basic book record."""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True)
    year_published = models.PositiveSmallIntegerField(null=True, blank=True)
    copies_total = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} — {self.author}"

class BookIssue(models.Model):
        """Tracks which user has which book and its status."""

ACTION_CHOICES = [
        ("issued", "Issued"),
        ("returned", "Returned"),
        ("lost", "Lost"),
    ]

book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="issues")
student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="book_issues"
    )
action = models.CharField(max_length=10, choices=ACTION_CHOICES, default="issued")
issued_at = models.DateTimeField(default=timezone.now)
due_date = models.DateField(null=True, blank=True)
returned_at = models.DateTimeField(null=True, blank=True)
note = models.TextField(blank=True)

class Meta:
        ordering = ["-issued_at"]
        verbose_name = "Book Issue"
        verbose_name_plural = "Book Issues"

def __str__(self):
        return f"{self.book.title} -> {self.student.username} ({self.action})"
