from django.apps import AppConfig

class FormFacilConfig(AppConfig):
    name = 'formfacil'

    def ready(self):
        import formfacil.signals