from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentification.models import Ticket, Review, UserFollows
from . import forms

# Create your views here.


@login_required
def home(request):
    # Import all tickets and reviews form database
    reviews = Review.objects.all()
    tickets = Ticket.objects.all().exclude(review__in=reviews)

    context = {
        'tickets': tickets,
        'reviews': reviews,
    }
    return render(request, 'blog/home.html', context=context)


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


@login_required
def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')
    return render(request, 'blog/ticket_delete.html', {'ticket': ticket})

@login_required
def review_delete(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        review.delete()
        return redirect('home')
    return render(request, 'blog/review_delete.html', {'review': review})


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

@login_required
def abonnements_view(request):
    user = request.user
    userFollowing = user.following.all()
    userFollowedBy = user.followed_by.all()
    context = {
        'userFollowing': userFollowing,
        'userFollowedBy': userFollowedBy,
    }
    return render(request, 'blog/abonnements.html', context=context)
