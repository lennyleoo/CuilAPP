from flask import Flask, render_template, request
from cuilCalculator import cuilCalculator

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



if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)
