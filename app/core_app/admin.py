from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core_app import models
# to translate the model field into human readable
# in the admin page of django
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['name', 'email']
    # the fields of the model
    # adding the required sections for any user object
    # to display and edit in the admin panel
    fieldsets = (
        # the custom section
        (None, {"fields": ("email", "password"), }),
        # section for some personal info
        (_('personal info'), {"fields": ("name",), }),
        # the permissions section
        (
            _("permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")}
        ),
        # section for some important dates
        (_("Important dates"), {"fields": ("last_login",)})

    )
    # the required fields for the add page in the admin panel
    add_fieldsets = (
        (None, {
            "classes": "wide",
            "fields": ("email", "password1", "password2")
        }),
    )


# finally registering the user model into the admin panel
admin.site.register(models.User, UserAdmin)
