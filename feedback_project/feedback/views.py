from django.shortcuts import render, redirect
from django.db.models import Avg, Count
from .forms import FeedbackForm
from .models import Feedback

def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/submit.html', {'form': form})

def success(request):
    return render(request, 'feedback/success.html')

def all_feedback(request):
    feedbacks = Feedback.objects.all()
    stats = Feedback.objects.aggregate(
        avg_rating=Avg('rating'),
        total=Count('id'),
    )
    category_counts = Feedback.objects.values('category').annotate(count=Count('id'))
    return render(request, 'feedback/list.html', {
        'feedbacks': feedbacks,
        'stats': stats,
        'category_counts': category_counts,
    })
