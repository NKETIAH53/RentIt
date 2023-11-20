from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Invalid email. Provide a valid email."))

    def create_user(self, username, firstname, lastname, email, password, **kwargs):
        if not username:
            raise ValueError(_("Provide a username."))
        if not firstname:
            raise ValueError(_("Provide a firstname."))
        if not lastname:
            raise ValueError(_("Provide a lastname."))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Email address is required to set up account."))

        user = self.model(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            **kwargs
        )
        user.set_password(password)
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, firstname, lastname, email, password, **kwargs
    ):
        if not password:
            raise ValueError(_("Provide password for user."))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(
                _("Email address is required to set up superuser account.")
            )
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if not (kwargs.get("is_staff") and kwargs.get("is_superuser")):
            raise ValueError(
                _("is_staff and is_superuser must be set to True for superusers")
            )

        user = self.create_user(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            **kwargs
        )
        
        user.save(using=self._db)
        return user
