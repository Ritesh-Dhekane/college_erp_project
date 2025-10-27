# college_erp/core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Book, BookIssue

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Extra", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "copies_total", "copies_available")
    search_fields = ("title", "author", "isbn")
    list_filter = ("author",)


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    """
    Use callables for list_display to avoid errors if fields change.
    Ensures admin will not crash if model is slightly different.
    """
    def book_title(self, obj):
        # safe accessor, returns readable fallback if missing
        return getattr(obj.book, "title", str(obj.book))

    book_title.short_description = "Book"

    def student_username(self, obj):
        return getattr(obj.student, "username", str(obj.student))

    student_username.short_description = "Student"

    def action_value(self, obj):
        return getattr(obj, "action", "-")

    def issued_at_value(self, obj):
        return getattr(obj, "issued_at", None)

    def returned_at_value(self, obj):
        return getattr(obj, "returned_at", None)

    list_display = ("book_title", "student_username", "action_value", "issued_at_value", "returned_at_value")
    list_filter = ("action",) if "action" in [f.name for f in BookIssue._meta.get_fields()] else ()
    search_fields = ("book__title", "student__username")
