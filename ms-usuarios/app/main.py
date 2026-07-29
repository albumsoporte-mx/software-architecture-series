from fastapi import FastAPI
from opentelemetry import trace
from fastapi import HTTPException
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# 1. Configuramos el proveedor principal de trazas (TracerProvider)
provider = TracerProvider()
trace.set_tracer_provider(provider)

# 2. Apuntamos el exportador OTLP al puerto 4318 de nuestro OTel Collector en la red interna
otlp_exporter = OTLPSpanExporter(endpoint="http://inspector_otel:4318/v1/traces")
processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)



# El root_path hace la magia: le avisa a Swagger UI que estamos detrás de un Gateway
app = FastAPI(
    title="Microservicio de Usuarios",
    root_path="/api/usuarios"
)

# 3. ¡Magia pura! Auto-instrumentamos FastAPI para que capture cada petición automáticamente
FastAPIInstrumentor.instrument_app(app)


# Nota que aquí dejamos la ruta limpia, sin el prefijo
@app.get("/get-usuarios")
def obtener_usuarios():
    """Endpoint principal que Traefik enrutará."""
    return {
        "status": "success",
        "message": "¡Hola desde el MS de Usuarios!",
        "data": [
            {"id": 1, "nombre": "Dev 1"},
            {"id": 2, "nombre": "Dev 2"}
        ]
    }
    
@app.get("/health")
def health_check():
    """Endpoint vital para el monitoreo."""
    return {"status": "ok", "service": "ms-usuarios"}



tracer = trace.get_tracer(__name__)

@app.get("/simular-error")
def detonar_error():
    """Endpoint para probar cómo viajan los errores críticos en la telemetría."""
    
    # Creamos un bloque de rastreo manual (Span)
    with tracer.start_as_current_span("operacion_riesgosa_db") as span:
        
        # 1. Agregamos un log/evento interno a la traza
        span.add_event("Iniciando conexión a la supuesta base de datos...")
        
        # 2. Le inyectamos atributos personalizados (etiquetas)
        span.set_attribute("usuario.id", 999)
        span.set_attribute("accion", "simulacion_caos")
        
        # 3. ¡Hacemos que todo explote!
        span.add_event("¡Fallo detectado! Cerrando conexiones de emergencia.")
        raise HTTPException(
            status_code=500, 
            detail="Error crítico: La base de datos simulada no responde."
        )