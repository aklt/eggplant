from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import UserProfile


class NewUserForceProfileMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.is_superuser:
            allowed_paths = (
                reverse('profile'),
                reverse('account_login'),
                reverse('account_logout'),
                reverse('eggplant:membership:new_member_set_password'),
            )
            if request.path not in allowed_paths:
                try:
                    profile = request.user.userprofile
                except UserProfile.DoesNotExist:
                    profile = None
                if not profile or not profile.is_complete():
                    msg = "Please update your profile."
                    messages.add_message(request, messages.WARNING, msg)
                    return HttpResponseRedirect(reverse('profile'))
