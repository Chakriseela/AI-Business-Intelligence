PS D:\D_drive\MY_PROJECTS\14. AI Business Intelligence\AI-Business-Intelligence (Git Repo)\bizinsight-ai> python -m backend.DeepEval_evaluation.rag_evaluation.run_rag_evaluation
OpenTelemetry Tracing Details
|  Phoenix Project: bizinsight-ai
|  Span Processor: SimpleSpanProcessor
|  Collector Endpoint: http://localhost:6006/v1/traces
|  Transport: HTTP + protobuf
|  Transport Headers: {}
|
|  Using a default SpanProcessor. `add_span_processor` will overwrite this default.
|  
|  WARNING: It is strongly advised to use a BatchSpanProcessor in production environments.
|  
|  `register` has set this TracerProvider as the global OpenTelemetry default.
|  To disable this behavior, call `register` with `set_global_tracer_provider=False`.

Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "D:\D_drive\MY_PROJECTS\14. AI Business Intelligence\AI-Business-Intelligence (Git Repo)\bizinsight-ai\backend\DeepEval_evaluation\rag_evaluation\run_rag_evaluation.py", line 148, in <module>
    ContextualRelevancyMetric(
    ~~~~~~~~~~~~~~~~~~~~~~~~~^
        threshold=0.70,
        ^^^^^^^^^^^^^^^
        model=EVAL_MODEL,
        ^^^^^^^^^^^^^^^^^
        include_reason=True,
        ^^^^^^^^^^^^^^^^^^^^
    ),
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\metrics\contextual_relevancy\contextual_relevancy.py", line 112, in __init__
    self.model, self.using_native_model = initialize_model(
                                          ~~~~~~~~~~~~~~~~^
        model, self.eval_mode
        ^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\metrics\utils\models.py", line 186, in initialize_model
    return _build_model(model)
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\metrics\utils\models.py", line 231, in _build_model
    return OpenAIModel(model=model), True
           ~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\models\llms\openai_model.py", line 143,in __init__
    super().__init__(model)
    ~~~~~~~~~~~~~~~~^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\models\base_model.py", line 75, in __init__
    self.model = self.load_model()
                 ~~~~~~~~~~~~~~~^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\models\llms\openai_model.py", line 478,in load_model
    return self._build_client(OpenAI)
           ~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\models\llms\openai_model.py", line 496,in _build_client
    api_key = require_secret_api_key(
        self.api_key,
    ...<2 lines>...
        param_hint="`api_key` to OpenAIModel(...)",
    )
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\models\utils.py", line 100, in require_secret_api_key
    raise DeepEvalError(
    ...<3 lines>...
    )
deepeval.errors.DeepEvalError: OpenAI API key is not configured. Set OPENAI_API_KEY in your environment or pass `api_key` to OpenAIModel(...).
PS D:\D_drive\MY_PROJECTS\14. AI Business Intelligence\AI-Business-Intelligence (Git Repo)\bizinsight-ai> 
