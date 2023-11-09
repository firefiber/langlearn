from django.db import models

# Create your models here.
class ComparisonMode(models.Model):
    MODE_CHOICES = [
        ('A', 'Mode A'),
        ('B', 'Mode B'),
    ]
    mode = models.CharField(max_length=1, choices=MODE_CHOICES, default='A')

    def __str__(self):
        return self.get_mode_display()
