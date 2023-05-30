from .models import *
from .forms import *
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.http import Http404


# Create your views here.
class IndexView(TemplateView):
    template_name = 'todo/index.html'


class ToDoCreateView(LoginRequiredMixin, CreateView):
    form_class = TodoForm
    template_name = 'todo/todo_create.html'
    success_url = '/todo-list/'

    def form_valid(self, form):
        # Set the current user as the owner of the todo item
        form.instance.user = self.request.user
        messages.success(self.request, 'Todo item created successfully.')
        return super().form_valid(form)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Store the requested path in the session
            self.request.session['next'] = self.request.get_full_path()

            # Redirect to the login page
            return super().handle_no_permission()

        # If the user is authenticated but doesn't have permission, return a 403 Forbidden response
        return super().handle_no_permission()
    

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    context_object_name = 'todos'
    login_url = reverse_lazy('login')  # Specify your login URL

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        status = self.request.GET.get('status')
        q = self.request.GET.get('q')

        if status:
            queryset = queryset.filter(status=status)

        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))

        return queryset
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Store the requested path in the session
            self.request.session['next'] = self.request.get_full_path()

            # Redirect to the login page
            return super().handle_no_permission()

        # If the user is authenticated but doesn't have permission, return a 403 Forbidden response
        return super().handle_no_permission()


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todo/todo_update.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)  # Filter todos by the logged-in user
        return queryset

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()

            # Check if the user owns the todo item being accessed
            if self.object.user != self.request.user:
                messages.error(request, 'You are not allowed to access this todo item.')
                return redirect('todo_list')

            return super().get(request, *args, **kwargs)

        except Http404:
            messages.error(request, 'Todo item not found.')
            return redirect('todo_list')

    def form_valid(self, form):
        # Check if the user owns the todo item being updated
        if form.instance.user != self.request.user:
            messages.error(self.request, 'You are not allowed to update this todo item.')
            return redirect('todo_list')

        messages.success(self.request, 'Todo item updated successfully.')
        return super().form_valid(form)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            self.request.session['next'] = self.request.get_full_path()
            return super().handle_no_permission()
        messages.error(self.request, 'You are not allowed to update this todo item.')
        return redirect('todo_list')

    def get_success_url(self):
        return reverse('todo_list')
    

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'
    login_url = reverse_lazy('login')  # Specify your login URL

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Todo item deleted successfully.')
        return super().delete(request, *args, **kwargs)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Store the requested path in the session
            self.request.session['next'] = self.request.get_full_path()

            # Redirect to the login page
            return super().handle_no_permission()

        # If the user is authenticated but doesn't have permission, return a 403 Forbidden response
        return super().handle_no_permission()
    
    def get_success_url(self):
        return reverse('todo_list')
    
