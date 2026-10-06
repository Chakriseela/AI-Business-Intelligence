from phoenix.otel import register

# Register Phoenix as the OpenTelemetry provider
tracer_provider = register(
    project_name="bizinsight-ai",
    endpoint="http://localhost:6006/v1/traces",
)

# Tracer used by our custom BizInsight spans
tracer = tracer_provider.get_tracer("bizinsight-ai")