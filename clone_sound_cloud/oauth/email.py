from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = "oauth/email/activation.html"


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = "oauth/email/confirmation.html"


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "oauth/email/password_reset.html"


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "oauth/email/password_changed_confirmation.html"


class UsernameChangedConfirmationEmail(email.UsernameChangedConfirmationEmail):
    template_name = "oauth/email/username_changed_confirmation.html"


class UsernameResetEmail(email.UsernameResetEmail):
    template_name = "oauth/email/username_reset.html"
