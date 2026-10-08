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


==========================================================================================
BIZINSIGHT AI - DEEPEVAL RAG EVALUATION
==========================================================================================

Evaluation Model: gemini-2.5-flash
Dataset: D:\D_drive\MY_PROJECTS\14. AI Business Intelligence\AI-Business-Intelligence (Git Repo)\bizinsight-ai\backend\DeepEval_evaluation\datasets\rag_test_cases.csv

Metrics:
1. Contextual Relevancy
2. Contextual Precision
3. Contextual Recall

Dataset Size: 2

==========================================================================================
TEST CASE: RET-001
==========================================================================================

Question:
How long is the standard warranty for laptops?
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.

RAG Agent Result:
{
  "success": true,
  "context": "BizInsight AI | Business Policy Library\nPage 1\nBIZINSIGHT AI\n Product Warranty Policy\nDocument ID: WAR-004    |    Owner: Operations & Customer Experience    |    Version: 1.0\nPurpose: This controlled document defines business rules used by BizInsight AI when answering customer, sales,\nand operational questions.\nWarranty Coverage\n Product Type\nStandard Warranty\nCoverage Summary\nLaptop\n2 years\nManufacturing defects and covered hardware failures\nElectronics\n2 years\nManufacturing defects under normal use\nAccessories\n1 year\nManufacturing defects\nFurniture\n3years\nStructural defects under normal use\nBattery\n6 months\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n  The product serial number or identifying information may be requested.\n  Damage caused by misuse, unauthorized modification, or accidental impact may be excluded.\n  Warranty coverage does not extend the return window unless a separate exception applies.\n \nRecommended Handling\nWhen a user asks whether an item is covered, determine the product type and purchase timing from structured data when\navailable, then apply the warranty duration and exclusions in this document.\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\n\nHow long is the warranty?\nWarranty duration depends on the product type. Refer to the warranty policy for the approved coverage period.\nWhat benefits do Platinum customers receive?\nPlatinum customers receive the benefits defined in the loyalty program, including the standard 15% discounton eligible\nproducts.\nData vs. Knowledge\n Question Type\nPrimary Source\nCurrent order status\nSQL database\nCustomer purchase amount\nSQL database\nWarranty duration\nKnowledge base\nRefund rules\nKnowledge base\nCustomer-specific policy + transaction question\nSQL + Knowledge base\nThis FAQ is a navigation aid. When a specific policy contains the authoritative rule, the assistant should rely on that\npolicy document.\n\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\nInternal business reference. Rules may be updated by the document owner; the latest approved version takes precedence.",
  "sources": [
    {
      "document": "warranty_policy.pdf",
      "page": 1
    },
    {
      "document": "warranty_policy.pdf",
      "page": 1
    },
    {
      "document": "faq.pdf",
      "page": 1
    },
    {
      "document": "warranty_policy.pdf",
      "page": 1
    }
  ],
  "document_count": 4,
  "retrieval_result": {
    "context": "BizInsight AI | Business Policy Library\nPage 1\nBIZINSIGHT AI\n Product Warranty Policy\nDocument ID:WAR-004    |    Owner: Operations & Customer Experience    |    Version: 1.0\nPurpose: This controlled document defines business rules used by BizInsight AI when answering customer, sales,\nand operational questions.\nWarranty Coverage\nProduct Type\nStandard Warranty\nCoverage Summary\nLaptop\n2 years\nManufacturing defects and covered hardware failures\nElectronics\n2 years\nManufacturing defects under normal use\nAccessories\n1 year\nManufacturing defects\nFurniture\n3 years\nStructural defects under normal use\nBattery\n6 months\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n  The product serial number or identifying information may be requested.\n  Damage caused by misuse, unauthorized modification, or accidental impact may be excluded.\n  Warranty coverage does not extend the return window unless a separate exception applies.\n \nRecommended Handling\nWhen a userasks whether an item is covered, determine the product type and purchase timing from structured data when\navailable, then apply the warranty duration and exclusions in this document.\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\n\nHow long is the warranty?\nWarranty duration depends on the product type. Refer to the warranty policy for the approved coverage period.\nWhat benefits do Platinum customers receive?\nPlatinum customers receive the benefits defined in the loyalty program, including the standard 15% discount on eligible\nproducts.\nData vs. Knowledge\n Question Type\nPrimary Source\nCurrent order status\nSQL database\nCustomer purchase amount\nSQL database\nWarranty duration\nKnowledge base\nRefund rules\nKnowledge base\nCustomer-specific policy + transaction question\nSQL + Knowledge base\nThis FAQ is a navigation aid. When a specific policy contains the authoritative rule, the assistant should rely on that\npolicy document.\n\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\nInternal business reference. Rules may be updated by the document owner; the latest approved version takes precedence.",
    "context_parts": [
      "BizInsight AI | Business Policy Library\nPage 1\nBIZINSIGHT AI\n Product Warranty Policy\nDocument ID: WAR-004  |    Owner: Operations & Customer Experience    |    Version: 1.0\nPurpose: This controlled document defines business rules used by BizInsight AI when answering customer, sales,\nand operational questions.\nWarranty Coverage\n Product Type\nStandard Warranty\nCoverage Summary\nLaptop\n2 years\nManufacturing defects and covered hardware failures\nElectronics\n2 years\nManufacturing defects under normal use\nAccessories\n1 year\nManufacturing defects\nFurniture\n3 years\nStructural defects under normal use\nBattery\n6 months\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.",
      "Manufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n  The product serial number or identifying information may be requested.\n  Damage caused by misuse, unauthorized modification, or accidental impact may be excluded.\n  Warranty coverage does not extend the return window unless a separate exception applies.\n \nRecommended Handling\nWhen a user asks whether an item is covered, determine the product type and purchase timing from structured data when\navailable, then apply the warranty duration and exclusions in this document.\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.",
      "How long is the warranty?\nWarranty duration depends on the product type. Refer to the warranty policy for the approved coverage period.\nWhat benefits do Platinum customers receive?\nPlatinum customers receive the benefits defined in the loyalty program, including the standard 15% discount on eligible\nproducts.\nData vs. Knowledge\n Question Type\nPrimary Source\nCurrent order status\nSQL database\nCustomer purchase amount\nSQL database\nWarranty duration\nKnowledge base\nRefund rules\nKnowledge base\nCustomer-specific policy + transaction question\nSQL + Knowledge base\nThis FAQ is a navigation aid. When a specific policy contains the authoritative rule, the assistant should rely on that\npolicy document.",
      "Decision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\nInternal business reference. Rules may be updated by the document owner; the latest approved version takes precedence."
    ],
    "sources": [
      {
        "document": "warranty_policy.pdf",
        "page": 1
      },
      {
        "document": "warranty_policy.pdf",
        "page": 1
      },
      {
        "document": "faq.pdf",
        "page": 1
      },
      {
        "document": "warranty_policy.pdf",
        "page": 1
      }
    ]
  }
}

Retrieved Context Count: 1
Document Count: 4
Sources: [{'document': 'warranty_policy.pdf', 'page': 1}, {'document': 'warranty_policy.pdf', 'page': 1}, {'document':'faq.pdf', 'page': 1}, {'document': 'warranty_policy.pdf', 'page': 1}]
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we recommend touse AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not recommended. Instead, we recommend to use AFC in Chat.send_message_stream.

Expected Answer:
The standard warranty for laptops is 2 years and covers manufacturing defects and covered hardware failures.

Actual Answer:
Based on the **warranty_policy.pdf**, here is the standard warranty information for laptops:

### **Laptop Warranty Details**

* **Standard Warranty Duration:** **2 years**
* **Coverage Summary:** Covers manufacturing defects and covered hardware failures

---
*Source: `warranty_policy.pdf`*

==========================================================================================
TEST CASE: RET-002
==========================================================================================

Question:
How long is the standard warranty for electronics?

RAG Agent Result:
{
  "success": true,
  "context": "BizInsight AI | Business Policy Library\nPage 1\nBIZINSIGHT AI\n Product Warranty Policy\nDocument ID: WAR-004    |    Owner: Operations & Customer Experience    |    Version: 1.0\nPurpose: This controlled document defines business rules used by BizInsight AI when answering customer, sales,\nand operational questions.\nWarranty Coverage\n Product Type\nStandard Warranty\nCoverage Summary\nLaptop\n2 years\nManufacturing defects and covered hardware failures\nElectronics\n2 years\nManufacturing defects under normal use\nAccessories\n1 year\nManufacturing defects\nFurniture\n3years\nStructural defects under normal use\nBattery\n6 months\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n  The product serial number or identifying information may be requested.\n  Damage caused by misuse, unauthorized modification, or accidental impact may be excluded.\n  Warranty coverage does not extend the return window unless a separate exception applies.\n \nRecommended Handling\nWhen a user asks whether an item is covered, determine the product type and purchase timing from structured data when\navailable, then apply the warranty duration and exclusions in this document.\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\n\nHow long is the warranty?\nWarranty duration depends on the product type. Refer to the warranty policy for the approved coverage period.\nWhat benefits do Platinum customers receive?\nPlatinum customers receive the benefits defined in the loyalty program, including the standard 15% discounton eligible\nproducts.\nData vs. Knowledge\n Question Type\nPrimary Source\nCurrent order status\nSQL database\nCustomer purchase amount\nSQL database\nWarranty duration\nKnowledge base\nRefund rules\nKnowledge base\nCustomer-specific policy + transaction question\nSQL + Knowledge base\nThis FAQ is a navigation aid. When a specific policy contains the authoritative rule, the assistant should rely on that\npolicy document.\n\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\nInternal business reference. Rules may be updated by the document owner; the latest approved version takes precedence.",
  "sources": [
    {
      "document": "warranty_policy.pdf",
      "page": 1
    },
    {
      "document": "warranty_policy.pdf",
      "page": 1
    },
    {
      "document": "faq.pdf",
      "page": 1
    },
    {
      "document": "warranty_policy.pdf",
      "page": 1
    }
  ],
  "document_count": 4,
  "retrieval_result": {
    "context": "BizInsight AI | Business Policy Library\nPage 1\nBIZINSIGHT AI\n Product Warranty Policy\nDocument ID:WAR-004    |    Owner: Operations & Customer Experience    |    Version: 1.0\nPurpose: This controlled document defines business rules used by BizInsight AI when answering customer, sales,\nand operational questions.\nWarranty Coverage\nProduct Type\nStandard Warranty\nCoverage Summary\nLaptop\n2 years\nManufacturing defects and covered hardware failures\nElectronics\n2 years\nManufacturing defects under normal use\nAccessories\n1 year\nManufacturing defects\nFurniture\n3 years\nStructural defects under normal use\nBattery\n6 months\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n  The product serial number or identifying information may be requested.\n  Damage caused by misuse, unauthorized modification, or accidental impact may be excluded.\n  Warranty coverage does not extend the return window unless a separate exception applies.\n \nRecommended Handling\nWhen a userasks whether an item is covered, determine the product type and purchase timing from structured data when\navailable, then apply the warranty duration and exclusions in this document.\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\n\nHow long is the warranty?\nWarranty duration depends on the product type. Refer to the warranty policy for the approved coverage period.\nWhat benefits do Platinum customers receive?\nPlatinum customers receive the benefits defined in the loyalty program, including the standard 15% discount on eligible\nproducts.\nData vs. Knowledge\n Question Type\nPrimary Source\nCurrent order status\nSQL database\nCustomer purchase amount\nSQL database\nWarranty duration\nKnowledge base\nRefund rules\nKnowledge base\nCustomer-specific policy + transaction question\nSQL + Knowledge base\nThis FAQ is a navigation aid. When a specific policy contains the authoritative rule, the assistant should rely on that\npolicy document.\n\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\nInternal business reference. Rules may be updated by the document owner; the latest approved version takes precedence.",
    "context_parts": [
      "BizInsight AI | Business Policy Library\nPage 1\nBIZINSIGHT AI\n Product Warranty Policy\nDocument ID: WAR-004  |    Owner: Operations & Customer Experience    |    Version: 1.0\nPurpose: This controlled document defines business rules used by BizInsight AI when answering customer, sales,\nand operational questions.\nWarranty Coverage\n Product Type\nStandard Warranty\nCoverage Summary\nLaptop\n2 years\nManufacturing defects and covered hardware failures\nElectronics\n2 years\nManufacturing defects under normal use\nAccessories\n1 year\nManufacturing defects\nFurniture\n3 years\nStructural defects under normal use\nBattery\n6 months\nManufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.",
      "Manufacturing defects within the battery warranty period\nClaim Requirements\n  Proof of purchase may be required.\n  The product serial number or identifying information may be requested.\n  Damage caused by misuse, unauthorized modification, or accidental impact may be excluded.\n  Warranty coverage does not extend the return window unless a separate exception applies.\n \nRecommended Handling\nWhen a user asks whether an item is covered, determine the product type and purchase timing from structured data when\navailable, then apply the warranty duration and exclusions in this document.\nDecision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.",
      "How long is the warranty?\nWarranty duration depends on the product type. Refer to the warranty policy for the approved coverage period.\nWhat benefits do Platinum customers receive?\nPlatinum customers receive the benefits defined in the loyalty program, including the standard 15% discount on eligible\nproducts.\nData vs. Knowledge\n Question Type\nPrimary Source\nCurrent order status\nSQL database\nCustomer purchase amount\nSQL database\nWarranty duration\nKnowledge base\nRefund rules\nKnowledge base\nCustomer-specific policy + transaction question\nSQL + Knowledge base\nThis FAQ is a navigation aid. When a specific policy contains the authoritative rule, the assistant should rely on that\npolicy document.",
      "Decision rule: SQL identifies the relevant purchase/product facts; the warranty document supplies the coverage rule.\nInternal business reference. Rules may be updated by the document owner; the latest approved version takes precedence."
    ],
    "sources": [
      {
        "document": "warranty_policy.pdf",
        "page": 1
      },
      {
        "document": "warranty_policy.pdf",
        "page": 1
      },
      {
        "document": "faq.pdf",
        "page": 1
      },
      {
        "document": "warranty_policy.pdf",
        "page": 1
      }
    ]
  }
}

Retrieved Context Count: 1
Document Count: 4
Sources: [{'document': 'warranty_policy.pdf', 'page': 1}, {'document': 'warranty_policy.pdf', 'page': 1}, {'document':'faq.pdf', 'page': 1}, {'document': 'warranty_policy.pdf', 'page': 1}]

Expected Answer:
The standard warranty for electronics is 2 years and covers manufacturing defects under normal use.

Actual Answer:
Based on the company's policy documentation, here are the standard warranty details for electronics:

### **Electronics Warranty Overview**

* **Product Type:** Electronics
* **Standard Warranty Duration:** 2 years
* **Coverage:** Manufacturing defects under normal use

***
*Source: `warranty_policy.pdf`*

==========================================================================================
STARTING DEEPEVAL
==========================================================================================
✨ You're running DeepEval's latest Contextual Relevancy Metric! (using gemini-2.5-flash (Gemini), strict=False, 
async_mode=True)...
✨ You're running DeepEval's latest Contextual Precision Metric! (using gemini-2.5-flash (Gemini), strict=False, 
async_mode=True)...
✨ You're running DeepEval's latest Contextual Recall Metric! (using gemini-2.5-flash (Gemini), strict=False, 
async_mode=True)...
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
Direct use of automatic function calling (AFC) in AsyncModels.generate_content is not recommended. Instead, we 
recommend to use AFC in AsyncChat.send_message. Similarly, direct use of AFC in AsyncModels.generate_content_stream is 
not recommended. Instead, we recommend to use AFC in AsyncChat.send_message_stream.
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
Evaluating 2 test case(s) in parallel ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  50% 0:00:04
    🎯 Evaluating test case #0        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% 0:00:04
    🎯 Evaluating test case #1        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% 0:00:03
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "D:\D_drive\MY_PROJECTS\14. AI Business Intelligence\AI-Business-Intelligence (Git Repo)\bizinsight-ai\backend\DeepEval_evaluation\rag_evaluation\run_rag_evaluation.py", line 598, in <module>
    main()
    ~~~~^^
  File "D:\D_drive\MY_PROJECTS\14. AI Business Intelligence\AI-Business-Intelligence (Git Repo)\bizinsight-ai\backend\DeepEval_evaluation\rag_evaluation\run_rag_evaluation.py", line 521, in main
    results = evaluate(
    
    ...<2 lines>...
        metrics=METRICS,
    )
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\evaluate\evaluate.py", line 278, in evaluate
    test_results = loop.run_until_complete(
        a_execute_test_cases(
    ...<8 lines>...
        )
    )
  File "C:\Python313\Lib\asyncio\base_events.py", line 720, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\evaluate\execute\e2e.py", line 619, in a_execute_test_cases
    await asyncio.wait_for(
    ...<2 lines>...
    )
  File "C:\Python313\Lib\asyncio\tasks.py", line 507, in wait_for
    return await fut
           ^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\evaluate\execute\e2e.py", line 505, in execute_with_semaphore
    return await _await_with_outer_deadline(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        func, *args, timeout=get_per_task_timeout_seconds(), **kwargs
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\evaluate\execute\_common.py", line 239,in _await_with_outer_deadline
    return await asyncio.wait_for(coro, timeout=timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\asyncio\tasks.py", line 507, in wait_for
    return await fut
           ^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\evaluate\execute\e2e.py", line 774, in _a_execute_llm_test_cases
    await measure_metrics_with_indicator(
    ...<8 lines>...
    )
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\metrics\indicator.py", line 255, in measure_metrics_with_indicator
    await asyncio.gather(*tasks)
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\metrics\indicator.py", line 383, in safe_a_measure
    await metric.a_measure(
    ...<3 lines>...
    )
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\tracing\tracing.py", line 1560, in async_wrapper
    return await func(*args, **func_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\metrics\contextual_recall\contextual_recall.py", line 184, in a_measure
    await self._a_generate_verdicts(
        expected_output, retrieval_context, multimodal
    )
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\tracing\tracing.py", line 1560, in async_wrapper
    return await func(*args, **func_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\metrics\contextual_recall\contextual_recall.py", line 282, in _a_generate_verdicts
    verdicts = await a_generate_qag_verdicts(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<8 lines>...
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\metrics\utils\qag.py", line 300, in a_generate_qag_verdicts
    return await a_generate_with_schema_and_extract(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<7 lines>...
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\metrics\utils\generation.py", line 109,in a_generate_with_schema_and_extract
    result, cost = await metric.model.a_generate_with_schema(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        prompt, schema=schema_cls
        ^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\models\base_model.py", line 162, in a_generate_with_schema
    return await self.a_generate(*args, schema=schema, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\tracing\tracing.py", line 1560, in async_wrapper
    return await func(*args, **func_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\asyncio\__init__.py", line 193, in async_wrapped
    return await copy(fn, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\asyncio\__init__.py", line 112, in __call__
    do = await self.iter(retry_state=retry_state)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\asyncio\__init__.py", line 157, in iter
    result = await action(retry_state)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\_utils.py", line 111, in inner
    return call(*args, **kwargs)
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\__init__.py", line 393, in <lambda>
    self._add_action_func(lambda rs: rs.outcome.result())
                                     ~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\concurrent\futures\_base.py", line 449, in result
    return self.__get_result()
           ~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\concurrent\futures\_base.py", line 401, in __get_result
    raise self._exception
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\asyncio\__init__.py", line 116, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\models\retry_policy.py", line 658, in attempt
    return await asyncio.wait_for(coro, per_attempt_timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\asyncio\tasks.py", line 507, in wait_for
    return await fut
           ^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\deepeval\models\llms\gemini_model.py", line 319,in a_generate
    response = await client.aio.models.generate_content(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<9 lines>...
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\google\genai\models.py", line 8461, in generate_content
    response = await self._generate_content(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        model=model, contents=contents, config=final_parsed_config_to_call
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\google\genai\models.py", line 6915, in _generate_content
    response = await self._api_client.async_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        'post', path, request_dict, http_options
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\google\genai\_api_client.py", line 1803, in async_request
    result = await self._async_request(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
        http_request=http_request, http_options=http_options, stream=False
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\google\genai\_api_client.py", line 1736, in _async_request
    return await self._async_retry(  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self._async_request_once, http_request, stream
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\asyncio\__init__.py", line 112, in __call__
    do = await self.iter(retry_state=retry_state)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\asyncio\__init__.py", line 157, in iter
    result = await action(retry_state)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\_utils.py", line 111, in inner
    return call(*args, **kwargs)
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\__init__.py", line 413, in exc_check
    raise retry_exc.reraise()
          ~~~~~~~~~~~~~~~~~^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\__init__.py", line 184, in reraise
    raise self.last_attempt.result()
          ~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\concurrent\futures\_base.py", line 449, in result
    return self.__get_result()
           ~~~~~~~~~~~~~~~~~^^
  File "C:\Python313\Lib\concurrent\futures\_base.py", line 401, in __get_result
    raise self._exception
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\tenacity\asyncio\__init__.py", line 116, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\google\genai\_api_client.py", line 1664, in _async_request_once
    await errors.APIError.raise_for_async_response(response)
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\google\genai\errors.py", line 265, in raise_for_async_response
    await cls.raise_error_async(status_code, response_json, response)
  File "C:\Users\chakr\AppData\Roaming\Python\Python313\site-packages\google\genai\errors.py", line 287, in raise_error_async
    raise ClientError(status_code, response_json, response)
google.genai.errors.ClientError: 404 NOT_FOUND. {'error': {'code': 404, 'message': 'This model models/gemini-2.5-flashis no longer available to new users. Please update your code to use models/gemini-3.8-flash for the latest features and improvements. We recommend you to use the Interactions API (https://ai.google.dev/gemini-api/docs/get-started).', 'status': 'NOT_FOUND'}}
PS D:\D_drive\MY_PROJECTS\14. AI Business Intelligence\AI-Business-Intelligence (Git Repo)\bizinsight-ai> 