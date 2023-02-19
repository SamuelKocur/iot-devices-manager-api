from rest_framework import permissions


class LocalhostOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.META['REMOTE_ADDR'] == '127.0.0.1'