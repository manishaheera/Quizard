from django.urls import path
from . import views

urlpatterns = [
    # LOGIN FUNCTIONS
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    # HOME PAGE FUNCTIONS
    path('quizard', views.dashboard),
    path('quizard/sort_category', views.sort_category),


    # PROFILE PAGE FUNCTIONS
    path('quizard/user/<str:username>', views.user_page),

    # DELETE ONCE PROJECT IS MERGED! PLACEHOLDER TO VIEW ALL QUIZZES UNTIL USER PAGE IS RUNNING
    path('quizard/user/<str:username>/quizzes', views.user_quizzes),
    # ^^^^^^^^^^

    path('quizard/user/<str:username>/update', views.update_user),
    path('quizard/user/<str:username>/destroy', views.delete_account),


    # QUIZZES FUNCTIONS
    path('quizard/quizzes/new', views.quiz_form),
    path('quizard/quizzes/create', views.create_quiz),
    path('quizard/quizzes/<int:quiz_id>', views.view_quiz),
    path('quizard/quizzes/<int:quiz_id>/like', views.like_quiz),
    path('quizard/quizzes/<int:quiz_id>/dislike', views.dislike_quiz),
    path('quizard/quizzes/<int:quiz_id>/edit', views.edit_quiz),
    path('quizard/quizzes/<int:quiz_id>/update', views.update_quiz),
    path('quizard/quizzes/<int:quiz_id>/destroy', views.delete_quiz),
    path('quizard/quizzes/<int:quiz_id>/take_quiz',views.take_quiz),
    path('quizard/quizzes/<int:quiz_id>/mark_quiz',views.mark_quiz),

    # FLASHCARDS
    path('quizard/quizzes/<int:quiz_id>/flashcard/new', views.create_flashcard),
    path('quizard/quizzes/<int:quiz_id>/flashcard/<int:flashcard_id>/edit', views.edit_flashcard),
    path('quizard/quizzes/<int:quiz_id>/flashcard/<int:flashcard_id>/update', views.update_flashcard),
    path('quizard/quizzes/<int:quiz_id>/flashcard/<int:flashcard_id>/destroy', views.delete_flashcard)
]