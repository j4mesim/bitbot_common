import httpx
import datetime


def dictify_headers(headers: httpx.Headers):
    return {"encoding": headers.encoding, "raw": dict(headers.raw)}


def dictify_url(url: httpx.URL):
    return {
        "host": url.host,
        "scheme": url.scheme,
        "path": url.path,
    }


def dictify_request(request: httpx.Request):
    content_dict = request.__getstate__()
    content_dict["headers"] = dictify_headers(request.headers)
    content_dict["url"] = dictify_url(request.url)
    return content_dict


def dictify_response(response: httpx.Response):
    response_dict = response.__getstate__().copy()
    response_dict["_elapsed"] = response._elapsed.microseconds
    response_dict["headers"] = dictify_headers(response.headers)
    response_dict["request"] = dictify_request(response.request)
    response_dict["_request"] = dictify_request(response._request)
    return response_dict


def is_dictify_response_data(data: object):
    if not isinstance(data, dict):
        return False
    return set(data) == {"_elapsed", "headers", "request", "_request"}


def dedictify_url(url_dict: dict) -> httpx.URL:
    return httpx.URL(**url_dict)


def dedictify_headers(headers_dict: dict):
    return httpx.Headers(headers_dict["raw"], encoding=headers_dict["encoding"])


def dedictify_request(request_dict: dict):
    request_dict["headers"] = dedictify_headers(request_dict["headers"])
    request_dict["url"] = dedictify_url(request_dict["url"])
    content = request_dict.pop("_content")
    request = httpx.Request(**request_dict, content=content)
    return request


def dedictify_response(response_dict: dict):
    response_dict["_elapsed"] = datetime.timedelta(
        microseconds=response_dict["_elapsed"],
    )
    response_dict["request"] = dedictify_request(response_dict["request"])
    response_dict["_request"] = dedictify_request(response_dict["_request"])
    response = httpx.Response(200)
    response.__setstate__(response_dict)
    return response
