from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Movie, Review
from .forms import ReviewForm

# Create your views here.
def home(request):
  searchTerm = request.GET.get('searchMovie')
  if searchTerm:
    movies = Movie.objects.filter(title__icontains=searchTerm)
  else:
    movies = Movie.objects.all()
  return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
  return HttpResponse('<h1>About Page</h1>')

def signup(request):
  email = request.GET.get('email')
  return render(request, 'signup.html', {'email': email})

def detail(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)
  reviews = Review.objects.filter(movie=movie)
  return render(request, 'detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def createreview(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)
  if request.method == 'GET':
    return render(request, 'createreview.html', {'form': ReviewForm(), 'movie': movie})
  else:
    try:
      form = ReviewForm(request.POST)
      new_review = form.save(commit=False)
      new_review.user = request.user
      new_review.movie = movie
      new_review.save()
      return redirect('detail', new_review.movie.id)
    except ValueError:
      return render(request, 'createreview.html', {'form': ReviewForm(), 'error': 'Bad data passed in'})

@login_required
def updatereview(request, review_id):
  review = get_object_or_404(Review, pk=review_id, user=request.user)
  if request.method == 'GET':
    form = ReviewForm(instance=review)
    return render(request, 'updatereview.html', {'form': form, 'review': review})
  else:
    try:
      form = ReviewForm(request.POST, instance=review)
      form.save()
      return redirect('detail', review.movie.id)
    except ValueError:
      return render(request, 'updatereview.html', {'form': form, 'review': review, 'error': 'Bad data passed in'})

@login_required
def deletereview(request, review_id):
  review = get_object_or_404(Review, pk=review_id)
  review.delete()
  return redirect('detail', review.movie.id)
  