from rest_framework.permissions import BasePermission

class IsContractor(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'contractor'

class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'worker'

class IsInCharge(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'in_charge'
