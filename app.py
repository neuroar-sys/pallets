import streamlit as st
from marketplace import PalletsAI, DatabaseManager
import os

# Configuración de la página
st.set_page_config(
    page_title="Marketplace Muebles Pallets BA",
    page_icon="🛋️",
    layout="wide"
)

# Inicializar IA y Base de Datos
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

# Header de la aplicación
st.title("Marketplace de Muebles de Pallets - Buenos Aires")
st.markdown("**Conectamos fabricantes locales con clientes que buscan muebles únicos y ecológicos**")

# Sidebar para navegación
st.sidebar.title("Navegación")
opcion = st.sidebar.radio("Menú principal:", [
    "Inicio", 
    "Registrar Fabricante", 
    "Publicar Producto",
    "Buscar Productos"
])

if opcion == "Inicio":
    st.header("Bienvenido al Marketplace")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Para Clientes")
        st.write("Encuentra muebles únicos de pallets fabricados por artesanos locales")
        
        consulta = st.text_input("¿Qué mueble estás buscando?", 
                               placeholder="Ej: Mesa de living para balcón pequeño...")
        
        if st.button("Buscar recomendaciones"):
            if consulta:
                st.info("Función de búsqueda inteligente en desarrollo...")
                st.write("Por ahora puedes explorar todos los productos en 'Buscar Productos'")
            else:
                st.warning("Por favor, ingresa una búsqueda")
    
    with col2:
        st.subheader("Para Fabricantes")
        st.write("Registra tu taller y muestra tus productos a toda la comunidad")
        
        if st.button("Registrar mi taller"):
            st.session_state.registrar_fabricante = True
            st.rerun()
        
        st.subheader("Estadísticas Rápidas")
        try:
            fabricantes = db.obtener_fabricantes()
            productos = db.obtener_productos()
            st.metric("Fabricantes Registrados", len(fabricantes))
            st.metric("Productos Publicados", len(productos))
        except:
            st.metric("Fabricantes Registrados", 0)
            st.metric("Productos Publicados", 0)

elif opcion == "Registrar Fabricante":
    st.header("Únete como Fabricante")
    
    with st.form("registro_fabricante"):
        st.subheader("Información del Taller")
        
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del taller*")
            localidad = st.selectbox("Localidad*", 
                                   ["Zona Norte", "Zona Sur", "Zona Oeste", "Zona Este", "Capital Federal"])
        with col2:
            telefono = st.text_input("Teléfono de contacto*")
            experiencia = st.slider("Años de experiencia", 0, 50, 2)
        
        st.subheader("Especialidades")
        especialidades = st.multiselect("¿Qué tipo de muebles fabricás?",
                                      ["Sofás y sillones", "Mesas", "Sillas", "Estanterías", 
                                       "Camas", "Muebles de exterior", "Decoración"])
        
        st.subheader("Descripción de tu trabajo")
        descripcion = st.text_area("Contá sobre tu estilo y materiales que usás", height=100,
                                 placeholder="Ej: Especialista en muebles rústicos modernos...")
        
        if st.form_submit_button("Registrar Mi Taller"):
            if nombre and telefono and localidad:
                fabricante_id = db.agregar_fabricante({
                    'nombre': nombre,
                    'localidad': localidad,
                    'telefono': telefono,
                    'especialidad': ', '.join(especialidades),
                    'experiencia': str(experiencia),
                    'descripcion': descripcion
                })
                st.success(f"¡Registro exitoso! Tu ID de fabricante es: {fabricante_id}")
                st.info("Ahora podés publicar tus productos en la sección 'Publicar Producto'")
            else:
                st.error("Por favor, completá los campos obligatorios (*)")

elif opcion == "Publicar Producto":
    st.header("Publicar Nuevo Producto")
    
    # Obtener fabricantes para seleccionar
    fabricantes = db.obtener_fabricantes()
    
    if not fabricantes:
        st.warning("Primero tenés que registrar un fabricante en la sección 'Registrar Fabricante'")
    else:
        with st.form("producto_form"):
            # Seleccionar fabricante
            fabricante_options = {f"{fab[1]}": fab[0] for fab in fabricantes}
            fabricante_seleccionado = st.selectbox("Seleccioná tu taller*", list(fabricante_options.keys()))
            fabricante_id = fabricante_options[fabricante_seleccionado]
            
            nombre = st.text_input("Nombre del producto*", placeholder="Ej: Mesa ratona rústica")
            categoria = st.selectbox("Categoría*", 
                                   ["Living", "Dormitorio", "Comedor", "Exterior", "Oficina", "Decoración"])
            
            col1, col2 = st.columns(2)
            with col1:
                precio = st.number_input("Precio ($)*", min_value=0, value=15000)
                materiales = st.text_input("Materiales principales", placeholder="Pallets de pino, barniz...")
            with col2:
                dimensiones = st.text_input("Dimensiones", placeholder="80x40x50 cm")
            
            descripcion = st.text_area("Descripción del producto", height=100,
                                     placeholder="Describe tu producto o generá una descripción con IA...")
            
            # Generación automática de descripción con IA
            if ia and st.button("Generar descripción con IA"):
                if nombre and categoria and materiales:
                    with st.spinner("Creando descripción atractiva..."):
                        info_producto = f"{nombre}, {categoria}, materiales: {materiales}"
                        descripcion_generada = ia.generar_descripcion(info_producto)
                        st.text_area("Descripción generada", descripcion_generada, height=150, key="desc_generada")
                else:
                    st.warning("Completá al menos nombre, categoría y materiales para generar una descripción")
            
            if st.form_submit_button("Publicar Producto"):
                if nombre and categoria and precio and fabricante_id:
                    # Usar descripción generada si existe, sino la del usuario
                    desc_final = st.session_state.get('desc_generada', descripcion) if 'desc_generada' in st.session_state else descripcion
                    
                    producto_id = db.agregar_producto({
                        'fabricante_id': fabricante_id,
                        'nombre': nombre,
                        'categoria': categoria,
                        'descripcion': desc_final,
                        'precio': precio,
                        'materiales': materiales,
                        'dimensiones': dimensiones
                    })
                    st.success(f"¡Producto publicado exitosamente! ID: {producto_id}")
                    
                    # Limpiar session state
                    if 'desc_generada' in st.session_state:
                        del st.session_state['desc_generada']
                else:
                    st.error("Por favor, completá los campos obligatorios (*)")

elif opcion == "Buscar Productos":
    st.header("Catálogo de Productos")
    
    try:
        productos = db.obtener_productos()
        
        if not productos:
            st.info("Aún no hay productos publicados. ¡Sé el primero en publicar!")
        else:
            st.success(f"Encontramos {len(productos)} productos disponibles")
            
            for producto in productos:
                with st.container():
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    
                    with col1:
                        # Placeholder para imagen - luego podemos agregar imágenes reales
                        st.image("https://via.placeholder.com/150x150/4CAF50/white?text=Mueble", 
                                width=150, caption=producto[2])
                    
                    with col2:
                        st.subheader(producto[2])
                        st.write(f"**Categoría:** {producto[3]}")
                        st.write(f"**Descripción:** {producto[4]}")
                        if producto[6]:  # materiales
                            st.write(f"**Materiales:** {producto[6]}")
                        if producto[7]:  # dimensiones
                            st.write(f"**Dimensiones:** {producto[7]}")
                    
                    with col3:
                        st.write(f"**${producto[5]}**")
                        st.write(f"**Fabricante:** {producto[9]}")
                        st.write(f"**{producto[10]}**")
                        
                        # Botón de contacto
                        if producto[11]:  # teléfono
                            mensaje = f"Hola, me interesa el producto {producto[2]} que vi en Marketplace Pallets"
                            url_whatsapp = f"https://wa.me/54{producto[11]}?text={mensaje}"
                            st.link_button("Contactar por WhatsApp", url_whatsapp)
    except Exception as e:
        st.error(f"Error al cargar productos: {e}")

# Footer
st.markdown("---")
st.markdown("**Muebles Ecológicos  Artesanos Locales  Economía Circular**")