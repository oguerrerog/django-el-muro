from django.db import models
import re

# Validador Registro Usuarios
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['name']) < 2:
            errors['firstname_len'] = "nombre debe tener al menos 2 caracteres de largo";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['name']):
            errors['solo_letras'] = "solo letras en nombreporfavor"

        if len(postData['password']) < 4:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors


# Modelo Usuarios
class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=CHOICES)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"



# Validador Mensajes
class MensajeManager(models.Manager):
    def validador_mensaje(self, postData):

        errors = {}
        
        if len(postData['mensaje']) < 2:
            errors['mensaje'] = "El mensaje debe tener al menos 2 caracteres de largo";
        
        return errors

# Modelo Mensaje
class Mensaje(models.Model):
    mensaje = models.CharField(max_length=255)
    date = models.DateTimeField(null=True)
    user = models.ForeignKey(User, related_name="mensaje_user", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = MensajeManager()

    def __str__(self):
        return f"{self.mensaje}"

    def __repr__(self):
        return f"{self.mensaje}"


# Validador Comentarios
class ComentarioManager(models.Manager):
    def validador_comentario(self, postData):
        
        errors = {}
        
        if len(postData['comentario']) < 2:
            errors['comentario'] = "El comentario debe tener al menos 2 caracteres de largo";
        
        return errors

class Comentario(models.Model):
    comentario = models.CharField(max_length=255)
    mensaje = models.ForeignKey(Mensaje, related_name="comentarios_mensaje", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="comentarios_user", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = ComentarioManager()

    def __str__(self):
        return f"{self.comentario}"

    def __repr__(self):
        return f"{self.comentario}"