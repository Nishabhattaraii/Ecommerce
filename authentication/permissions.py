from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsSellerUser(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if  user.seller_user or user.is_superuser: 
            return True
        raise PermissionDenied(detail="You cannot perform this action")
    

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        user =  request.user
        if user.customer_user or user.is_superuser:
            return True
        raise PermissionDenied(detail="You cannot perform this action")
