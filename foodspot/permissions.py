from rest_framework import permissions

class IsCreationOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if view.action == 'create':
                return True
            else:
                return False
        else:
            return True

class IsOwnerOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.owner == request.user

class IsAuthenticated(permissions.BasePermission):

	def has_permission(self, request, view):
		if not request.user.is_authenticated():
			print "Not Authenticated"
			return False
		else:
			print "Authenticated as " + request.user.username
			return True
