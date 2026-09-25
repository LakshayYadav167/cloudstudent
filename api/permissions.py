from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    """
    General permission for role-based access.
    Admins: Full access.
    Teachers: Read/Write access (views will filter querysets).
    Students: Read-only access.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        role = request.user.role
        
        if role == 'ADMIN':
            return True
            
        if role == 'TEACHER':
            return True # Teachers can create/update, but only on their resources (checked in serializers/views)
            
        if role == 'STUDENT':
            # Students can only read (GET, HEAD, OPTIONS)
            return request.method in permissions.SAFE_METHODS
            
        return False
