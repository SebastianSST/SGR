# SGR - Sistema Integral de Gestión de Restaurante

Aplicación web Django para gestionar pedidos, reservas, administración de menús, control de caja y generación de reportes.

## 🎯 Características Principales

### 🔐 Módulo de Autenticación
- **Sistema de usuarios con tres roles:**
  - 🧑 **Cliente:** Puede ver menú, hacer pedidos, hacer reservas y ver su historial
  - 🍽 **Mesero:** Puede tomar pedidos, gestionar estado de órdenes, confirmar reservas y acceder a caja
  - 👨‍💼 **Administrador:** Acceso completo a todos los módulos, administración general y panel Django admin

### 📋 Módulo de Menú Digital
- **CRUD completo** para categorías y platos
- **Sistema de búsqueda** y filtrado por categorías
- **Gestión de imágenes** para platos y categorías
- **Control de disponibilidad** de platos
- **Tiempo de preparación** por plato

### 🛒 Módulo de Pedidos
- **Creación de pedidos** con múltiples platos
- **Seguimiento en tiempo real** con estados:
  - 🟡 Pendiente
  - 🔵 Confirmado
  - 🟠 Preparando
  - 🟢 Listo
  - ✅ Entregado
  - ❌ Cancelado
- **Asignación de meseros** a pedidos
- **Cálculo automático** de totales
- **Vista de cocina** para gestión de preparación

### 📅 Módulo de Reservas
- **Sistema de reservas** por fecha y hora
- **Validación automática** de horarios de atención (10 AM - 10 PM)
- **Gestión de mesas** con capacidad y ubicación
- **Calendario integrado** para visualización de reservas
- **Estados de reserva:** Pendiente, Confirmada, Completada, Cancelada

### 💰 Módulo de Caja
- **Apertura y cierre** de caja con montos iniciales
- **Registro de ventas** por método de pago:
  - 💵 Efectivo
  - 💳 Tarjeta
  - 🏦 Transferencia
- **Reportes diarios automáticos** con:
  - Total de órdenes del día
  - Total de ventas por método
  - Total de reservas y completadas
- **Exportación de datos** a CSV

## 🏗️ Arquitectura y Tecnología

### Backend
- **Framework:** Django 4.2.7
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción recomendada)
- **Autenticación:** Modelo de usuario personalizado
- **API REST:** Lista para futura expansión

### Frontend
- **Framework CSS:** Bootstrap 5.1.3
- **Iconos:** Font Awesome 6.0.0
- **JavaScript:** Vanilla JS con Bootstrap
- **Diseño:** Responsive y moderno
- **Templates:** Sistema de herencia con base.html

### Seguridad
- **Protección CSRF** configurada
- **Validación de contraseñas** robusta
- **Roles y permisos** diferenciados
- **Cookies seguras** con configuración HTTPONLY

## 📦 Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes Python)
- Git para control de versiones

### Pasos de Instalación

1. **Clonar el repositorio:**
   `ash
   git clone https://github.com/SebastianSST/SGR.git
   cd SGR
   `

2. **Crear entorno virtual:**
   `ash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   `

3. **Instalar dependencias:**
   `ash
   pip install -r requirements.txt
   `

4. **Configurar base de datos:**
   `ash
   python manage.py makemigrations
   python manage.py migrate
   `

5. **Crear superusuario:**
   `ash
   python manage.py createsuperuser
   `

6. **Iniciar servidor:**
   `ash
   python manage.py runserver
   `

### Acceso Rápido
- **Aplicación:** http://127.0.0.1:8000/
- **Panel Admin:** http://127.0.0.1:8000/admin/


## 📁 Estructura del Proyecto

```text
SGR/
├── manage.py                    # Script de administración Django
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Documentación del proyecto
├── SGR/                         # Configuración principal
│   ├── __init__.py
│   ├── settings.py              # Configuración de Django
│   ├── urls.py                  # URLs principales
│   ├── wsgi.py                  # Servidor WSGI
│   └── asgi.py                  # Servidor ASGI
│
├── authentication/              # Módulo de autenticación
│   ├── models.py                # Modelo User personalizado
│   ├── views.py                 # Vistas de login/registro
│   ├── forms.py                 # Formularios de usuario
│   ├── urls.py                  # URLs de autenticación
│   └── admin.py                 # Configuración admin
│
├── menu/                        # Módulo de menú digital
│   ├── models.py                # Modelos Category y Dish
│   ├── views.py                 # CRUD de menú
│   ├── forms.py                 # Formularios de platos
│   └── urls.py                  # URLs de menú
│
├── orders/                      # Módulo de pedidos
│   ├── models.py                # Modelos Order y OrderItem
│   ├── views.py                 # Gestión de pedidos
│   ├── forms.py                 # Formularios de órdenes
│   └── urls.py                  # URLs de pedidos
│
├── reservations/                # Módulo de reservas
│   ├── models.py                # Modelos Reservation y Table
│   ├── views.py                 # Gestión de reservas
│   ├── forms.py                 # Formularios de reservas
│   └── urls.py                  # URLs de reservas
│
├── cash_management/             # Módulo de caja
│   ├── models.py                # Modelos CashRegister y Sale
│   ├── views.py                 # Reportes y gestión de caja
│   ├── forms.py                 # Formularios de caja
│   └── urls.py                  # URLs de caja
│
├── templates/                   # Plantillas HTML
│   ├── base.html                # Plantilla principal con navegación Bootstrap
│   ├── authentication/          # Templates de autenticación
│   │   ├── home.html            # Página de inicio
│   │   ├── dashboard.html       # Dashboard general
│   │   ├── menu_dashboard.html  # Dashboard cliente
│   │   ├── orders_dashboard.html # Dashboard mesero
│   │   ├── admin_dashboard.html # Dashboard administrador
│   │   ├── login.html           # Formulario de login
│   │   └── register.html        # Formulario de registro
│   ├── menu/                    # Templates de menú
│   │   ├── menu_list.html       # Lista de categorías y platos
│   │   ├── menu_detail.html     # Detalle de categoría
│   │   ├── dish_list.html       # Lista de platos por categoría
│   │   ├── dish_detail.html     # Detalle de plato
│   │   ├── category_form.html   # Formulario de categoría
│   │   └── dish_form.html       # Formulario de plato
│   ├── orders/                  # Templates de pedidos
│   │   ├── order_list.html      # Lista de todas las órdenes
│   │   ├── order_detail.html    # Detalle de orden
│   │   ├── order_create.html    # Formulario de crear orden
│   │   ├── kitchen_orders.html  # Vista de cocina
│   │   └── order_form.html      # Formulario de orden
│   ├── reservations/            # Templates de reservas
│   │   ├── reservation_list.html # Lista de reservas
│   │   ├── reservation_detail.html # Detalle de reserva
│   │   ├── reservation_create.html # Formulario de crear reserva
│   │   └── reservation_form.html # Formulario de reserva
│   └── cash_management/         # Templates de caja
│       ├── dashboard.html       # Dashboard principal de caja
│       ├── cash_register_list.html # Lista de registros de caja
│       ├── cash_register_detail.html # Detalle de registro
│       ├── sales_list.html      # Lista de ventas
│       └── reports.html         # Reportes y estadísticas
│
└── static/                      # Archivos estáticos
    ├── css/
    │   └── style.css            # Estilos personalizados Bootstrap
    ├── js/
    │   └── main.js              # JavaScript principal
    └── images/                  # Imágenes del proyecto
        ├── logo/                 # Logotipos y branding
        ├── dishes/              # Imágenes de platos
        ├── categories/          # Imágenes de categorías
        └── ui/                  # Iconos y elementos UI
```

## 🔧 Flujo de Trabajo por Rol

### 🧑 Cliente
1. **Registro** en el sistema
2. **Login** con credenciales
3. **Explorar menú** digital
4. **Hacer pedido** seleccionando platos
5. **Hacer reserva** seleccionando fecha/hora
6. **Ver historial** de pedidos y reservas

### 🍽 Mesero
1. **Login** al sistema
2. **Ver pedidos** pendientes
3. **Tomar pedidos** asignándose
4. **Actualizar estado** de pedidos
5. **Ver cocina** para pedidos en preparación
6. **Confirmar reservas** del día
7. **Gestionar caja** - abrir/cerrar
8. **Generar reportes** diarios

### 👨‍💼 Administrador
1. **Login** al sistema
2. **Gestionar usuarios** y roles
3. **Administrar menú** - categorías y platos
4. **Configurar mesas** del restaurante
5. **Ver todos los pedidos** y reservas
6. **Acceso a panel** Django admin
7. **Configurar sistema** - settings generales
8. **Generar reportes** avanzados

## 🎨 Características de UI/UX

### Diseño Responsivo
- **Mobile-first:** Optimizado para dispositivos móviles
- **Tablets y desktop:** Adaptación automática
- **Navegación intuitiva:** Menú contextual por rol

### Experiencia de Usuario
- **Dashboard personalizado** por tipo de usuario
- **Notificaciones en tiempo real** de cambios de estado
- **Búsqueda y filtrado** rápido de información
- **Formularios validados** con feedback visual

### Accesibilidad
- **Etiquetas semánticas** HTML5
- **Contraste adecuado** para legibilidad
- **Navegación por teclado** funcional
- **Lectores de pantalla** compatibles

## 🔒 Seguridad Implementada

### Protección de Datos
- **Hashing de contraseñas** con algoritmos seguros
- **Protección CSRF** en todos los formularios
- **Sesiones seguras** con configuración HTTPONLY
- **Validación de entrada** sanitización de datos

### Control de Acceso
- **Autenticación requerida** para funciones sensibles
- **Permisos por rol** granulares
- **Logs de actividad** para auditoría
- **CORS configurado** para API futuras

## 📊 Reportes y Análisis

### Reportes Diarios
- **Ventas totales** por método de pago
- **Número de órdenes** por estado
- **Reservas** vs completadas
- **Productos más vendidos**
- **Horas pico** de actividad

### Métricas de Negocio
- **Ticket promedio** por orden
- **Tiempo de preparación** promedio
- **Ocupación de mesas** por franja horaria
- **Frecuencia de clientes** recurrentes

## 🚀 Despliegue y Producción

### Configuración de Producción
- **Variables de entorno** para settings sensibles
- **Base de datos PostgreSQL** recomendada
- **Servidor Gunicorn** para producción
- **Archivos estáticos** con Whitenoise
- **Dominios permitidos** configurados

### Optimizaciones
- **Compresión gzip** habilitada
- **Caching configurado** para mejorar rendimiento
- **CDN para assets** estáticos
- **Monitorización** básica implementada

## 🔄 Mantenimiento y Actualizaciones

### Tareas Programadas
- **Backups automáticos** de base de datos
- **Actualización de dependencias** regular
- **Limpieza de logs** periódica
- **Monitoreo de rendimiento** continuo

### Escalabilidad
- **Arquitectura modular** para fácil expansión
- **API REST preparada** para integraciones
- **Microservicios** opcionales para crecimiento
- **Base de datos escalable** con migraciones

## 🤝 Contribución y Desarrollo

### Guía de Contribución
1. **Fork del repositorio**
2. **Crear rama de características**
3. **Desarrollo con pruebas**
4. **Pull request** con descripción detallada
5. **Revisión de código** por pares
6. **Merge a main** después de aprobación

### Estándares de Código
- **PEP 8** para Python
- **Indentación consistente** (4 espacios)
- **Nomenclatura descriptiva** de variables
- **Comentarios explicativos** en código complejo
- **Tests unitarios** para funcionalidades críticas

## 📞 Soporte y Ayuda

### Documentación
- **README detallado** con ejemplos
- **Comentarios en código** para desarrolladores
- **Wiki del proyecto** para guías avanzadas
- **Issues template** para reportar problemas

### Canales de Comunicación
- **Issues de GitHub** para reportar bugs
- **Discusiones** para propuestas de mejora
- **Releases** con notas de versión
- **Wiki colaborativa** para documentación

## 📄 Licencia

Este proyecto está licenciado bajo **MIT License**, permitiendo:
- ✅ Uso comercial y personal
- ✅ Modificación y distribución
- ✅ Creación de trabajos derivados
- ✅ Uso privado y público

Atribución requerida a **Sebastian SST** como autor original.

---

## 🎊 Conclusión

El **Sistema Integral de Gestión de Restaurante (SIGR)** es una solución completa, moderna y escalable para la gestión eficiente de restaurantes. Combina las mejores prácticas de desarrollo web con una interfaz intuitiva y funcionalidades robustas que cubren todos los aspectos críticos de la operación de un restaurante.

**¿Listo para revolucionar tu gestión de restaurantes?** 🚀

**Contacto y Soporte:**
- 📧 **Desarrollador:** Sebastian SST
- 📧 **Email:** contacto@sigr.com
- 🌐 **GitHub:** https://github.com/SebastianSST/SGR
- 📞 **Issues:** Reportar problemas y sugerencias

---

*SIGR - Transformando la gestión de restaurantes, un plato a la vez.* 🍽✨
