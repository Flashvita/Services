from django import views
from .models import Requester, Order, Executor, Category, ResponseForOrder, MyOrders
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import LoginForm, RegistrationForm, SearchOrderForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LogoutView
from .forms import NewOrderForm, UserEditForm, ExecutorEditForm, RequesterEditForm, ResponseForm, MyWorksForm
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import get_object_or_404


class BaseView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})


class OrderDetailView(DetailView):
    """Подробности объявления"""
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'


class AllOrdersView(ListView):
    """Все объявления"""
    template_name = 'order/all_orders.html'
    context_object_name = 'orders'

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(is_active=True)
        categories = Category.objects.all()
        paginator = Paginator(orders, 2)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context = {
            'categories': categories,
            'page': page,
            'orders': page.object_list,
        }
        return render(request, 'order/all_orders.html', context)


class CategoryDetailView(views.View):

    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)

        orders = Order.objects.filter(category=category, is_active=True)
        context = {
            'orders': orders,
            'category': category,
        }
        return render(request, 'category/categories_detail.html', context)


class MyOrdersView(ListView):
    """Мои активные объявления"""
    def get(self, request, *args, **kwargs):
        requester = Requester.objects.get(user=request.user)
        my_orders = Order.objects.filter(requester__user=requester.user, is_active=True)
        context = {
            'my_orders': my_orders,

        }
        return render(request, 'order/my_orders.html', context)


class MyArchiveOrdersView(ListView):
    """Мои объявления в архиве"""
    def get(self, request, *args, **kwargs):
        requester = Requester.objects.get(user=request.user)
        my_archive_orders = Order.objects.filter(requester__user=requester.user, is_active=False)
        context = {
            'my_archive_orders': my_archive_orders,

        }
        return render(request, 'order/my_archive_orders.html', context)


class OrderRemovePublishView(views.View, Order):
    """Снять объявление с публикации"""

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.filter(requester__user=request.user, pk=pk, is_active=True)
        order.update(is_active=False)

        context = {
            'order': order,
        }
        return render(request, 'order/publish_off.html', context)

    def post(self, request, pk):
        order = Order.objects.filter(requester__user=request.user, pk=pk, is_active=True)
        order.update(is_active=False)
        if order.update:
            messages.success(request, 'Ваше объявление неактивно(перемещено в архив)')
            return HttpResponseRedirect('/account/personal_requester/')
        else:
            context = {
                'order': order,
            }
            return render(request, 'order/publish_on.html', context)


class OrderAgainPublishView(views.View, Order):
    """Опубликовать повторно"""

    def get(self, request, pk):
        order = Order.objects.filter(requester__user=request.user, pk=pk, is_active=False)
        order.update(is_active=True)
        context = {
            'order': order,
        }

        return render(request, 'order/publish_on.html', context)

    def post(self, request, pk):
        order = Order.objects.filter(requester__user=request.user, pk=pk, is_active=False)
        order.update(is_active=True)
        if order.update:
            messages.success(request, 'Ваше объявление успешно опубликованно повторно')
            return HttpResponseRedirect('/account/personal_requester/')
        else:
            context = {
                'order': order,
            }
            return render(request, 'order/publish_on.html', context)


class OrderEditView(UpdateView):
    """Редактирование объявления"""
    model = Order
    fields = ['name', 'category', 'description', 'district', 'image', 'price', ]
    template_name = 'order/order_edit.html'


class OrderDeleteView(DeleteView):
    """Удаление объявления"""
    model = Order
    template_name = 'order/order_delete.html'
    success_url = '/account/personal_requester/'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Ваше объявление успешно удалено')
        return self.delete(request, *args, **kwargs)


class AllExecutorView(ListView):
    """Все  зарегестрированные исполнители"""
    model = Executor
    template_name = 'executor/all_executor.html'
    context_object_name = 'executors'

    def get_queryset(self):
        return Executor.objects.all()


class AllMyWorksView(ListView):
    """Все  выполненые заказы"""
    model = MyOrders
    template_name = 'executor/all_complete_orders.html'
    context_object_name = 'complete_orders'


class MyWorksView(views.View):
    def get(self, request, *args, **kwargs):
        form = MyWorksForm(request.GET)
        context = {
            'form': form
        }
        return render(request, 'executor/complete_order.html', context)

    def post(self, request, *args, **kwargs):
        form = MyWorksForm(request.POST or None)
        if form.is_valid():
            new_complete_order = form.save(commit=False)
            new_complete_order.name = form.cleaned_data['name']
            new_complete_order.description = form.cleaned_data['description']
            new_complete_order.image = form.cleaned_data['image']

            MyOrders.objects.create(
                name=new_complete_order.name,
                description=form.cleaned_data['description'],
                image=form.cleaned_data['image'],
                executor=Executor.objects.get(user=request.user)
            )

            return HttpResponseRedirect('/account/personal_executor/')
        context = {
            'form': form,
        }
        return render(request, 'executor/complete_order.html', context)



class ExecutorDetailView(DetailView):
    """Вся информация об исполнителе"""
    model = Executor
    template_name = 'executor/executor_detail.html'
    context_object_name = 'executor'


    def get(self, request, pk, *args, **kwargs):
        executor = get_object_or_404(Executor, pk=pk)
        works = MyOrders.objects.filter(executor=executor)
        context = {
            'executor': executor,
            'works': works
        }
        return render(request, 'executor/executor_detail.html', context )



class PersonalWorksView(views.View):
    def get(self, request, pk, *args, **kwargs):
        executor = get_object_or_404(Executor, pk=pk)
        works = MyOrders.objects.filter(executor=executor)
        context = {
            'executor': executor,
            'works': works
        }
        return render(request, 'executor/personal_works.html', context)

class RequesterDetailView(DetailView):
    """Вся информация об заказщике"""
    model = Requester
    template_name = 'requester/requester_detail.html'
    context_object_name = 'requester'


class RequesterEditView(views.View):
    """Редактирования профиля заказщика"""

    def get(self, request, *args, **kwargs):

        user_form = UserEditForm(instance=request.user)
        requester_form = RequesterEditForm(instance=request.user.requester)

        context = {
            'user_form': user_form,
            'requester_form': requester_form,

        }
        return render(request, 'requester/requester_edit.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(data=request.POST,instance=request.user)
        requester_form = RequesterEditForm(data=request.POST,instance=request.user.requester )
        if user_form.is_valid() and requester_form.is_valid():
            requester_form.save()
            user_form.save()
            return HttpResponseRedirect('/account/personal_requester/')
        context = {
            'user_form': user_form,
            'requester_form': requester_form,
        }
        return render(request, 'requester/requester_edit.html', context)


class SearchOrderView(ListView):

    def get(self, request, *args, **kwargs):
        form = SearchOrderForm(request.GET)
        query = None
        results = []
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Order.objects.annotate(
                search=SearchVector('name', 'description'),
            ).filter(search=query)
        context = {
                    'form': form,
                    'query': query,
                    'results': results
                  }
        return render(request, 'order_search.html', context)


class LoginView(views.View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            context = {
                'form': form
            }
            return render(request, 'login.html', context)


class RegistrationRequesterView(views.View):
    """Регистрация для заказщика"""
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'registration/requester.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Requester.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],

            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрированы!')
            return HttpResponseRedirect('/account/personal_requester/')

        context = {
            'form': form
        }
        return render(request, 'registration/requester.html', context)


class RegistrationExecutorView(views.View):
    """Регистрация для исполнителя"""
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)

        context = {
            'form': form,

        }
        return render(request, 'registration/executor.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Executor.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],

            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            messages.success(request,
                             'Вы успешно зарегестрированы!Рекомендуем отредактировать свой профиль,'
                             ' заказщики смотрят анкеты исполнителей')
            return HttpResponseRedirect('/account/personal_executor/')

        context = {
            'form': form
        }
        return render(request, 'registration/executor.html', context)


class ExecutorEditView(views.View):
    """Редактирования профиля исполнителя"""
    def get(self, request, *args, **kwargs):

        user_form = UserEditForm(instance=request.user)
        executor_form = ExecutorEditForm(instance=request.user.executor)

        context = {
            'user_form': user_form,
            'executor_form': executor_form,

        }
        return render(request, 'account/executor_edit.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(data=request.POST, instance=request.user)
        executor_form = ExecutorEditForm(data=request.POST, instance=request.user.executor)
        if user_form.is_valid() and executor_form.is_valid():
            user_form.save()
            executor_form.save()

            return HttpResponseRedirect('/account/personal_executor/')
        context = {
            'user_form': user_form,
            'executor_form': executor_form,
        }
        return render(request, 'account/executor_edit.html', context)


class AccountRequesterView(views.View):

    def get(self, request, *args, **kwargs):
        requester = Requester.objects.get(user=request.user)
        user = requester.user
        context = {
            'requester': requester,
            'user': user
        }
        return render(request, 'account/personal_requester.html', context)


class AccountExecutorView(views.View):

    def get(self, request, *args, **kwargs):
        executor = Executor.objects.get(user=request.user)
        user = executor.user
        context = {
            'executor': executor,
            'user': user
        }
        return render(request, 'account/personal_executor.html', context)


class LogoutUserView(LogoutView):
    next_page = 'base'
    template_name = 'base.html'


class ResponseView(views.View):
    def get(self, request):
        form = ResponseForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'order/response.html', context)

    def post(self, request, pk):
        form = ResponseForm(request.POST or None)
        response = ResponseForOrder.objects.filter(sender__user=request.user, order=pk)

        if form.is_valid() and  not response:
            new_response = form.save(commit=False)
            new_response.text = form.cleaned_data['text']
            ResponseForOrder.objects.create(
                text=form.cleaned_data['text'],
                sender=Executor.objects.get(user=request.user),
                order=Order.objects.get(pk=pk),
            )

            messages.success(request, 'Ваш отклик успешно отправлен')
            return HttpResponseRedirect('/account/personal_executor/')
        messages.error(request, 'Вы уже отправляли отклик по данному заказу')
        return HttpResponseRedirect('/account/personal_executor/')


class NewOrderView(views.View):

    def get(self, request, *args, **kwargs):
        form = NewOrderForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'order/new_order.html', context)

    def post(self, request, *args, **kwargs):
        form = NewOrderForm(request.POST or None)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.image = form.cleaned_data['image']
            new_order.category = form.cleaned_data['category']
            new_order.description = form.cleaned_data['description']
            new_order.district = form.cleaned_data['district']
            new_order.price = form.cleaned_data['price']
            Order.objects.create(
                name=new_order,
                category=form.cleaned_data['category'],
                district=form.cleaned_data['district'],
                price=form.cleaned_data['price'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data['image'],
                requester=Requester.objects.get(user=request.user)
            )
            return HttpResponseRedirect('/account/personal_requester/')
        context = {
            'form': form,
        }
        return render(request, 'order/new_order.html', context)


class AllResponseOrderView(ListView):
    context_object_name = 'responses'
    model = ResponseForOrder
    template_name = 'notifications/responses.html'

    def get_queryset(self):
        return ResponseForOrder.objects.all().order_by('order__name')


class ResponseOrderDetailView(DetailView):
    context_object_name = 'response'
    model = ResponseForOrder
    template_name = 'notifications/response_detail.html'


