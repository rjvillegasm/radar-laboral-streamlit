import pandas as pd
from pathlib import Path

# ============================================
# CONFIGURACIÓN 
# ============================================
RAW_PATH = Path("raw_data")
PROCESSED_PATH = Path("clean_data")
PROCESSED_PATH.mkdir(exist_ok=True) 

# ============================================
# TRANSFORMACIONES
# ============================================
def limpiar_obras(df):
    """Limpieza para obras públicas"""
    
    
    # Estandarización de fechas 
    # nota: algunas fechas cuantan "/" lo que no permite una conversión directa al formato fecha
    df['F Inicio'] = pd.to_datetime(
        df['F Inicio'].str.replace('/', '-'), 
        format='%d-%m-%Y', 
        errors='coerce'
    )
    df['F Termino'] = pd.to_datetime(
        df['F Termino'].str.replace('/', '-'), 
        format='%d-%m-%Y', 
        errors='coerce'
    )
    
    df.rename(columns={
    'Region':'Región',
    'F Inicio':'Fecha Inicio',
    'F Termino':'Fecha Término',}, inplace=True)
    
    return df

def limpiar_avisos(df):
    """Limpieza para avisos de empleo"""
    
    # Importamos
    avisos_empleo=pd.read_excel("raw_data/02_avisos_empleo_CRUDO.xlsx",
                                header=0, sheet_name=0, 
                                dtype={'Ocupacion CIUO08CL codigo': str})
    
    # limpiamos string de la columna , dejando solo cantidades

    df['N anuncios de empleo web'] = df['N anuncios de empleo web'].str.replace(' avisos', '').astype('Int64')
    
    # Cambio de la columna meses mediante método map
    meses = {
    "ene": "Enero",
    "feb": "Febrero",
    "mar": "Marzo",
    "abr": "Abril",
    "may": "Mayo",
    "jun": "Junio",
    "jul": "Julio",
    "ago": "Agosto",
    "sep": "Septiembre",
    "oct": "Octubre",
    "nov": "Noviembre",
    "dic": "Diciembre"
    }
    df['Mes'] = df['Mes'].map(meses)
    
    # Creamos la columna fecha
    
    df['Fecha'] = pd.to_datetime(
    df['Anio'].astype(str) + '-' + 
    df['Mes'].map({'Enero':'01', 'Febrero':'02', 'Marzo':'03', 'Abril':'04', 
                              'Mayo':'05', 'Junio':'06', 'Julio':'07', 'Agosto':'08',
                              'Septiembre':'09', 'Octubre':'10', 'Noviembre':'11', 'Diciembre':'12'}),
    format='%Y-%m')
    
    # Renombramos columnas 
    df.rename(columns={
    'Region':'Región',
    'Anio':'Año',
    'Ocupacion CIUO08CL codigo': 'Código ocupación',
    'Ocupacion CIUO08CL glosa':'Glosa ocupación',
    
    'N anuncios de empleo web': 'Anuncios',
    'N vacantes de empleo web': 'Vacantes',
    'Remuneracion mediana': 'Remuneración promedio'
    }, inplace=True)
    
    return df

# ============================================
# PIPELINE
# ============================================
def ejecutar_etl():
    """Ejecuta las transformaciones y guarda los datos procesados"""
    
    print("🔄 Iniciando ETL...")
    
    # 1. Cargar y limpiar avisos
    avisos_raw = pd.read_excel(RAW_PATH / "02_avisos_empleo_CRUDO.xlsx", header=0, 
                               sheet_name=0, 
                               dtype={'Ocupacion CIUO08CL codigo': str})
    
    avisos_clean = limpiar_avisos(avisos_raw)
    avisos_clean.to_csv(PROCESSED_PATH / "avisos_clean.csv", index=False)
    print(f"✅ Avisos: {len(avisos_clean)} registros")
    
    # 2. Cargar y limpiar obras públicas
    obras_raw = pd.read_csv(RAW_PATH / "01_obras_publicas_CRUDO.csv",
                              delimiter=';',
                              thousands='.',
                              decimal=',',
                              dtype= {'Monto Vigente Contrato': int},
                              encoding='utf-8')
                            
    obras_clean = limpiar_obras(obras_raw)
    obras_clean.to_csv(PROCESSED_PATH / "obras_clean.csv", index=False)
    print(f"✅ Obras: {len(obras_clean)} registros")
    
    # 3. Cargar datos ya limpios
    
    recomendaciones = pd.read_csv(RAW_PATH / "03_recomendaciones_LIMPIO.csv")
    recomendaciones.to_csv(PROCESSED_PATH / "recomendaciones.csv", index=False)
    print(f"✅ Recomendaciones: {len(recomendaciones)} registros")
    
    cursos = pd.read_csv(RAW_PATH / "04_cursos_disponibles_LIMPIO.csv")
    cursos.to_csv(PROCESSED_PATH / "cursos.csv", index=False)
    print(f"✅ Cursos: {len(cursos)} registros")
    
    print("ETL completado exitosamente")

# ============================================
# EJECUCIÓN DIRECTA
# ============================================
if __name__ == "__main__":
    ejecutar_etl()
