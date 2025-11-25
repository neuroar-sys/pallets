import streamlit as st
from marketplace import PalletsAI, DatabaseManager
import os

# =============================================
# ESTILOS CREATIVOS - TEMA PARA MARKETPLACE DE MUEBLES
# =============================================

def aplicar_estilo_creativo():
    st.markdown("""
    <style>
    :root {
        --primary: #e74c3c;
        --secondary: #f39c12;
        --accent: #27ae60;
        --background: #ecf0f1;
    }
    
    .main {
        background-color: var(--background);
    }
    
    /* Header creativo */
    .creative-header {
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        color: white;
        padding: 30px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    
    /* Tarjetas de productos creativas */
    .creative-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-top: 5px solid var(--primary);
        transition: transform 0.3s ease;
    }
    
    .creative-card:hover {
        transform: translateY(-5px);
    }
    
    /* Botones coloridos */
    .stButton>button {
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 1em;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
    }
    
    /* Badges para categorías */
    .category-badge {
        display: inline-block;
        background: var(--accent);
        color: white;
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 0.8em;
        margin: 2px;
    }
    
    /* Métricas/KPIs */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2c3e50;
    }
    
    /* Input fields mejorados */
    .stTextInput>div>div>input, 
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #bdc3c7;
    }
    
    .stTextInput>div>div>input:focus, 
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(231, 76, 60, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def header_personalizado(titulo, subtitulo=""):
    st.markdown(f"""
    <div class="creative-header">
        <h1 style="margin:0; font-size: 2.5em;">{titulo}</h1>
        <p style="margin:0; font-size: 1.2em; opacity: 0.9;">{subtitulo}</p>
    </div>
    """, unsafe_allow_html=True)

def tarjeta_producto(nombre, precio, descripcion, categoria, materiales="", dimensiones="", fabricante="", telefono=""):
    st.markdown(f"""
    <div class="creative-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <h3 style="margin-top:0; color: #2c3e50; flex: 1;">{nombre}</h3>
            <span class="category-badge">{categoria}</span>
        </div>
        <p style="color: #7f8c8d; margin: 10px 0;">{descripcion}</p>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h4 style="color: #e74c3c; margin:0; font-size: 1.5em;">${precio:,.0f}</h4>
            {f'<a href="https://wa.me/54{telefono}?text=Hola, me interesa el producto {nombre} que vi en Marketplace Pallets" style="background: #25D366; color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-weight: bold;" target="_blank">📲 Contactar</a>' if telefono else '<span style="color: #95a5a6; font-size: 0.9em;">Teléfono no disponible</span>'}
        </div>
        <div style="margin-top: 10px; font-size: 0.9em; color: #95a5a6;">
            {f'<p><strong>Materiales:</strong> {materiales}</p>' if materiales else ''}
            {f'<p><strong>Dimensiones:</strong> {dimensiones}</p>' if dimensiones else ''}
            {f'<p><strong>Fabricante:</strong> {fabricante}</p>' if fabricante else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

def metric_card(titulo, valor, cambio=""):
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin:0; font-size: 0.9em; opacity: 0.8;">{titulo}</h3>
        <h1 style="margin:10px 0; font-size: 2em;">{valor}</h1>
        <p style="margin:0; font-size: 0.8em;">{cambio}</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# APLICAR ESTILOS CREATIVOS
# =============================================

aplicar_estilo_creativo()

# =============================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================

st.set_page_config(
    page_title="Marketplace Muebles Pallets BA",
    page_icon="🛋️",
    layout="wide"
)

# =============================================
# INICIALIZACIÓN DE IA Y BASE DE DATOS
# =============================================

@st.cache_resource
def init_ia():
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        st.error("GOOGLE_AI_API_KEY no configurada")
        st.info("Agrega tu API key en Streamlit Cloud: Settings -> Secrets")
        return None
    return PalletsAI(api_key)

@st.cache_resource
def init_db():
    return DatabaseManager()

ia = init_ia()
db = init_db()

# =============================================
# HEADER PRINCIPAL DE LA APLICACIÓN
# =============================================

header_personalizado(
    "🛋️ Marketplace de Muebles de Pallets - Buenos Aires",
    "Conectamos fabricantes locales con clientes que buscan muebles únicos y ecológicos"
)

# =============================================
# SIDEBAR PARA NAVEGACIÓN
# =============================================

st.sidebar.title("🌐 Navegación")
opcion = st.sidebar.radio("Menú principal:", [
    "🏠 Inicio", 
    "👨‍🏭 Registrar Fabricante", 
    "📦 Publicar Producto",
    "🔍 Buscar Productos"
])

# =============================================
# SECCIÓN: INICIO
# =============================================

if opcion == "🏠 Inicio":
    st.header("🌟 Bienvenido al Marketplace")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Para Clientes")
        st.write("Encuentra muebles únicos de pallets fabricados por artesanos locales.")
        
        consulta = st.text_input("🔍 ¿Qué mueble estás buscando?", 
                               placeholder="Ej: Mesa de living para balcón pequeño...")
        
        if st.button("🚀 Buscar recomendaciones"):
            if consulta:
                st.info("Búsqueda inteligente en desarrollo.")
                st.write("Por ahora puedes explorar todos los productos en 'Buscar Productos'.")
            else:
                st.warning("Por favor, ingresa una búsqueda.")
    
    with col2:
        st.subheader("🛠️ Para Fabricantes")
        st.write("Registra tu taller y muestra tus productos a toda la comunidad.")
        
        if st.button("📝 Registrar mi taller"):
            st.session_state.registrar_fabricante = True
            st.rerun()
        
        st.subheader("📊 Estadísticas rápidas")
        try:
            fabricantes = db.obtener_fabricantes()
            productos = db.obtener_productos()
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                metric_card("Fabricantes", len(fabricantes))
            with k2:
                metric_card("Productos", len(productos))
            with k3:
                metric_card("Rating", "4.8★")
            with k4:
                metric_card("Ecológicos", "100%")
        except Exception:
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                metric_card("Fabricantes", "0")
            with k2:
                metric_card("Productos", "0")
            with k3:
                metric_card("Rating", "5.0★")
            with k4:
                metric_card("Ecológicos", "100%")

# =============================================
# SECCIÓN: REGISTRAR FABRICANTE
# =============================================

elif opcion == "👨‍🏭 Registrar Fabricante":
    st.header("🎯 Únete como Fabricante")
    
    with st.form("registro_fabricante"):
        st.subheader("📋 Información del taller")
        
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("🏷️ Nombre del taller*")
            localidad = st.selectbox("📍 Localidad*", 
                                   ["Zona Norte", "Zona Sur", "Zona Oeste", "Zona Este", "Capital Federal"])
        with col2:
            telefono = st.text_input("📞 Teléfono de contacto*")
            experiencia = st.slider("🎓 Años de experiencia", 0, 50, 2)
        
        st.subheader("🛠️ Especialidades")
        especialidades = st.multiselect("¿Qué tipo de muebles fabricás?",
                                      ["Sofás y sillones", "Mesas", "Sillas", "Estanterías", 
                                       "Camas", "Muebles de exterior", "Decoración"])
        
        st.subheader("📝 Descripción de tu trabajo")
        descripcion = st.text_area("Contá sobre tu estilo y materiales que usás", height=100,
                                 placeholder="Ej: Especialista en muebles rústicos modernos...")
        
        submitted = st.form_submit_button("🚀 Registrar Mi Taller")
        if submitted:
            if nombre and telefono and localidad:
                fabricante_id = db.agregar_fabricante({
                    'nombre': nombre,
                    'localidad': localidad,
                    'telefono': telefono,
                    'especialidad': ', '.join(especialidades),
                    'experiencia': str(experiencia),
                    'descripcion': descripcion
                })
                if fabricante_id:
                    st.success(f"¡Registro exitoso! Tu ID de fabricante es: {fabricante_id}")
                    st.info("Ahora podés publicar tus productos en la sección 'Publicar Producto'.")
                else:
                    st.error("No se pudo registrar el fabricante. Intenta nuevamente.")
            else:
                st.error("Por favor, completá los campos obligatorios (*)")

# =============================================
# SECCIÓN: PUBLICAR PRODUCTO
# =============================================

elif opcion == "📦 Publicar Producto":
    st.header("📦 Publicar Nuevo Producto")
    
    fabricantes = db.obtener_fabricantes()
    
    if not fabricantes:
        st.warning("⚠️ Primero tenés que registrar un fabricante en la sección 'Registrar Fabricante'.")
    else:
        with st.form("producto_form"):
            fabricante_options = {f"{fab[1]}": fab[0] for fab in fabricantes}
            fabricante_seleccionado = st.selectbox("🏭 Seleccioná tu taller*", list(fabricante_options.keys()))
            fabricante_id = fabricante_options[fabricante_seleccionado]
            
            nombre = st.text_input("🏷️ Nombre del producto*", placeholder="Ej: Mesa ratona rústica")
            categoria = st.selectbox("📂 Categoría*", 
                                   ["Living", "Dormitorio", "Comedor", "Exterior", "Oficina", "Decoración"])
            
            col1, col2 = st.columns(2)
            with col1:
                precio = st.number_input("💰 Precio ($)*", min_value=0, value=15000)
                materiales = st.text_input("🪵 Materiales principales", placeholder="Pallets de pino, barniz...")
            with col2:
                dimensiones = st.text_input("📏 Dimensiones", placeholder="80x40x50 cm")
            
            descripcion = st.text_area("📝 Descripción del producto", height=100,
                                     placeholder="Describe tu producto...")
            
            col_gen, col_pub = st.columns(2)
            with col_gen:
                generar_desc = st.form_submit_button("🤖 Generar descripción con IA")
            with col_pub:
                publicar = st.form_submit_button("🚀 Publicar Producto")
            
            if ia and generar_desc:
                if nombre and categoria and materiales:
                    with st.spinner("🤖 Creando descripción atractiva..."):
                        info_producto = f"{nombre}, {categoria}, materiales: {materiales}"
                        descripcion_generada = ia.generar_descripcion(info_producto)
                        st.session_state['desc_generada'] = descripcion_generada
                        st.text_area("📄 Descripción generada", descripcion_generada, height=150, key="desc_generada_area")
                else:
                    st.warning("Completá al menos nombre, categoría y materiales para generar una descripción.")
            
            if publicar:
                if nombre and categoria and precio and fabricante_id:
                    desc_final = st.session_state.get('desc_generada', descripcion)
                    
                    producto_id = db.agregar_producto({
                        'fabricante_id': fabricante_id,
                        'nombre': nombre,
                        'categoria': categoria,
                        'descripcion': desc_final,
                        'precio': precio,
                        'materiales': materiales,
                        'dimensiones': dimensiones
                    })
                    if producto_id:
                        st.success(f"¡Producto publicado exitosamente! ID: {producto_id}")
                        if 'desc_generada' in st.session_state:
                            del st.session_state['desc_generada']
                    else:
                        st.error("No se pudo publicar el producto. Intenta nuevamente.")
                else:
                    st.error("Por favor, completá los campos obligatorios (*)")

# =============================================
# SECCIÓN: BUSCAR PRODUCTOS
# =============================================

elif opcion == "🔍 Buscar Productos":
    st.header("📦 Catálogo de Productos")
    
    try:
        productos = db.obtener_productos()
        
        if not productos:
            st.info("ℹ️ Aún no hay productos publicados. ¡Sé el primero en publicar!")
        else:
            st.success(f"🎉 Encontramos {len(productos)} productos disponibles")
            
            # Filtros de búsqueda
            col1, col2, col3 = st.columns(3)
            with col1:
                categorias = list(set([p[3] for p in productos]))
                categoria_filtro = st.selectbox("Filtrar por categoría", ["Todas"] + categorias)
            with col2:
                localidades = list(set([p[10] for p in productos if len(p) > 10]))
                localidad_filtro = st.selectbox("Filtrar por localidad", ["Todas"] + localidades)
            with col3:
                precio_max = max([p[5] for p in productos]) if productos else 100000
                precio_filtro = st.slider("Precio máximo", 0, precio_max, precio_max)
            
            # Aplicar filtros
            productos_filtrados = productos
            if categoria_filtro != "Todas":
                productos_filtrados = [p for p in productos_filtrados if p[3] == categoria_filtro]
            if localidad_filtro != "Todas":
                productos_filtrados = [p for p in productos_filtrados if len(p) > 10 and p[10] == localidad_filtro]
            productos_filtrados = [p for p in productos_filtrados if p[5] <= precio_filtro]
            
            st.write(f"**Mostrando {len(productos_filtrados)} productos**")
            
            for producto in productos_filtrados:
                tarjeta_producto(
                    nombre=producto[2],
                    precio=producto[5],
                    descripcion=producto[4],
                    categoria=producto[3],
                    materiales=producto[6] if len(producto) > 6 else "",
                    dimensiones=producto[7] if len(producto) > 7 else "",
                    fabricante=producto[9] if len(producto) > 9 else "",
                    telefono=producto[11] if len(producto) > 11 else ""
                )
                
    except Exception as e:
        st.error(f"❌ Error al cargar productos: {e}")

# =============================================
# FOOTER
# =============================================

st.markdown("---")
st.markdown("**🌱 Muebles Ecológicos · 👨‍🏭 Artesanos Locales · 🔄 Economía Circular**")
st.markdown("*Marketplace Pallets BA - Conectando talento local con clientes conscientes*")