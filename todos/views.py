from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo,User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# @login_required
class IndexView(generic.ListView):
    template_name = 'todos/index.html'
    context_object_name = 'todo_list'
 
    def get_queryset(self):
        """Return all the latest todos."""
        # return Todo.objects.order_by('-created_at')
        return Todo.objects.filter(user=self.request.user).order_by('-created_at')

def add(request):
    title = request.POST['title']
    user=request.user
    # Todo.objects.create(title=title)
    Todo.objects.create(title=title,user=user)

    return redirect('todos:index')

def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('todos:index')

def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    isCompleted = request.POST.get('isCompleted', False)
    if isCompleted == 'on':
        isCompleted = True
    
    todo.isCompleted = isCompleted

    todo.save()
    return redirect('todos:index')