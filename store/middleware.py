from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [
            reverse('login'),
            reverse('register'),
            reverse('password_reset'),
            reverse('password_reset_done'),
            reverse('password_reset_confirm', kwargs={'uidb64': 'dummy', 'token': 'dummy-token'}),
            reverse('password_reset_complete')
        ]
        
        if not request.user.is_authenticated and not any(request.path.startswith(path) for path in allowed_paths):
            return redirect('login')

        response = self.get_response(request)
        return response
