from __future__ import annotations

import os
import json
from typing import Any, Generator, Iterator, Union

import wrapt
from opentelemetry import trace
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.completion import Completion
from openai import Stream

TracedModels = Union[ChatCompletion, Completion]


def has_tracing_enabled() -> bool:
    tracing = os.getenv("OPENAI_TRACE_ENABLED", "")
    if tracing.lower() == "true":
        return True
    return False


def _set_attribute(span: trace.Span, key: str, value: Any) -> None:
    if value is not None:
        span.set_attribute(key, value)


def _add_request_chat_message_event(span: trace.Span, **kwargs: Any) -> None:
    for message in kwargs.get("messages", []):
        try:
            message = message.to_dict()
        except AttributeError:
            pass

        if message.get("role"):
            name = f"gen_ai.{message.get('role')}.message"
            span.add_event(
                name=name,
                attributes={"event.data": json.dumps(message)}
            )


def _add_request_chat_attributes(span: trace.Span, **kwargs: Any) -> None:
    _set_attribute(span, "gen_ai.system", "openai")
    _set_attribute(span, "gen_ai.request.model", kwargs.get("model"))
    _set_attribute(span, "gen_ai.request.max_tokens", kwargs.get("max_tokens"))
    _set_attribute(span, "gen_ai.request.temperature", kwargs.get("temperature"))
    _set_attribute(span, "gen_ai.request.top_p", kwargs.get("top_p"))


def _add_response_chat_message_event(span: trace.Span, result: ChatCompletion) -> None:
    for choice in result.choices:
        response: dict[str, Any] = {
            "message.role": choice.message.role,
            "message.content": choice.message.content,
            "finish_reason": choice.finish_reason,
            "index": choice.index,
        }
        if choice.message.tool_calls:
            response["message.tool_calls"] = [tool.to_dict() for tool in choice.message.tool_calls]
        span.add_event(name="gen_ai.response.message", attributes={"event.data": json.dumps(response)})


def _add_response_chat_attributes(span: trace.Span, result: ChatCompletion) -> None:
    _set_attribute(span, "gen_ai.response.id", result.id)
    _set_attribute(span, "gen_ai.response.model", result.model)
    _set_attribute(span, "gen_ai.response.finish_reason", result.choices[0].finish_reason)
    if hasattr(result, "usage"):
        _set_attribute(span, "gen_ai.usage.completion_tokens", result.usage.completion_tokens if result.usage else None)
        _set_attribute(span, "gen_ai.usage.prompt_tokens", result.usage.prompt_tokens if result.usage else None)


def _traceable_stream(stream_obj: Stream[ChatCompletionChunk], span: trace.Span) -> Generator[ChatCompletionChunk, None, None]:
    try:
        accumulate: dict[str, Any] = {"role": ""}
        for chunk in stream_obj:
            for item in chunk.choices:
                if item.finish_reason:
                    accumulate["finish_reason"] = item.finish_reason
                if item.index:
                    accumulate["index"] = item.index
                if item.delta.role:
                    accumulate["role"] = item.delta.role
                if item.delta.content:
                    accumulate.setdefault("content", "")
                    accumulate["content"] += item.delta.content
                if item.delta.tool_calls:
                    accumulate.setdefault("tool_calls", [])
                    for tool_call in item.delta.tool_calls:
                        if tool_call.id:
                            accumulate["tool_calls"].append({"id": tool_call.id, "type": "", "function": {"name": "", "arguments": ""}})
                        if tool_call.type:
                            accumulate["tool_calls"][-1]["type"] = tool_call.type
                        if tool_call.function and tool_call.function.name:
                            accumulate["tool_calls"][-1]["function"]["name"] = tool_call.function.name
                        if tool_call.function and tool_call.function.arguments:
                            accumulate["tool_calls"][-1]["function"]["arguments"] += tool_call.function.arguments
            yield chunk

        span.add_event(name="gen_ai.response.message", attributes={"event.data": json.dumps(accumulate)})
        _add_response_chat_attributes(span, chunk)

    except Exception as exc:
        _set_attribute(span, "error.type", exc.__class__.__name__)
        raise

    finally:
        if stream_obj.response.is_stream_consumed and stream_obj.response.is_closed is False:
             span.set_status(trace.Status(trace.StatusCode.ERROR, "Stream was not fully consumed"))
        span.end()


def _wrapped_stream(stream_obj: Stream[ChatCompletionChunk], span: trace.Span) -> Stream[ChatCompletionChunk]:
    class StreamWrapper(wrapt.ObjectProxy):
        def __iter__(self) -> Iterator[ChatCompletionChunk]:
            return _traceable_stream(stream_obj, span)

    return StreamWrapper(stream_obj)


def _add_request_span_attributes(span: trace.Span, span_name: str, kwargs: Any) -> None:
    if span_name.startswith("chat.completions.create"):
        _add_request_chat_attributes(span, **kwargs)
        _add_request_chat_message_event(span, **kwargs)
    # TODO add more models here


def _add_response_span_attributes(span: trace.Span, result: TracedModels) -> None:
    if result.object == "chat.completion":
        _add_response_chat_attributes(span, result)
        _add_response_chat_message_event(span, result)
    # TODO add more models here


def chat_completions_wrapper(tracer: trace.Tracer, span_name: str):
    def _wrapper(func, instance, args, kwargs):
        if not has_tracing_enabled():
            return func(*args, **kwargs)

        span = tracer.start_span(span_name, kind=trace.SpanKind.CLIENT)
        try:
            _add_request_span_attributes(span, span_name, kwargs)

            result = func(*args, **kwargs)

            if hasattr(result, "__stream__"):
                # stream=True used
                return _wrapped_stream(result, span)

            if hasattr(result, "iter_bytes"):
                # with_streaming_response used
                # TODO wrap with object proxy?
                return result

            if hasattr(result, "parse"):
                # with_raw_response used
                parsed = result.parse()
                _add_response_span_attributes(span, parsed)
                return result

            _add_response_span_attributes(span, result)

        except Exception as exc:
            _set_attribute(span, "error.type", exc.__class__.__name__)
            span.end()
            raise

        span.end()
        return result

    return _wrapper


def achat_completions_wrapper(tracer: trace.Tracer, span_name: str):
    async def _wrapper(func, instance, args, kwargs):
        if not has_tracing_enabled():
            return await func(*args, **kwargs)

        span = tracer.start_span(span_name, kind=trace.SpanKind.CLIENT)
        try:
            _add_request_span_attributes(span, span_name, kwargs)

            result = await func(*args, **kwargs)

            if hasattr(result, "__stream__"):
                # stream=True used
                # TODO add async wrapper
                return _wrapped_stream(result, span)

            if hasattr(result, "iter_bytes"):
                # with_streaming_response used
                # TODO wrap with object proxy?
                return result

            if hasattr(result, "parse"):
                # with_raw_response used
                parsed = result.parse()
                _add_response_span_attributes(span, parsed)
                return result

            _add_response_span_attributes(span, result)

        except Exception:
            span.end()
            raise

        span.end()
        return result

    return _wrapper



class InstrumentOpenAI:

    def __init__(self) -> None:

        tracer = trace.get_tracer(__name__)

        wrapt.wrap_function_wrapper(
            "openai.resources.chat.completions",
            "Completions.create",
            chat_completions_wrapper(
                tracer,
                "chat.completions.create",
            ),
        )
        wrapt.wrap_function_wrapper(
            "openai.resources.chat.completions",
            "AsyncCompletions.create",
            achat_completions_wrapper(
                tracer,
                "chat.completions.create",
            ),
        )
