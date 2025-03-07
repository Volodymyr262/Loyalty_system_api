from rest_framework import permissions

from rest_framework import permissions

class IsOwnerOfLoyaltyProgram(permissions.BasePermission):
    """Allow only the owner of the Loyalty Program to access it"""

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user owns the related Loyalty Program"""
        if hasattr(obj, "program"):  # If obj is LoyaltyTier, access program's owner
            return obj.program.owner == request.user
        return obj.owner == request.user  # Default case for LoyaltyProgram