ROLE_PERMISSIONS={
    "admin":{"*"},
    "manager":{"view_employee","add_employee","change_employee","delete_employee"},
    "staff":{"view_employee"},
    "lead":{"view_employee","change_employee"},
    "simpleuser":{"view_employee"}
}

"""
BUILT IN PERMISSIONS
AllowAny(no authentication needed)
Authenticated(only loggined in users)
IsAdminUser
IsAuthenticatedOrReadOnly(read only for unauthenticated users'GET' and full access for authenticated users)
DjangoModelPermissions:
Permission	Codename(profile is model)
View	view_profile    GET
Add	    add_profile     POST
Change	change_profile  PUT/PATCH
Delete	delete_profile  DELETE
It maps HTTP methods → model permissions.These are built in model permissions.
does not give permission to unauthenticated users.
give permission to authenticated users based on their model permissions.




can give custom permissions by creating a groups in authentication.groups in /admin/.

way of giving custom permissions to user.
from django.contrib.auth.models import Permission

perm = Permission.objects.get(codename="add_post")
user.user_permissions.add(perm)

        
should create model permissions in admin panel for user and assign them to user.
Example:
title="first post",My first blog post","Django permissions explained","Meeting notes","Announcement 2025","Hello World"


permission_classes = [IsAuthenticated, IsAdminUser]
'User must be authenticated
AND(not OR)
User must be admin
'
"""

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

perm = Permission.objects.get(codename="add_post")
User.user_permissions.add(perm)
