from rest_framework.permissions import IsAuthenticated

class IsAuthenticatedAndOwnData(IsAuthenticated):
    '''
    Permission class for logged in users to show only their own inventory
    Allow if the username in the url and the username of the logged in user are the same
    '''
    
    def has_permission(self, request, view):
        if (request.user 
            and request.user.is_authenticated
            and request.user.username == view.kwargs['username']):
            return True
        return False
    