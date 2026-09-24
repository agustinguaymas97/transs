import numpy as np
import pandas as pd

# Semilla para que los datos sean reproducibles si volvés a correr el script
np.random.seed(104)

# Parámetros teóricos base para la configuración PLANA
alfa_base = 0.038    # Coeficiente de atenuación longitudinal base
I_fondo_base = 12.5  # Luz parásita que entra a la caja (lux)
I0_base = 820.0      # Intensidad de tu lámpara LED (lux)

print("Generando 5 corridas para Configuración Directa (Plana)...")

for corrida in range(1, 6):
    tiempo = []
    lux = []
    t_actual = 0.0
    
    # 1. Medición de luz de fondo (Lámpara apagada, 20 segundos)
    t_fondo = np.arange(0, 20, 1.0)
    ruido_fondo = np.random.normal(I_fondo_base, 0.8, len(t_fondo))
    tiempo.extend(t_fondo)
    lux.extend(ruido_fondo)
    t_actual += 20.0
    
    # Cada vez que acomodás el celular, el beta y el I0 cambian un poquito
    beta_corrida = np.random.normal(-0.06, 0.02) 
    I0_corrida = I0_base + np.random.normal(0, 15.0)

    # 2. Medición con lámpara prendida (n=0 a n=16 folios)
    for n in range(17):
        t_esc = np.arange(t_actual, t_actual + 20, 1.0)
        
        if n == 0:
            # Sin folios, no aplica beta ni alfa todavía
            I_teorica = I0_corrida + I_fondo_base
        else:
            # Defectos de fábrica: cada folio suma o resta un poquito de atenuación
            defecto_folio = np.random.normal(0, 0.004)
            alfa_real_capa = alfa_base + defecto_folio
            
            # Modelo fenomenológico: I = I0 * e^beta * e^(-alfa * n) + Fondo
            I_teorica = I0_corrida * np.exp(beta_corrida) * np.exp(-alfa_real_capa * n) + I_fondo_base
        
        # El sensor del celular oscila (ruido de lectura de alta frecuencia)
        ruido_sensor = np.random.normal(I_teorica, I_teorica * 0.015, len(t_esc))
        
        tiempo.extend(t_esc)
        lux.extend(ruido_sensor)
        t_actual += 20.0

    # Guardar a CSV
    df = pd.DataFrame({'Time (s)': tiempo, 'Illuminance (lx)': lux})
    nombre_archivo = f'run_plano_c{corrida}.csv'
    df.to_csv(nombre_archivo, index=False)
    print(f" -> Guardado: {nombre_archivo}")

print("\n¡Simulación completada! Tenés los datos sucios y listos para procesar.")
