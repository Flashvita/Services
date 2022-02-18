from django.urls import path
from .views import BaseView, OrderDetailView, LoginView, RegistrationRequesterView, RegistrationExecutorView
from .views import AccountRequesterView, AccountExecutorView, LogoutUserView, NewOrderView, AllOrdersView
from .views import AllExecutorView, ExecutorDetailView, MyOrdersView, ExecutorEditView, AllMyWorksView
from .views import CategoryDetailView, OrderEditView, OrderDeleteView, RequesterDetailView
from .views import RequesterEditView, OrderRemovePublishView, MyArchiveOrdersView
from .views import OrderAgainPublishView, ResponseView, AllResponseOrderView
from .views import ResponseOrderDetailView, SearchOrderView, MyWorksView, PersonalWorksView


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/requester/', RegistrationRequesterView.as_view(), name='requester'),
    path('registration/executor/', RegistrationExecutorView.as_view(), name='executor'),
    path('account/personal_executor/', AccountExecutorView.as_view(), name='personal_executor'),
    path('account/personal_requester/', AccountRequesterView.as_view(), name='personal_requester'),
    path('order/new_order/', NewOrderView.as_view(), name='new_order'),
    path('registration/logout/', LogoutUserView.as_view(), name='logout'),
    path('order/all_orders/', AllOrdersView.as_view(), name='all_orders'),
    path('order_search/', SearchOrderView.as_view(), name='order_search'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('executor/all_executor/', AllExecutorView.as_view(), name='all_executor'),
    path('executor/<int:pk>/', ExecutorDetailView.as_view(), name='executor_detail'),
    path('order/my_orders/', MyOrdersView.as_view(), name='my_orders'),
    path('order/my_orders/my_archive_orders/', MyArchiveOrdersView.as_view(), name='my_archive_orders'),
    path('order/<int:pk>/publish_on/', OrderAgainPublishView.as_view(), name='publish_on'),
    path('order/<int:pk>/order_delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('account/executor_edit/', ExecutorEditView.as_view(), name='executor_edit'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='categories_detail'),
    path('order/<int:pk>/order_edit/', OrderEditView.as_view(), name='order_edit'),
    path('requester/<int:pk>>/', RequesterDetailView.as_view(), name='requester_detail'),
    path('requester/<int:pk>/requester_edit/', RequesterEditView.as_view(), name='requester_edit'),
    path('order/<int:pk>/publish_off/', OrderRemovePublishView.as_view(), name='publish_off'),
    path('order/<int:pk>/response/', ResponseView.as_view(), name='response'),
    path('notifications/responses/', AllResponseOrderView.as_view(), name='responses'),
    path('notifications/<int:pk>/', ResponseOrderDetailView.as_view(), name='response_detail'),
    path('executor/complete_order/', MyWorksView.as_view(), name='complete_order'),
    path('executor/all_complete_orders/', AllMyWorksView.as_view(), name='all_complete_orders'),
    path('executor/<int:pk>/personal_works/', PersonalWorksView.as_view(), name='personal_works')
]
