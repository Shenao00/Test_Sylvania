# app.py
from flask import Flask, render_template, request, jsonify
from tu_codigo import Carga, Productos, Panel, Bateria, MPPT  # Asegúrate de importar correctamente tu código

app = Flask(__name__)

# Ruta principal para mostrar el formulario
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar los datos y mostrar resultados
@app.route('/calcular', methods=['POST'])
def calcular():
    # Recibe datos del formulario
    p_luminaria = int(request.form['p_luminaria'])
    eficacia = int(request.form['eficacia'])
    autonomia = int(request.form['autonomia'])
    ba_tip = request.form['ba_tip']
    
    # Crear instancia de Productos y agregar componentes
    productos = Productos()
    # Agregar Paneles
    productos.agregar_panel(Panel(165, 19.21))
    productos.agregar_panel(Panel(450, 41.65))
    productos.agregar_panel(Panel(540, 41.65))
    productos.agregar_panel(Panel(580, 42.71))  # Asegúrate de agregar todos
    productos.agregar_panel(Panel(610, 39.73))
    
    # Agregar Baterías
    productos.agregar_bateria(Bateria("Litio", 36, 12.8))
    productos.agregar_bateria(Bateria("Litio", 50, 12.8))
    productos.agregar_bateria(Bateria("Litio", 75, 12.8))
    productos.agregar_bateria(Bateria("Gel", 150, 12))
    productos.agregar_bateria(Bateria("Gel", 200, 12))
    productos.agregar_bateria(Bateria("Gel", 250, 12))
    
    # Agregar MPPTs
    productos.agregar_MPPT(MPPT("SC160", 200, 400, 80, 160))
    productos.agregar_MPPT(MPPT("SC200", 260, 520, 100, 200))
    productos.agregar_MPPT(MPPT("SC260", 400, 800, 130, 260))
    productos.agregar_MPPT(MPPT("SC300", 550, 1100, 150, 300))
    
    # Crear instancia de Carga y calcular panel, batería, y MPPT
    carga = Carga(p_luminaria, eficacia, autonomia, ba_tip, productos)
    resultado_panel = carga.calculo_Panel()
    resultado_bateria = carga.calculo_Bateria()
    resultado_mppt = carga.calculo_MPPT()
    
    # Retorna los resultados en formato JSON para ser manejados en la página
    return jsonify({
        'opciones_paneles': resultado_panel['todas_opciones'],
        'mejor_panel': resultado_panel['mejor_opcion'],
        'opciones_baterias': resultado_bateria['todas_opciones'],
        'mejor_bateria': resultado_bateria['mejor_opcion'],
        'opciones_mppt': resultado_mppt['todas_opciones'],
        'mejor_mppt': resultado_mppt['mejor_opcion']
    })

if __name__ == '__main__':
    app.run(debug=True)
