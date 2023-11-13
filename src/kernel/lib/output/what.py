#!/usr/bin/env python3

__all__ = ['what']

import kernel
import assure
from .array import argsort, similarities, permute

def what(query, keys):
    q = assure.vector(query)
    K = assure.vectors([kernel.think(key) for key in keys])
    s = similarities(q, K)
    I = argsort(s.ravel())[::-1]
    return permute(keys, I).tolist()
