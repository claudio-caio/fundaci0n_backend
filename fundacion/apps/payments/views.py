import mercadopago

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.courses.models import Curso
from apps.payments.models import Payment
from apps.enrollments.models import Inscripcion
from apps.users.models import User

# 🔐 (activar en producción real si configurás el secret)
from .utils import verify_signature


# =========================
# 🔹 CREAR PAGO
# =========================
class CreatePaymentView(APIView):

    def post(self, request):
        course_id = request.data.get("course_id")

        try:
            course = Curso.objects.get(id=course_id)
        except Curso.DoesNotExist:
            return Response({"error": "Curso no encontrado"}, status=404)

        if not request.user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=401)

        # Evitar doble inscripción
        if Inscripcion.objects.filter(usuario=request.user, curso=course).exists():
            return Response({"message": "Ya estás inscripto"}, status=200)

        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

        preference_data = {
            "items": [
                {
                    "title": course.nombre,
                    "quantity": 1,
                    "unit_price": float(course.precio),
                }
            ],
            "metadata": {
                "user_id": request.user.id,
                "course_id": course.id
            },
            "back_urls": {
                "success": "https://fundacion-frontend.caioalegres.workers.dev/",
                "failure": "https://fundacion-frontend.caioalegres.workers.dev/capacitaciones",
                "pending": "https://fundacion-frontend.caioalegres.workers.dev/capacitaciones"
            },
            "notification_url": "https://fundaci0n-backend-63ij.onrender.com/api/payments/webhook/"
        }

        response = sdk.preference().create(preference_data)

        if response.get("status") != 201:
            return Response({"error": "Error creando pago"}, status=400)

        pref = response["response"]

        return Response({
            "init_point": pref["init_point"]
        })


# =========================
# 🔥 WEBHOOK
# =========================
@method_decorator(csrf_exempt, name="dispatch")
class MercadoPagoWebhook(APIView):

    def post(self, request):

        print("🔥 WEBHOOK RECIBIDO")
        print("HEADERS:", request.headers)
        print("DATA:", request.data)

        # 🔥 FILTRAR SOLO EVENTOS DE PAGO
        topic = request.query_params.get("topic") or request.data.get("type")

        if topic != "payment":
            print("⛔ Evento ignorado:", topic)
            return Response({"status": "ignored"})

        # 🔐 ACTIVAR SOLO EN PRODUCCIÓN SEGURA
        # if not verify_signature(request):
        #     return Response({"error": "firma inválida"}, status=403)

        # 🔹 Obtener payment_id
        payment_id = (
            request.query_params.get("id")
            or request.data.get("data", {}).get("id")
        )

        if not payment_id:
            return Response({"error": "sin payment_id"}, status=400)

        # 🔥 EVITAR PROCESAR DUPLICADOS
        if Payment.objects.filter(payment_id=payment_id).exists():
            print("⚠️ Pago ya procesado")
            return Response({"status": "already processed"})

        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

        payment_response = sdk.payment().get(payment_id)

        if payment_response.get("status") != 200:
            print("⛔ Error obteniendo pago:", payment_response)
            return Response({"error": "payment not found"}, status=400)

        payment = payment_response["response"]

        print("🔥 PAYMENT:", payment)

        # 🔹 Validar estado del pago
        if payment.get("status") not in ["approved", "authorized"]:
            return Response({"status": "not approved"})

        metadata = payment.get("metadata", {})
        user_id = metadata.get("user_id")
        course_id = metadata.get("course_id")

        try:
            user = User.objects.get(id=user_id)
            course = Curso.objects.get(id=course_id)
        except:
            return Response({"error": "datos inválidos"}, status=400)

        # 🔹 Guardar pago
        Payment.objects.get_or_create(
            payment_id=payment_id,
            defaults={
                "user": user,
                "course": course,
                "status": "approved"
            }
        )

        # 🔹 Inscripción automática
        Inscripcion.objects.get_or_create(
            usuario=user,
            curso=course
        )

        return Response({"status": "ok"})


# =========================
# 🔹 CONSULTA ESTADO
# =========================
class PaymentStatusView(APIView):

    def get(self, request, payment_id):

        try:
            payment = Payment.objects.get(payment_id=payment_id)

            return Response({
                "status": payment.status
            })

        except Payment.DoesNotExist:
            return Response({"status": "not_found"}, status=404)