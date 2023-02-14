from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            #check permission for read_only
            return True

        else:
            #check permission for write
            return super().has_permission(request,view)


class ReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            #check permission for read_only
            return True

        else:
            #check permission for write
            return obj.review_user == request.user or request.user.is_staff