from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permissions(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll allways allow GET, HEAD or OPTION request.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # write permissions are only allowed to the owner of the project
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to read it.
    """

    def has_object_permissions(self, request, view, obj):
        # Read and write permissions are allowed to owner.
        print "User : %s" % request.user
        print "Owner: %s" % obj.owner
        return obj.owner == request.user


class IsReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow rad an object.
    """

    def has_object_permissions(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
