from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read-only requests are allowed for any user
        if request.method in permissions.SAFE_METHODS:
            return True

        # write permissions are only allowed to the sender of a parcel
        return obj.sender == request.user