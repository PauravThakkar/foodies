from django.contrib.auth.models import User

class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_cuisine = models.CharField(max_length=50, blank=True, null=True)
    notifications_enabled = models.BooleanField(default=True)
    email_frequency = models.CharField(max_length=20, choices=[('daily', 'Daily'), ('weekly', 'Weekly')], default='daily')
