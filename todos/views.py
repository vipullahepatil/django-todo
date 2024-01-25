from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse


@login_required
def send_notification_email(request, todo_id):
    print("in email send func")
    todo = get_object_or_404(Todo, id=todo_id)

    user_email = request.user.username

    subject = "Todo Notification"
    message = f'Hello {request.user.username},\n\nYour todo "{todo.title}" has reached its notification time.'
    from_email = "testnet@akgroup.co.in"
    recipient_list = [user_email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        return JsonResponse({"status": "success", "message": "Email sent successfully"})
    except Exception as e:
        print("error:", e)
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@login_required
def add(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        deadline = request.POST.get("deadline", None)
        notification_time = request.POST.get("notification_time", None)
        user = request.user

        Todo.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            notification_time=notification_time,
            user=user,
        )

        return redirect("todos:index")

    return render(request, "todos/add.html")


class IndexView(generic.ListView):
    template_name = "todos/index.html"
    context_object_name = "todo_list"

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by("-created_at")


@login_required
def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        deadline = request.POST.get("deadline", None)
        notification_time = request.POST.get("notification_time", None)
        isCompleted = request.POST.get("isCompleted", False)

        if isCompleted == "on":
            isCompleted = True
        else:
            isCompleted = False

        todo.title = title
        todo.description = description
        todo.deadline = deadline
        todo.notification_time = notification_time
        todo.isCompleted = isCompleted

        todo.save()
        return redirect("todos:index")

    return render(request, "todos/update.html", {"todo": todo})


def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect("todos:index")
