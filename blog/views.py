from django.shortcuts import render, redirect
from itertools import chain
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from authentification.models import Ticket, Review, UserFollows
from . import forms
# Create your views here.


# Feed view
@login_required
def home(request):
    # Get authenticated user
    user = request.user
    posts = []

    # Get all users following
    userFollowing = UserFollows.objects.filter(user=user)

    # Get user review (the current user)
    userReview = Review.objects.filter(user=user)

    # Get only user Ticket (the current user)
    userTicket = Ticket.objects.filter(
        user=user).exclude(review__in=userReview)

    # Add the current user posts
    reviews = {user.id: userReview}
    tickets = {user.id: userTicket}

    # Add the following users posts
    for element in userFollowing:
        if element.followed_user:
            followed_user_id = element.followed_user.id
            review = Review.objects.filter(user=followed_user_id)
            ticket = Ticket.objects.filter(user=followed_user_id).exclude(
                review__in=userReview)
            reviews[followed_user_id] = review
            tickets[followed_user_id] = ticket

    review_ids = [review.id for reviews_list in reviews.values()
                  for review in reviews_list]
    ticket_ids = [ticket.id for tickets_list in tickets.values()
                  for ticket in tickets_list]

    # Fetch all reviews and tickets with a single query
    all_reviews = Review.objects.filter(id__in=review_ids)
    all_tickets = Ticket.objects.filter(id__in=ticket_ids)

    posts = sorted(chain(all_reviews, all_tickets),
                   key=lambda instance: instance.time_created, reverse=True)

    context = {
        'posts': posts,
    }
    return render(request, 'blog/home.html', context=context)


# User posts view
@login_required
def posts_view(request):
    # Import  tickets and reviews form database by id
    user = request.user
    reviews = Review.objects.filter(user=user)
    tickets = Ticket.objects.filter(user=user).exclude(review__in=reviews)

    context = {
        'tickets': tickets,
        'reviews': reviews,
    }
    return render(request, 'blog/posts.html', context=context)


# User ticket view
@login_required
def ticket_view(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            tikect = form.save(commit=False)
            tikect.user = request.user
            tikect.save()
            return redirect('home')
    else:
        form = forms.TicketForm()

    return render(request, 'blog/ask_for_ticket.html',
                  {"form": form})


# Update ticket view
@login_required
def ticket_update(request, id):
    ticket = Ticket.objects.get(id=id)
    ticketFile = ticket.image.url
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.TicketForm(instance=ticket)
    context = {
        'form': form,
        'ticketFile': ticketFile,
    }

    return render(request, 'blog/ticket_update.html', context=context)


# Delete ticket view
@login_required
def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')
    return render(request, 'blog/ticket_delete.html', {'ticket': ticket})


# Delete review view
@login_required
def review_delete(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        review.delete()
        return redirect('home')
    return render(request, 'blog/review_delete.html', {'review': review})


# Update review view
@login_required
def review_update(request, id):
    review = Review.objects.get(id=id)
    reviewTicketFile = review.ticket.image.url
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.ReviewForm(instance=review)
    context = {
        'form': form,
        'reviewTicketFile': reviewTicketFile,
    }

    return render(request, 'blog/review_update.html', context=context)


# User review view
@login_required
def review_view(request):
    formReview = forms.ReviewForm()
    formTicket = forms.TicketForm()
    if request.method == 'POST':
        formReview = forms.ReviewForm(request.POST)
        formTicket = forms.TicketForm(request.POST, request.FILES)
        if all([formReview.is_valid(), formTicket.is_valid()]):
            ticket = formTicket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = formReview.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'formReview': formReview,
        'formTicket': formTicket,
}
    return render(request, 'blog/create_review.html', context=context)


# Review respose view
@login_required
def review_response_view(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        formReview = forms.ReviewForm(request.POST)
        if formReview.is_valid():
            review = formReview.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    else:
        formReview = forms.ReviewForm()
    context = {
        'formReview': formReview,
        'ticket': ticket,
        }
    return render(request, 'blog/create_review_response.html', context=context)


# Abonnements view
@login_required
def abonnements_view(request):
    user = request.user
    userFollowing = UserFollows.objects.filter(user=user)
    userFollowedBy = UserFollows.objects.filter(followed_user=user)
    message = ""
    dejaAbonné = False
    if request.method == 'POST':
        form = forms.FollowUsers(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # Import model user
            User = get_user_model()
            userResults = User.objects.filter(username=username).first()
            if userResults:
                # check if user is followed yet
                for element in userFollowing:
                    if userResults == element.followed_user:
                        dejaAbonné = True
                # Check if the user is the authenticated user
                if userResults == user:
                    message = "On ne peut pas s'abonner a soit meme"
                elif dejaAbonné:
                    message = "Vous etes deja abonné a cet utlilisateur!"
                else:
                    userFollow = UserFollows()
                    userFollow.user = user
                    userFollow.followed_user = userResults
                    userFollow.save()
                    return redirect('abonnements-view')
            else:
                message = "l'utilisateur n'existe pas"

        else:
            message = "erreur de saisie!"
    else:
        form = forms.FollowUsers()
    context = {
        'form': form,
        'message': message,
        'userFollowing': userFollowing,
        'userFollowedBy': userFollowedBy,
    }
    return render(request, 'blog/abonnements.html', context=context)


# desbonnements view
@login_required
def desabonnements_view(request, id):
    userFollowing = UserFollows.objects.get(id=id)
    if request.method == 'POST':
        userFollowing.delete()
        return redirect('abonnements-view')

    context = {
        'userFollowing': userFollowing,
    }
    return render(request, 'blog/desabonnements.html', context=context)

