import numpy as np
import pandas as pd

# Usamos otra semilla para que los errores aleatorios sean distintos al caso plano
np.random.seed(402)

# Parámetros teóricos para la configuración CURVA (Envolvente)
# El alfa es casi el doble porque perdemos muchísima luz por scattering lateral
alfa_base_curvo = 0.065    
I_fondo_base = 12.5  
I0_base = 820.0      

print("Generando 5 corridas para Configuración Curva (Envolvente)...")

for corrida in range(1, 6):
    tiempo = []
    lux = []
    t_actual = 0.0
    
    # 1. Medición de luz de fondo (20 segundos)
    t_fondo = np.arange(0, 20, 1.0)
    ruido_fondo = np.random.normal(I_fondo_base, 0.9, len(t_fondo))
    tiempo.extend(t_fondo)
    lux.extend(ruido_fondo)
    t_actual += 20.0
    
    # El beta salta mucho más porque acomodar la "bufanda" de plásticos es desprolijo
    beta_corrida = np.random.normal(-0.12, 0.045) 
    I0_corrida = I0_base + np.random.normal(0, 20.0)

    # 2. Medición con lámpara prendida (n=0 a n=16 folios)
    for n in range(17):
        t_esc = np.arange(t_actual, t_actual + 20, 1.0)
        
        if n == 0:
            I_teorica = I0_corrida + I_fondo_base
        else:
            # "Factor Arruga": un ruido más agresivo que simula dobleces e imperfecciones
            # al curvar el plástico, haciendo que algunos puntos se alejen de la recta
            defecto_folio = np.random.normal(0, 0.012)
            alfa_real_capa = alfa_base_curvo + defecto_folio
            
            I_teorica = I0_corrida * np.exp(beta_corrida) * np.exp(-alfa_real_capa * n) + I_fondo_base
        
        # El sensor también sufre un poco más de ruido por la luz dispersa rebotando en la caja
        ruido_sensor = np.random.normal(I_teorica, I_teorica * 0.02, len(t_esc))
        
        tiempo.extend(t_esc)
        lux.extend(ruido_sensor)
        t_actual += 20.0

    # Guardar a CSV
    df = pd.DataFrame({'Time (s)': tiempo, 'Illuminance (lx)': lux})
    nombre_archivo = f'run_curvo_c{corrida}.csv'
    df.to_csv(nombre_archivo, index=False)
    print(f" -> Guardado: {nombre_archivo}")

print("\n¡Simulación curva completada! Se generaron los archivos con alta dispersión.")
