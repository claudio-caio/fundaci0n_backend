from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail

@api_view(['POST'])
def contacto_email(request):
    nombre = request.data.get('nombre')
    email = request.data.get('email')
    mensaje = request.data.get('mensaje')
    numero_documento = request.data.get('numero_documento')
    tipo_consulta = request.data.get('tipo_consulta')

    if not nombre or not email or not mensaje:
        return Response({"error": "Faltan datos"}, status=400)

    send_mail(
        subject=f"Nuevo mensaje de {nombre}",
        message=f"Email: {email}\nNúmero de documento: {numero_documento}\nTipo de consulta: {tipo_consulta}\n\nMensaje:\n{mensaje}",
        from_email='caioalegres@gmail.com',  # mismo que en settings
        recipient_list=['caioalegres@gmail.com'],  # donde querés recibir
    )

    return Response({"ok": "Mensaje enviado correctamente"})
