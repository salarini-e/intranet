from django.apps import AppConfig


class FormfacilConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'formfacil'
    #######################################
    def ready(self):
        # Importa os sinais para registrá-los
        import formfacil.signals