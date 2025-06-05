import time

_cache = {}

def cache_set(chave, valor, ttl=300):
    _cache[chave] = (valor, time.time() + ttl)

def cache_get(chave):
    item = _cache.get(chave)
    if not item:
        return None
    valor, expira = item
    if time.time() > expira:
        del _cache[chave]
        return None
    return valor

def cache_clear(chave):
    if chave in _cache:
        del _cache[chave]
