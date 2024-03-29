from django.apps import AppConfig


class ExerciseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wellbeing_django_framework.exercise'

    def ready(self):
        import wellbeing_django_framework.exercise.signals
