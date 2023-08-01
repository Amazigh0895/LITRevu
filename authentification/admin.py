from django.contrib import admin
from authentification.models import UserFollows, User, Ticket, Review

# Register your models here.


admin.site.register(UserFollows)
admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Review)