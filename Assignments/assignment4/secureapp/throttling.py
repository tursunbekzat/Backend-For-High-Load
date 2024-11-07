from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled

class UserRoleThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        # Apply different throttle rates based on the user's role
        if request.user.is_authenticated:
            if request.user.is_staff:  # Admin or staff role
                self.rate = '1000/minute'  # Higher limit for admins
            else:  # Regular authenticated users
                self.rate = '100/minute'
        else:
            # Use default rate for anonymous users
            self.rate = '10/minute'
        
        return super().get_cache_key(request, view)
    
    def allow_request(self, request, view):
        """
        Override allow_request to check and handle throttling based on custom limits.
        """
        if not super().allow_request(request, view):
            self.throttle_failure(request, view)
            raise Throttled(detail="Request limit exceeded.")
        return True
