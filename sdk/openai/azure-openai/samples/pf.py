import os

from promptflow.client import PFClient
from promptflow.entities import AzureOpenAIConnection
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from azure.openai import InstrumentOpenAI

load_dotenv()

InstrumentOpenAI()

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

exporter = AzureMonitorTraceExporter(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

client = PFClient()

# Initialize an AzureOpenAIConnection object
connection = AzureOpenAIConnection(
    name="open_ai_connection",
    api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)
# Create the connection, note that api_key will be scrubbed in the returned result
result = client.connections.create_or_update(connection)
print(result)
# client can help manage your runs and connections.

flow = "."

# Test flow
flow_inputs = {
    "url": "https://play.google.com/store/apps/details?id=com.twitter.android",
}
flow_result = client.test(flow=flow, inputs=flow_inputs)
print(f"Flow result: {flow_result}")
