from rest_framework.permissions import IsAuthenticated

class IsAuthenticatedAndOwnData(IsAuthenticated):

    #Added custom permmission
    def has_permission(self, request, view):
        if (request.user 
            and request.user.is_authenticated
            and request.user.username == view.kwargs['username']):
            return True
        return False
    