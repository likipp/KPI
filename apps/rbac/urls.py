from rest_framework import routers

from django.urls import path, include

from rbac.views import user_view, organization_view, position_view, role_view, menu_view

router = routers.SimpleRouter()
router.register('users', user_view.UserViewSet, base_name="users")
router.register('organizations', organization_view.OrganizationViewSet, base_name="organizations")
router.register('position', position_view.PositionViewSet, base_name="position")
router.register('menus', menu_view.MenuViewSet, base_name="menus")
router.register('roles', role_view.RoleViewSet, base_name="roles")

urlpatterns = [
    path('', include(router.urls)),
    path('users/list', user_view.UserListView.as_view(), name='user_list'),
    path('users/info', user_view.UserInfoView.as_view(), name='user_info'),
    path('organization/tree/', organization_view.OrganizationTreeView.as_view(), name='organizations_tree'),
    path('organization/user/tree/', organization_view.OrganizationUserTreeView.as_view(),
         name='organization_user_tree'),
    path('menu/tree/', menu_view.MenuTreeView.as_view(), name='menus_tree')
]
