# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from knowledge.utils import user_can_ask_question, get_current_user_questions


def common(request):

    return {
        'my_questions': get_current_user_questions(request),
        'can_ask_questions': user_can_ask_question(request.user),
    }
