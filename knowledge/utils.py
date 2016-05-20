from django.conf import settings


def paginate(iterable, per_page, page_num):
    """
        recipes = Recipe.objects.all()
        paginator, recipes = paginate(recipes, 12,
            request.GET.get('page', '1'))
    """
    from django.core.paginator import Paginator, InvalidPage, EmptyPage

    paginator = Paginator(iterable, per_page)

    try:
        page = int(page_num)
    except ValueError:
        page = 1

    try:
        iterable = paginator.page(page)
    except (EmptyPage, InvalidPage):
        iterable = paginator.page(paginator.num_pages)

    return paginator, iterable


def get_module(path):
    """
    A modified duplicate from Django's built in backend
    retriever.

        slugify = get_module('django.template.defaultfilters.slugify')
    """
    try:
        from importlib import import_module
    except ImportError:
        from django.utils.importlib import import_module

    try:
        mod_name, func_name = path.rsplit('.', 1)
        mod = import_module(mod_name)
    except ImportError, e:
        raise ImportError(
            'Error importing alert function {0}: "{1}"'.format(mod_name, e))

    try:
        func = getattr(mod, func_name)
    except AttributeError:
        raise ImportError(
            ('Module "{0}" does not define a "{1}" function'
                            ).format(mod_name, func_name))

    return func


user_model_label = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def user_can_ask_question(user):
    return settings.KNOWLEDGE_ALLOW_QUESTIONS or user.is_staff or user.is_superuser


def get_current_user_questions(request):
    from knowledge.models import Question
    if request.user.is_anonymous():
        return []
    return Question.objects.can_view(request.user).filter(user=request.user)
