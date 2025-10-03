from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permission to only allow admin users or owners of an object to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.role == 'admin':
            return True
        
        # Object owner can access their own object
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # For User objects, check if it's the same user
        if obj == request.user:
            return True
        
        return False


class IsPatient(permissions.BasePermission):
    """
    Permission to only allow patients to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'patient'


class IsDoctor(permissions.BasePermission):
    """
    Permission to only allow doctors to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'doctor'


class IsDoctorOrAdmin(permissions.BasePermission):
    """
    Permission to only allow doctors or admins to access the view.
    """
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and 
                request.user.role in ['doctor', 'admin'])


class IsPatientOrAdmin(permissions.BasePermission):
    """
    Permission to only allow patients or admins to access the view.
    """
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and 
                request.user.role in ['patient', 'admin'])


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class IsAppointmentParticipant(permissions.BasePermission):
    """
    Permission to only allow appointment participants (patient, doctor) or admin to access.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        
        if hasattr(obj, 'patient') and hasattr(obj, 'doctor'):
            return (obj.patient.user == request.user or 
                   obj.doctor.user == request.user)
        
        return False