import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Balance de Masa | Pulpa de Fruta",
    page_icon="🍇",
    layout="wide",
)

# --- Título y Descripción ---
st.title("Calculadora de Balance de Masa para Pulpa de Fruta 🍇")
st.markdown("""
Esta aplicación web calcula la cantidad de azúcar necesaria para ajustar la concentración de sólidos solubles (grados °Brix) en una pulpa de fruta, basándose en un problema de balance de masa.
""")
st.markdown("---")


# --- Entradas del Usuario en la Barra Lateral ---
st.sidebar.header("Parámetros de Entrada")

# Usamos st.number_input para obtener los valores del usuario
m1 = st.sidebar.number_input(
    "Masa Inicial de Pulpa (M1 en kg)",
    min_value=0.0,
    value=50.0,
    step=1.0,
    help="Introduce la masa inicial de la pulpa que se va a procesar."
)

x1_percent = st.sidebar.number_input(
    "Concentración Inicial de Sólidos (X1 en %)",
    min_value=0.0,
    max_value=100.0,
    value=7.0,
    step=0.1,
    help="Porcentaje de grados °Brix iniciales de la pulpa."
)

x3_percent = st.sidebar.number_input(
    "Concentración Final Deseada (X3 en %)",
    min_value=0.0,
    max_value=100.0,
    value=10.0,
    step=0.1,
    help="Porcentaje de grados °Brix que se desea alcanzar."
)

# --- Cálculos del Balance de Masa ---
# Convertir porcentajes a decimales para los cálculos
x1 = x1_percent / 100.0
x3 = x3_percent / 100.0

# El azúcar (M2) tiene una concentración de sólidos (X2) del 100% (1.0) y 0% de agua (Y2=0.0)
x2 = 1.0
y2 = 0.0

# Calcular la concentración de agua inicial y final
y1 = 1 - x1
y3 = 1 - x3

# Inicializar variables para evitar errores si x3 >= x1
m2 = 0
m3 = m1

# Validar que la concentración final sea mayor que la inicial
if x3 <= x1:
    st.error("Error: La concentración final deseada debe ser mayor que la concentración inicial para poder agregar azúcar.")
else:
    # --- Balance General por componente (Agua) ---
    # M1*Y1 + M2*Y2 = M3*Y3
    # Como Y2 = 0 (el azúcar no tiene agua), la ecuación se simplifica:
    # M1*Y1 = M3*Y3
    # Despejamos M3:
    m3 = (m1 * y1) / y3

    # --- Balance General de Masa ---
    # M1 + M2 = M3
    # Despejamos M2:
    m2 = m3 - m1


# --- Visualización de Resultados ---
st.header("Resultados del Cálculo")
st.markdown(f"Con una masa inicial de **{m1:.2f} kg** de pulpa al **{x1_percent:.1f}%** de °Brix, para llegar al **{x3_percent:.1f}%** de °Brix se necesita:")

st.success(f"**Agregar {m2:.2f} kg de azúcar.**")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Masa de Azúcar a Agregar (M2)", value=f"{m2:.2f} kg")
with col2:
    st.metric(label="Masa Final de la Pulpa (M3)", value=f"{m3:.2f} kg")


# --- Explicación del Proceso (Expandible) ---
with st.expander("Ver la explicación y las ecuaciones del cálculo"):
    st.subheader("Ecuaciones de Balance de Masa")

    st.markdown("""
    Donde:
    - **M1**: Masa de Pulpa Inicial
    - **M2**: Masa de Azúcar a agregar
    - **M3**: Masa de Pulpa Final
    - **X1, X2, X3**: Concentración de Sólidos (azúcar) en cada corriente.
    - **Y1, Y2, Y3**: Concentración de Agua en cada corriente.
    """)

    st.subheader("1. Balance General de Masa Total")
    st.latex("M1 + M2 = M3")

    st.subheader("2. Balance por Componente (Agua)")
    st.markdown("Se realiza un balance para el agua, ya que su cantidad en la pulpa inicial es la misma que en la pulpa final (el azúcar agregado no contiene agua).")
    st.latex("M1 \cdot Y1 + M2 \cdot Y2 = M3 \cdot Y3")
    st.markdown("Como el azúcar es 100% sólidos, su concentración de agua **Y2** es 0. La ecuación se simplifica a:")
    st.latex("M1 \cdot Y1 = M3 \cdot Y3")
    st.markdown("Despejando la Masa Final (**M3**):")
    st.latex(r"M3 = \frac{M1 \cdot Y1}{Y3}")
    # Cálculo de ejemplo
    st.latex(fr"M3 = \frac{{{m1:.2f} \text{{ kg}} \cdot {y1:.2f}}}{{{y3:.2f}}} = {m3:.2f} \text{{ kg}}")


    st.subheader("3. Cálculo del Azúcar a Agregar (M2)")
    st.markdown("Conociendo **M3**, usamos el balance general para encontrar **M2**:")
    st.latex("M2 = M3 - M1")
    st.latex(f"M2 = {m3:.2f} \\text{{ kg}} - {m1:.2f} \\text{{ kg}} = {m2:.2f} \\text{{ kg}}")
