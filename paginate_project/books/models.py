from django.db import models

GENRE_CHOICES = [
    ('fiction',     'Fiction'),
    ('non-fiction', 'Non-Fiction'),
    ('science',     'Science'),
    ('technology',  'Technology'),
    ('history',     'History'),
    ('biography',   'Biography'),
]

class Book(models.Model):
    title      = models.CharField(max_length=200)
    author     = models.CharField(max_length=100)
    genre      = models.CharField(max_length=20, choices=GENRE_CHOICES)
    year       = models.IntegerField()
    rating     = models.DecimalField(max_digits=3, decimal_places=1)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
