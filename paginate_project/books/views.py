from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Book

def book_list(request):
    query  = request.GET.get('q', '').strip()
    genre  = request.GET.get('genre', '')
    sort   = request.GET.get('sort', 'title')
    per_page = int(request.GET.get('per_page', 6))

    books = Book.objects.all()

    # --- Search ---
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    # --- Genre filter ---
    if genre:
        books = books.filter(genre=genre)

    # --- Sort ---
    sort_map = {
        'title':   'title',
        '-title':  '-title',
        'author':  'author',
        'year':    '-year',
        'rating':  '-rating',
    }
    books = books.order_by(sort_map.get(sort, 'title'))

    total = books.count()

    # --- Pagination ---
    paginator = Paginator(books, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Build page range (show max 5 pages around current)
    current = page_obj.number
    total_pages = paginator.num_pages
    start = max(current - 2, 1)
    end   = min(current + 2, total_pages)
    page_range = range(start, end + 1)

    # Preserve GET params (except page) for pagination links
    get_params = request.GET.copy()
    get_params.pop('page', None)
    query_string = get_params.urlencode()

    from .models import GENRE_CHOICES
    return render(request, 'books/book_list.html', {
        'page_obj':     page_obj,
        'query':        query,
        'genre':        genre,
        'sort':         sort,
        'per_page':     per_page,
        'total':        total,
        'page_range':   page_range,
        'query_string': query_string,
        'genre_choices': GENRE_CHOICES,
    })
