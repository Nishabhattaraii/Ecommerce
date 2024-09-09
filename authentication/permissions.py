from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsStaffUser(BasePermission):

    def has_permission(self, request, view):

        user = request.user
        if  user.is_staff or user.is_superuser: 
            return True
        raise PermissionDenied(detail="You cannot perform this action")
    

 