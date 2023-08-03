from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.


@login_required
def home(request):
    return render(request, 'blog/home.html')


@login_required
def ticket_view(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            tikect = form.save(commit=False)
            tikect.user = request.user
            tikect.save()
    else:
        form = forms.TicketForm()

    return render(request, 'blog/ask_for_ticket.html',
                  {"form": form})

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
    context = {
        'formReview': formReview,
        'formTicket': formTicket,
}
    return render(request, 'blog/create_review.html', context=context)