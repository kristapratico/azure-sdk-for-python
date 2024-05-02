import os
import openai
import dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from azure.openai import InstrumentOpenAI

dotenv.load_dotenv()

InstrumentOpenAI()
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

exporter = AzureMonitorTraceExporter(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

client = openai.AzureOpenAI()

messages = [
    {"role": "system", "content": "Don't make assumptions about what values to plug into tools. Ask for clarification if a user request is ambiguous."},
    {"role": "user", "content": "What's the weather like today in Seattle?"}
]
response = client.chat.completions.create(
    messages=messages,
    model="gpt-4",
)
