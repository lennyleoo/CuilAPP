from flask import Flask, render_template, request, send_file, after_this_request

from cuilCalculator import cuilCalculator
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/", methods=['GET', 'POST']) 
def index():
    cuil = None 
    error = None 

    if request.method == "POST":
        if "btnLimpiar" in request.form: 
            cuil = None
            error = None
        else:
            genero = request.form.get("opciones")
            dni = request.form.get("DNI")

            if not genero or not dni:
                error = 'Debe completar todos los datos.'
            elif not dni.isdigit() or len(dni) != 8:
                error = 'El DNI debe contener 8 dígitos numéricos.'
            else:
                calculator = cuilCalculator(dni, genero)

                try:
                    calculator.validateDNI()
                    cuil = calculator.calculate()  
                except Exception as e:
                    error = str(e)

    return render_template("index.html", cuil=cuil, error=error)


import tempfile
import shutil

@app.route("/descargar_cuil/<cuil>")
def descargar_cuil(cuil):
    # Crea el contenido del archivo
    contenido = f"Cuil: {cuil}\n"
    
    # Crea un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        temp_file.write(contenido.encode('utf-8'))
        temp_file_path = temp_file.name  # Guarda la ruta del archivo temporal
    
    # Envía el archivo para su descarga
    response = send_file(temp_file_path, as_attachment=True)
    
    # Elimina el archivo después de enviarlo
    @after_this_request
    def cleanup(response):
        try:
            os.remove(temp_file_path)
        except Exception as e:
            print(f'Error al eliminar el archivo: {e}')
        return response

    return response






if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)
