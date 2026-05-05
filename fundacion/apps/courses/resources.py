from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from apps.enrollments.models import Inscripcion
from .models import Curso

class InscripcionResource(resources.ModelResource):
    course = fields.Field(
        column_name='Curso',
        attribute='curso',
        widget=ForeignKeyWidget(Curso, 'nombre')
    )
    
    class Meta:
        model = Inscripcion
        fields = ('usuario__username', 'usuario__email', 'usuario__telefono', 'course', 'estado', 'fecha_inscripcion')
        export_order = ('usuario__username', 'usuario__email', 'usuario__telefono', 'course', 'estado', 'fecha_inscripcion')