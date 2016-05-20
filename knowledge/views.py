import settings

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Q

from knowledge.models import Question, Response, Category
from knowledge.forms import QuestionForm, ResponseForm
from knowledge.utils import paginate, user_can_ask_question


ALLOWED_MODS = {
    'question': [
        'private', 'public',
        'delete', 'lock',
        'clear_accepted'
    ],
    'response': [
        'internal', 'inherit',
        'private', 'public',
        'delete', 'accept'
    ]
}


def knowledge_index(request, template='django_knowledge/index.html'):
    if settings.LOGIN_REQUIRED and not request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_URL + "?next=%s" % request.path)

    questions = Question.objects.can_view(request.user)\
                                .prefetch_related('responses__question')[0:20]
    [setattr(q, '_requesting_user', request.user) for q in questions]

    return render(request, template, {
        'request': request,
        'questions': questions,
        'categories': Category.objects.all(),
        'BASE_TEMPLATE': settings.BASE_TEMPLATE,
    })


def knowledge_list(request, category_slug=None,
                   template='django_knowledge/list.html'):

    if settings.LOGIN_REQUIRED and not request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_URL + "?next=%s" % request.path)

    search = request.GET.get('title', None)
    questions = Question.objects.can_view(request.user)\
                                .prefetch_related('responses__question')

    if search:
        questions = questions.filter(
            Q(title__icontains=search) | Q(body__icontains=search)
        )

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        questions = questions.filter(categories=category)

    paginator, questions = paginate(questions, 50, request.GET.get('page', '1'))
    [setattr(q, '_requesting_user', request.user) for q in questions]

    form = None
    if user_can_ask_question(request.user):
        form = QuestionForm(request.user, initial={'title': search})

    return render(request, template, {
        'request': request,
        'search': search,
        'questions': questions,
        'category': category,
        'categories': Category.objects.all(),
        'form': form,
        'BASE_TEMPLATE': settings.BASE_TEMPLATE,
    })


def knowledge_thread(request, question_id, slug=None,
                     template='django_knowledge/thread.html'):

    if settings.LOGIN_REQUIRED and not request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_URL + "?next=%s" % request.path)

    try:
        question = Question.objects.can_view(request.user)\
                                   .get(id=question_id)
    except Question.DoesNotExist:
        if Question.objects.filter(id=question_id).exists() and \
                                hasattr(settings, 'LOGIN_REDIRECT_URL'):
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            raise Http404

    responses = question.get_responses(request.user)

    if request.path != question.get_absolute_url():
        return redirect(question.get_absolute_url(), permanent=True)

    form = ResponseForm(request.user, question, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if request.user.is_authenticated() or not form.cleaned_data['phone_number']:
            form.save()
        return redirect(question.get_absolute_url())

    return render(request, template, {
        'request': request,
        'question': question,
        'responses': responses,
        'allowed_mods': ALLOWED_MODS,
        'form': form,
        'categories': Category.objects.all(),
        'BASE_TEMPLATE': settings.BASE_TEMPLATE,
    })


def knowledge_moderate(
        request,
        lookup_id,
        model,
        mod,
        allowed_mods=ALLOWED_MODS):

    """
    An easy to extend method to moderate questions
    and responses in a vaguely RESTful way.

    Usage:
        /knowledge/moderate/question/1/inherit/     -> 404
        /knowledge/moderate/question/1/public/      -> 200

        /knowledge/moderate/response/3/notreal/     -> 404
        /knowledge/moderate/response/3/inherit/     -> 200

    """
    if request.method != 'POST':
        raise Http404

    if settings.LOGIN_REQUIRED and not request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_URL + "?next=%s" % request.path)

    if model == 'question':
        Model, perm = Question, 'change_question'
    elif model == 'response':
        Model, perm = Response, 'change_response'
    else:
        raise Http404

    if not request.user.has_perm(perm):
        raise Http404

    if mod not in allowed_mods[model]:
        raise Http404

    instance = get_object_or_404(
        Model.objects.can_view(request.user),
        id=lookup_id)

    func = getattr(instance, mod)
    if callable(func):
        func()

    try:
        return redirect((
            instance if instance.is_question else instance.question
        ).get_absolute_url())
    except NoReverseMatch:
        return redirect(reverse('knowledge_index'))


def knowledge_ask(request, template='django_knowledge/ask.html'):

    if not user_can_ask_question(request.user):
        return redirect(reverse('knowledge_index'))

    if settings.LOGIN_REQUIRED and not request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_URL + "?next=%s" % request.path)

    form = QuestionForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if request.user.is_authenticated() or not form.cleaned_data['phone_number']:
            question = form.save()
            return redirect(question.get_absolute_url())
        else:
            return redirect('knowledge_index')

    return render(request, template, {
        'request': request,
        'form': form,
        'categories': Category.objects.all(),
        'BASE_TEMPLATE': settings.BASE_TEMPLATE,
    })
