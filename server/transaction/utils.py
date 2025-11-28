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

def add_connects(connects, user):
    if hasattr(user, "connects"):
        print("user connects before", user.connects)
        user.connects = (user.connects or 0) + connects
        user.save(update_fields=["connects"])
        print("updated user connects to", user.connects)
