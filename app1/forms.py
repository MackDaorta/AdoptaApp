from django import forms
from datetime import date #Importacion de date para validacion de la fecha
from .models import TipoMascota, Mascota, Persona, PostMascota #Importacion de PostMascota

class TipoMascotaForm(forms.ModelForm):
    class Meta:
        model = TipoMascota
        fields = ['nombre', 'descripcion']

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Perro'
            }),
            'descripcion': forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Ej. Mascotas caninas de todas las razas',
                'rows':3
            }) 
        }

        labels = {
            'nombre':'Nombre del tipo',
            'descripcion': 'Descripcion'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or nombre.strip() == '':
            raise forms.ValidationError("El nombre no puede estar vacio")
        if TipoMascota.objects.filter(nombre__iexact=nombre.strip()).exists():
            raise forms.ValidationError("Este tipo de mascota ya existe")
        return nombre.strip()
    
    def clean(self):
        cleaned = super().clean()
        nombre = cleaned.get('nombre')
        descripcion = cleaned.get('descripcion')
        if nombre and descripcion and nombre.strip().lower() == descripcion.strip().lower():
            raise forms.ValidationError("El nombre y la descripcion no pueden ser iguales")
        return cleaned
    
    
    
    
    """
        =========================================================
         SECCIÓN: CREAR EL FORMULARIO PostMascotaForm
         ---------------------------------------------------------
         TODO: Crear el formulario con los campos indicados
        =========================================================
    """
class PostMascotaForm(forms.ModelForm):
    class Meta:
        model = PostMascota

        #Campos obligatorios
        fields = ['titulo','descripcion','fecha','foto']

        #Usando Bootstrap y placehokders 
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Titulo del momento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe una breve historia...',
                'rows': 3
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'foto': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
    #Minimo 20 caracteres para la descripcion
    def clean_descripcion(self):
        descripcion= self.cleaned_data.get('descripcion')
        if descripcion and len(descripcion)<20:
            raise forms.ValidationError('La descripcion debe tener mas de 20 caracteres')
        return descripcion
    
    #Impedir que se creen fechas del futuro
    def clean_fecha(self):
        fecha_post= self.cleaned_data.get('fecha')
        if fecha_post and fecha_post > date.today():
            raise forms.ValidationError('La fecha no puede ser mayor a la actual')
        return fecha_post