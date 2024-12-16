from app import create_app, db
from app.travel.models import Destination, Package
from datetime import  date

# Crear la aplicación
app = create_app()

# Ejecutar el código dentro de un contexto de aplicación
with app.app_context():
    # Lista de destinos
    destinos = [
    ("Valparaíso", "Ciudad portuaria de Chile, famosa por su arquitectura y cultura.", "Paseo por la ciudad, visita al puerto, tours históricos", 15000),
    ("Santiago", "La capital de Chile, rodeada de montañas y con una gran vida urbana.", "Visita a la Plaza de Armas, tour por los Andes, restaurantes y museos", 12000),
    ("San Pedro de Atacama", "Desierto más árido del mundo, con paisajes impresionantes.", "Visitas a los géiseres del Tatio, Valle de la Luna, observación de estrellas", 25000),
    ("Isla de Pascua", "Isla remota en el Pacífico, famosa por sus moáis y cultura ancestral.", "Excursión a los moáis, caminatas por la isla, playas", 40000),
    ("Pucón", "Ciudad ubicada en el sur de Chile, famosa por su volcán y lagos.", "Senderismo, rafting, termas, actividades en el volcán Villarrica", 22000),
    ("Puerto Varas", "Ciudad en la Región de los Lagos, rodeada de naturaleza.", "Navegación por el Lago Llanquihue, excursión al volcán Osorno, visita a las termas", 18000),
    ("La Serena", "Ubicada en la zona norte de Chile, conocida por sus playas y cielos despejados.", "Visita al Valle del Elqui, playas, observación astronómica", 14000),
    ("Valle de Casablanca", "Famoso por sus viñedos y vinos.", "Tour por viñedos, cata de vinos, visitas a bodegas", 17000),
    ("Temuco", "Ciudad en el sur de Chile, conocida por su cultura mapuche y parques naturales.", "Visita a parques nacionales, cultura mapuche, senderismo", 16000),
    ("Concepción", "Una ciudad universitaria, con acceso a playas y naturaleza.", "Visita a las playas, senderismo, vida nocturna", 13000),
    ("Viña del Mar", "Famosa por sus playas, jardines y el Festival Internacional de la Canción.", "Disfrutar de la playa, ver el festival, paseo por los jardines", 16000),
    ("Chiloé", "Archipiélago en el sur de Chile, conocido por sus iglesias de madera y mitología.", "Visita a las iglesias de madera, navegación por el archipiélago", 22000),
    ("Cochamó", "Ubicada en la Región de los Lagos, conocida por sus hermosos valles y paisajes naturales.", "Senderismo, escalada, camping", 25000),
    ("Punta Arenas", "Ciudad en el extremo sur de Chile, cerca de la Antártida.", "Visitas a la isla Magdalena, navegación por el estrecho de Magallanes", 27000),
    ("Iquique", "Ciudad costera en el norte de Chile, famosa por su clima y desierto.", "Deportes extremos, paseo por el desierto de Atacama, playas", 13000),
    ("Rapa Nui", "Otro nombre para Isla de Pascua, famosa por sus moáis.", "Cultura rapanui, caminatas, playa Anakena", 38000),
    ("Aysén", "Región austral conocida por sus glaciares y lagos.", "Excursión a los glaciares, pesca, caminatas por la naturaleza", 21000),
    ("La Araucanía", "Región del sur conocida por su cultura mapuche y paisajes naturales.", "Visitas culturales, senderismo, termas", 18000),
    ("Parque Nacional Torres del Paine", "Un parque nacional en la Patagonia, famoso por sus montañas y lagos.", "Senderismo, paseos en bote, observación de fauna", 30000),
    ("Elqui Valley", "Famoso por la producción de pisco y cielos despejados para la observación astronómica.", "Visitas a pisco destilerías, observación de estrellas, trekking", 15000),
    ]
    

    # Agregar destinos a la base de datos
    for nombre, descripcion, actividades, costo in destinos:
        destino = Destination(name=nombre, description=descripcion, activities=actividades, cost=costo)
        db.session.add(destino)
    
    # Lista de paquetes turísticos
    paquetes = [
    ("Aventura Inca", "Recorrido por Machu Picchu y alrededores, ideal para los amantes de la historia y la aventura.", 50000, date(2024, 1, 1), date(2024, 12, 31)),
    ("Maravillas de la India", "Tour por los lugares más emblemáticos de la India, como el Taj Mahal.", 60000, date(2024, 5, 1), date(2024, 11, 30)),
    ("Exploración Patagónica", "Recorrido por los glaciares y montañas de la Patagonia.", 70000, date(2024, 3, 1), date(2024, 9, 30)),
    ("Descubriendo Chiloé", "Tour cultural por la isla de Chiloé, famosa por su arquitectura y naturaleza.", 45000, date(2024, 4, 1), date(2024, 10, 31)),
    ("Valle del Elqui", "Recorrido por el valle, visitando viñedos y observatorios astronómicos.", 35000, date(2024, 6, 1), date(2024, 12, 31)),
    ("Ruta del Pisco", "Visita a las mejores bodegas de pisco en Chile.", 28000, date(2024, 2, 1), date(2024, 8, 31)),
    ("Aventura en Pucón", "Actividades de aventura como rafting, senderismo y visitas al volcán Villarrica.", 48000, date(2024, 1, 1), date(2024, 12, 31)),
    ("Isla de Pascua", "Explora la cultura y los moáis de la isla más aislada del mundo.", 55000, date(2024, 7, 1), date(2024, 12, 31)),
    ("Tour de los Lagos", "Excursión por los lagos del sur de Chile, incluyendo navegación y senderismo.", 62000, date(2024, 3, 1), date(2024, 10, 31)),
    ("Cultura Mapuche", "Tour cultural por la región de La Araucanía, visitando comunidades mapuches.", 39000, date(2024, 5, 1), date(2024, 12, 31)),
    ("Torres del Paine", "Excursión por el Parque Nacional Torres del Paine, uno de los más hermosos del mundo.", 80000, date(2024, 10, 1), date(2024, 12, 31)),
    ("Santiago y Valparaíso", "Un recorrido combinado entre la capital y la ciudad costera de Valparaíso.", 42000, date(2024, 1, 1), date(2024, 12, 31)),
    ("Chilean Wine Tour", "Tour enológico por los mejores viñedos de Chile.", 38000, date(2024, 6, 1), date(2024, 11, 30)),
    ("Desierto de Atacama", "Recorrido por el desierto más árido del mundo, visitando los géiseres y el Valle de la Luna.", 75000, date(2024, 3, 1), date(2024, 9, 30)),
    ("Viña del Mar y Reñaca", "Disfruta de las playas y la vida nocturna de la costa central.", 35000, date(2024, 1, 1), date(2024, 12, 31)),
    ("Rapa Nui", "Visita a la Isla de Pascua, explorando su cultura y sus antiguos moáis.", 85000, date(2024, 2, 1), date(2024, 12, 31)),
    ("Elqui Astronómico", "Tour de observación astronómica en el Valle de Elqui.", 33000, date(2024, 4, 1), date(2024, 12, 31)),
    ("Río Maule", "Disfruta de las actividades de aventura en el río Maule y su entorno natural.", 46000, date(2024, 5, 1), date(2024, 11, 30)),
    ("Patagonia y Fiordos", "Excursión por la Patagonia, explorando los fiordos y glaciares.", 92000, date(2024, 1, 1), date(2024, 12, 31)),
    ]

    # Agregar paquetes a la base de datos
    for nombre, descripcion, precio, desde, hasta in paquetes:
        paquete = Package(name=nombre, description=descripcion, price=precio, available_from=desde, available_to=hasta)
        db.session.add(paquete)
    
    # Confirmar los cambios en la base de datos
    db.session.commit()

    print("Destinos y paquetes agregados correctamente")
