from fastapi import FastAPI
from opentelemetry import trace
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
    title="Microservicio de Ventas",
    root_path="/api/ventas"
)

# 3. ¡Magia pura! Auto-instrumentamos FastAPI para que capture cada petición automáticamente
FastAPIInstrumentor.instrument_app(app)


# Nota que aquí dejamos la ruta limpia, sin el prefijo
@app.get("/get-ventas")
def obtener_ventas():
    """Endpoint principal que Traefik enrutará."""
    return {
        "status": "success",
        "message": "¡Hola desde el MS de Ventas!",
        "data": [
            {"id": 1, "nombre": "Dev 1"},
            {"id": 2, "nombre": "Dev 2"}
        ]
    }
    
@app.get("/health")
def health_check():
    """Endpoint vital para el monitoreo."""
    return {"status": "ok", "service": "ms-ventas"}