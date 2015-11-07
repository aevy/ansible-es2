from collections import MutableMapping


def merge_hash(a, b):
    """
    Recursively merges hash b into a so that keys from b take precedence over keys from a
    """
    result = a.copy()

    # next, iterate over b keys and values
    for k, v in b.iteritems():
        # if there's already such key in a
        # and that key contains a MutableMapping
        if k in result and isinstance(result[k], MutableMapping):
            # merge those dicts recursively
            result[k] = merge_hash(result[k], v)
        else:
            # otherwise, just copy the value from b to a
            result[k] = v

    return result


def combine(*terms, **kwargs):
    recursive = kwargs.get('recursive', False)
    if len(kwargs) > 1 or (len(kwargs) == 1 and 'recursive' not in kwargs):
        raise RuntimeError("whoops")
    for t in terms:
        if not isinstance(t, dict):
            raise RuntimeError("whoops")

    if recursive:
        return reduce(merge_hash, terms)
    else:
        return dict(itertools.chain(*map(lambda x: x.iteritems(), terms)))


class FilterModule(object):
    def filters(self):
        return {
            'combine': combine
        }
