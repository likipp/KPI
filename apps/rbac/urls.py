from rest_framework import routers

from django.urls import path, include

from rbac.views import user_view, organization_view, position_view, role_view, menu_view, permission_view

router = routers.SimpleRouter()
router.register('users', user_view.UserViewSet, base_name="users")
router.register('center', user_view.UserCenterViewSet, base_name='center')
router.register('organizations', organization_view.OrganizationViewSet, base_name="organizations")
router.register('position', position_view.PositionViewSet, base_name="position")
router.register('menus', menu_view.MenuViewSet, base_name="menus")
router.register('roles', role_view.RoleViewSet, base_name="roles")
router.register('permissions', permission_view.PermissionViewSet, base_name="permission")
router.register('role_permission', role_view.RoleSingleViewSet, base_name='role_permission')

urlpatterns = [
    path('', include(router.urls)),
    path('users/list', user_view.UserListView.as_view(), name='user_list'),
    path('users/info', user_view.UserInfoView.as_view(), name='user_info'),
    path('organization/tree/', organization_view.OrganizationTreeView.as_view(), name='organizations_tree'),
    path('organization/user/tree/', organization_view.OrganizationUserTreeView.as_view(),
         name='organization_user_tree'),
    path('menu/tree/', menu_view.MenuTreeView.as_view(), name='menus_tree'),
    path('role/tree/', role_view.RoleTreeViewSet.as_view(), name='role_tree'),
    path('permission/tree/', permission_view.PermissionToMenuView.as_view(), name='permission_tree'),
    # path('role/single/', role_view.RoleSingleViewSet.as_view({'get': 'list'}), name='role-single')
    # path('auth/build/menus/', user_view.UserBuildMenuView.as_view(), name='build_menus')
]
