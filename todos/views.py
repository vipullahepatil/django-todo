from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo
from django.contrib.auth.decorators import login_required


@login_required
def add(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST.get('deadline', None)
        notification_time = request.POST.get('notification_time', None)
        user = request.user

        Todo.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            notification_time=notification_time,
            user=user
        )

        return redirect('todos:index')

    return render(request, 'todos/add.html')

class IndexView(generic.ListView):
    template_name = 'todos/index.html'
    context_object_name = 'todo_list'
    
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('-created_at')


@login_required
def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)

    if request.method == 'POST': 
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST.get('deadline', None)
        notification_time = request.POST.get('notification_time', None)
        isCompleted = request.POST.get('isCompleted', False)

        if isCompleted == 'on':
            isCompleted = True
        else:
            isCompleted = False

        todo.title = title
        todo.description = description
        todo.deadline = deadline
        todo.notification_time = notification_time
        todo.isCompleted = isCompleted

        todo.save()

    return redirect('todos:index')


def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('todos:index')
