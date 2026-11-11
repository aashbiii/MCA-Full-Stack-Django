from django.db import models

RATING_CHOICES = [
    (1, '⭐ Poor'),
    (2, '⭐⭐ Fair'),
    (3, '⭐⭐⭐ Good'),
    (4, '⭐⭐⭐⭐ Very Good'),
    (5, '⭐⭐⭐⭐⭐ Excellent'),
]

CATEGORY_CHOICES = [
    ('general', 'General'),
    ('service', 'Service'),
    ('product', 'Product'),
    ('support', 'Support'),
    ('other', 'Other'),
]

class Feedback(models.Model):
    name        = models.CharField(max_length=100)
    email       = models.EmailField()
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    rating      = models.IntegerField(choices=RATING_CHOICES)
    subject     = models.CharField(max_length=200)
    message     = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.name} — {self.subject} ({self.get_rating_display()})"
