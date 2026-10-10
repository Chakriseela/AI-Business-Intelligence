from dotenv import load_dotenv
from confident_trace import init
from phoenix.otel import register

load_dotenv()

# Register Phoenix as the OpenTelemetry provider
tracer_provider = register(
    project_name="bizinsight-ai",
    endpoint="http://localhost:6006/v1/traces",
)

init(tracer_provider=tracer_provider)

# Tracer used by our custom BizInsight spans
tracer = tracer_provider.get_tracer("bizinsight-ai")
