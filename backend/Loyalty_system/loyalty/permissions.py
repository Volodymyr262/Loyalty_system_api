from rest_framework import permissions

from rest_framework import permissions
from .models import UserTaskProgress, SpecialTask
class IsOwnerOfLoyaltyProgram(permissions.BasePermission):
    """Allow only the owner of the Loyalty Program to access it"""

    def has_object_permission(self, request, view, obj):
        """Check if the requesting user owns the related Loyalty Program"""
        if hasattr(obj, "program"):  # If obj is LoyaltyTier, access program's owner
            return obj.program.owner == request.user
        if isinstance(obj, UserTaskProgress):
            return obj.task.program.owner == request.user  # Fix for UserTaskProgress
        return obj.owner == request.user  # Default case for LoyaltyProgram