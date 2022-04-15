import itertools

candidate_url = r"/albums/{id}"
url = "/albums/123442"


def part_compare(actual, template):
    if "{" not in template and "}" not in template:
        return actual == template
    if template[0] == "{" and template[-1] == "}":
        return True
    else:
        return False


def does_path_match(actual, template):
    return all(
        itertools.starmap(part_compare, zip(actual.split("/"), template.split("/")))
    )


mapping = {r"/albums/{id}": {200: lambda **kwargs: {"baz": "bang", **kwargs}}}


def path_match(registed_routes, url):
    matched_route = next(
        (
            template_path
            for template_path in registed_routes.keys()
            if does_path_match(url, template_path)
        ),
        False,
    )
    return registed_routes.get(matched_route)


def response_match(registed_routes, url, status_code):
    return path_match(registed_routes, url).get(status_code)


def response_intercept(registed_routes, url, status_code, json):
    interceptor = response_match(registed_routes, url, status_code)
    return interceptor(**json)


test = response_intercept(mapping, url, 200, {"foo": "bar"})
