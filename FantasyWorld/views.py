from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Subclass, Response, Category
from .forms import ResponseForm, SubclassForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Gamer
from .tasks import response_send_email, response_accept_send_email
from .filters import SubclassFilter


class SubclassList(ListView):
    model = Subclass
    template_name = 'subclasslist.html'
    context_object_name = 'subclass'
    ordering = '-subclass_time'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubclassDetail(LoginRequiredMixin, DetailView):
    model = Subclass
    template_name = 'subclass_detail.html'
    context_object_name = 'subclass'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subclass_author = Subclass.objects.get(id=self.kwargs['pk']).author
        context['is_author'] = self.request.user == subclass_author
        response_authors = Response.objects.filter(response_subclass=self.kwargs['pk']).values('author')
        context['response'] = {'author': self.request.user.id} in response_authors
        return context


class SubclassCreate(LoginRequiredMixin, CreateView):
    form_class = SubclassForm
    model = Subclass
    template_name = 'subclass_edit.html'
    context_object_name = 'subclass_create'
    success_url = reverse_lazy('subclass_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Gamer.objects.get(id=self.request.user.id)
        post.save()
        return redirect(f'/subclass/{post.id}')


class SubclassUpdate(LoginRequiredMixin, UpdateView):
    form_class = SubclassForm
    model = Subclass
    template_name = 'subclass_edit.html'
    success_url = '/create/'


    def dispatch(self, request, *args, **kwargs):
        author = Subclass.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Редактировать объявление может только его автор")

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Subclass.objects.get(pk=id)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/subclass/' + str(self.kwargs.get('pk')))


class SubclassDelete(LoginRequiredMixin, DeleteView):
    model = Subclass
    template_name = 'subclass_delete.html'
    success_url = reverse_lazy('subclass_list')

    def dispatch(self, request, *args, **kwargs):
        author = Subclass.objects.get(pk=self.kwargs.get('pk')).author.username
        if self.request.user.username == 'admin' or self.request.user.username == author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponse("Удалить объявление может только его автор")


class ResponseList(ListView):
    model = Response
    template_name = 'myresponse.html'
    ordering = '-date_in'
    context_object_name = 'myresponse'

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Response.objects.filter(response_subclass__author=user_id).order_by('-date_in')
        self.filterset = SubclassFilter(self.request.GET, queryset, request=self.request.user.id)
        return self.filterset.qs


    # def get_queryset(self):
    #     queryset = Comment.objects.filter(comment_bill__author=self.request.user).order_by('-date_in')
    #     self.filterset = BillFilter(self.request.GET, queryset, request=self.request.user)
    #     return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# class CommentCreate(LoginRequiredMixin, CreateView):
#     form_class = CommentForm
#     model = Comment
#     template_name = 'respond.html'
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bill_detail'] = Bill.objects.get(pk=self.kwargs['pk']).title
#         return context
#
#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.author = self.request.user
#         comment.comment_bill = Bill.objects.get(id=self.kwargs['pk'])
#         return super().form_valid(form)
#

class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('myresponse')

    def get_object(self, **kwargs):
        my_id = self.kwargs.get('pk')
        return Response.objects.get(pk=my_id)


class CategoryList(SubclassList):
    model = Subclass
    template_name = 'category_list.html'
    context_object_name = 'subclass_cat_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Subclass.objects.filter(category=self.category).order_by('-subclass_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class Respond(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'respond.html'
    form_class = ResponseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        respond = form.save(commit=False)
        respond.author = Gamer.objects.get(id=self.request.user.id)
        respond.response_subclass = Subclass.objects.get(id=self.kwargs.get('pk'))
        respond.save()
        response_send_email.delay(respond.id)
        return redirect(f'/subclass/{self.kwargs.get("pk")}/')


class ConfirmUser(UpdateView):
    model = Gamer
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = Gamer.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'invalid_code.html')
        return redirect('account_login')


# @login_required
# def accept_comment(request, pk):
#     comment = Comment.objects.get(id=pk)
#     comment.accepted = True
#     comment.save()
#     return HttpResponseRedirect(reverse('mycomments'))

@login_required
def accept_response(request, **kwargs):
    if request.user.is_authenticated:
        response = Response.objects.get(id=kwargs.get('pk'))
        response.status = True
        response.save()
        response_accept_send_email.delay(response_subclass_id=response.id)
        return HttpResponseRedirect('/myresponse')
    else:
        return HttpResponseRedirect('/accounts/login')

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return redirect('subclass_cat_list', pk)
