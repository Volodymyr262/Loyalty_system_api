from rest_framework import permissions

class IsOwnerOfLoyaltyProgram(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a Loyalty Program to access its data.
    """

    def has_object_permission(self, request, view, obj):
        """ Allow only the owner of the Loyalty Program to access it """
        return obj.owner == request.user  # Only the owner can view/edit
