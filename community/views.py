from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from community.forms import CustomRegistrationForm, QuestionForm, QuestionCommentForm, AnswerCommentForm, AnswerForm
from community.models import Question, QuestionComment, Answer, AnswerComment, Tag


def register(request):
    form = CustomRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Added.")

                return redirect('questions')

    return render(request, 'auth/signup.html', {"form": form})


def paginate_objects(request, queryset, num):
    paginator = Paginator(queryset, num)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return queryset


def questions(request):
    queryset = Question.objects.all().order_by('-timestamp')
    tags = Tag.objects.all()[0:10]

    search_request_var = 'q'
    search_query = request.GET.get(search_request_var, '')
    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) |
            Q(tag__title__icontains=search_query)
        ).distinct()

    tag_request_var = 'tag'
    tag_search_query = request.GET.get(tag_request_var, '')
    if tag_search_query != '' and tag_search_query != 'Latest':
        if tag_search_query == 'Active':
            queryset = [obj for obj in queryset if obj.is_active()]
        elif tag_search_query == 'Unanswered':
            queryset = [obj for obj in queryset if not obj.has_answer()]
        else:
            queryset = [obj for obj in queryset if obj.has_answer()]

    queryset = paginate_objects(request, queryset, 10)


    context = {
        "questions": queryset,
        "page_request_var": 'page',
        "search_request_var": search_request_var,
        "search_query": search_query,
        "tag_request_var": tag_request_var,
        "tag_search_query": tag_search_query,
        "tags": tags
    }

    return render(request, 'community/questions.html', context)


def question(request, pk, slug):
    obj = get_object_or_404(Question, id=pk)

    question_comment_form = QuestionCommentForm(request.POST or None)
    answer_comment_form = AnswerCommentForm(request.POST or None)
    answer_form = AnswerForm(request.POST or None)

    context = {
        'question_comment_form': question_comment_form,
        'answer_comment_form': answer_comment_form,
        'answer_form': answer_form,
        'question': obj
    }

    if not request.user.is_authenticated:
        context["login_required"] = "You have to be logged in"

    else:
        if request.method == "POST":
            if "questionComment" in request.POST:
                if question_comment_form.is_valid():
                    question_comment_id = request.POST["question_comment_id"]
                    if question_comment_id != "":
                        # TODO consider scenario if obj not found
                        question_comment = get_object_or_404(QuestionComment, id=int(question_comment_id))
                        if question_comment.user == request.user:
                            question_comment.text = question_comment_form.instance.text
                            question_comment.save()
                        else:
                            context['authority_error'] = "You cannot edit other users' comments!"
                    else:
                        question_comment_form.instance.user = request.user
                        question_comment_form.instance.question = obj
                        question_comment_form.save()

            elif "answer_id" in request.POST:
                if answer_comment_form.is_valid():
                        answer_id = request.POST["answer_id"]
                        # TODO consider scenario if obj not found
                        answer = get_object_or_404(Answer, id=int(answer_id))
                        answer_comment_form.instance.user = request.user
                        answer_comment_form.instance.answer = answer
                        answer_comment_form.save()

            else:
                if answer_form.is_valid():
                    # TODO consider scenario if obj not found
                    if request.user != obj.user:
                        answer_form.instance.user = request.user
                        answer_form.instance.question = obj
                        answer_form.save()
                    else:
                        context["authority_error"] = "You are not permitted to answer to your own questions!"
                  

            return redirect(reverse("question", kwargs={
                'pk': obj.pk,
                'slug': obj.slug
            }))

    return render(request, 'community/question_detail.html', context)
    


def create_question(request):
    form = QuestionForm(request.POST, request.FILES or None)
    context = {"form": form}

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to ask a question."      
    else:
        if request.method == "POST":
            if form.is_valid():
                form.instance.user = request.user
                obj = form.save()
                return redirect(reverse("question", kwargs={
                    'pk': form.instance.pk,
                    'slug': obj.slug
                }))
            else:
                context["error"] = form.errors

    return render(request, 'community/question_create.html', context)


def update_question(request, pk, slug):
    obj = get_object_or_404(Question, id=pk)
    form = QuestionForm(request.POST or None, instance=obj)
    context = {"form": form}

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to request for an update of question."
    elif request.user != obj.user:
        context["authority_error"] = "Bad Request: Question belongs to another user. Thus, you are not " \
                                     "allowed to edit this question."
    else:
        if request.method == "POST":
            if form.is_valid():
                obj = form.save()
                return redirect(reverse("question", kwargs={
                    'pk': form.instance.pk,
                    'slug': obj.slug
                }))
            else:
                context["error"] = form.errors

    return render(request, 'community/question_update.html', context)


def update_answer(request, pk):
    obj = get_object_or_404(Answer, id=pk)
    form = AnswerForm(request.POST or None, instance=obj)
    context = {"form": form}

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in to request for an update of question."
    elif request.user == obj.question.user:
        context["authority_error"] = "Bad Request: You are not allowed to answer to your own questions."
    elif request.user != obj.user:
        context["authority_error"] = "Bad Request: Answer belongs to another user. Thus, you are not " \
                                     "allowed to edit this question."
    else:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect(reverse("question", kwargs={
                    'pk': form.instance.question.pk,
                    'slug': form.instance.question.slug
                }))
            else:
                context["error"] = form.errors

    return render(request, 'community/answer_update.html', context)


def update_answer_comment(request, pk):
    obj = get_object_or_404(AnswerComment, id=pk)
    form = AnswerCommentForm(request.POST or None, instance=obj)
    context = {"form": form}

    if not request.user.is_authenticated:
        context["login_required"] = "Bad Request: You must be logged in first."
    elif request.user != obj.user:
        context["authority_error"] = "Bad Request: Comment belongs to another user. Thus, you are not " \
                                     "allowed to edit this comment."
    else:
        if request.method == "POST":
            if form.is_valid():
                obj.text = form.instance.text
                obj.save()
                return redirect(reverse("question", kwargs={
                    'pk': form.instance.answer.question.pk,
                    'slug': form.instance.answer.question.slug
                }))
            else:
                context["error"] = form.errors

    return render(request, 'community/answer_comment_update.html', context)
