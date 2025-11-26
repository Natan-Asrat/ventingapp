from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def add_params(url, params):
    url_parts = urlparse(url)
    query = parse_qs(url_parts.query)

    # Merge new params
    query.update(params)

    new_query = urlencode(query, doseq=True)

    return urlunparse((
        url_parts.scheme,
        url_parts.netloc,
        url_parts.path,
        url_parts.params,
        new_query,
        url_parts.fragment
    ))
