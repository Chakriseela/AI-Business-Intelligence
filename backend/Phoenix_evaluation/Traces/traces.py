import json
import pandas as pd
from backend.config.settings import PHOENIX_BASE_URL
from phoenix.client import Client
# python.exe -m backend.Phoenix_evaluation.Traces.traces

# Initialize client
client = Client(base_url=PHOENIX_BASE_URL)

# 1. Fetch the spans (traces) using the updated resource path
# By default, Phoenix logs everything to the "default" project
df = client.spans.get_spans_dataframe(project_identifier="bizinsight-ai") 

# 2. See the available columns (attributes)
print(df.columns)

# 3. View the first few traces
print(df.head())

# Take the very first span record
first_span = df.iloc[0].to_dict()

# Print the entire object cleanly
print("=== COMPLETE SPAN DATA OBJECT ===")
print(json.dumps(first_span, indent=4, default=str))


# # Target the specific trace ID from your application
# target_trace_id = "4080b0e60f76fca646afff93c5c09f14"

# # Fetch the entire trace lifecycle from the server
# # (Using a list filter since get_traces expects an iterable of IDs)
# traces = client.get_traces(trace_ids=[target_trace_id])


# 1. Fetch all traces from the default project
# (Omitting trace_ids returns all captured traces)
traces = list(client.traces.get_traces(project_identifier="bizinsight-ai"))

if traces:
    # 2. Grab the very first trace dictionary from the list
    first_trace_dict = traces[0]
    
    # 3. Access keys using dictionary bracket notation safely
    # Phoenix trace objects use 'trace_id' instead of 'id' in their return payload
    dynamic_trace_id = first_trace_dict.get("trace_id") or first_trace_dict.get("id") or "unknown_trace"

    # 4. Save the dictionary directly to a JSON file
    output_filename = f"first_trace_{dynamic_trace_id}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(first_trace_dict, f, indent=4, default=str)
        
    print(f"✅ Success! First trace (ID: {dynamic_trace_id}) written to: {output_filename}")
    print("=== COMPLETE TRACE DATA OBJECT ===")
    print(json.dumps(first_trace_dict, indent=4, default=str))
    print(f"✅ Trace data saved to {output_filename}.")
else:
    print("❌ No traces found in your Phoenix instance.")
