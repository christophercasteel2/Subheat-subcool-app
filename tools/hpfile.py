"""Write and read HP Prime program files in the format current firmware uses
(what the Connectivity Kit itself saves): a 12-byte header followed by
length-prefixed records.

    7C 61 8A B2 FE FF FF FF 00 00 00 00      header
    [u32 len][05 FF ..] x3                    flag records
    [u32 len][3E 02 00 01][function entries]  every function, with its kind
    [u32 len][BE 00 40 01][source block]      the PPL source, UTF-16LE + NUL
    [u32 len][8E 02 40 02][...]               trailer

tools/hpapp/container.bin is an empty file of this shape (header, flag
records and trailer taken from a Connectivity Kit file); build() fills in
the function list and the source.
"""
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
CONTAINER = os.path.join(HERE, "hpapp", "container.bin")
HEADER = 12
FUNCS = bytes.fromhex("3e020001")
CODE = bytes.fromhex("be004001")
MARK = bytes.fromhex("9b00c000")      # starts the source text


def records(b, off=HEADER, end=None):
    """[(offset, length, tag)] of the records between off and end."""
    end = len(b) if end is None else end
    out = []
    while off < end:
        ln, = struct.unpack_from("<I", b, off)
        out.append((off, ln, b[off + 4:off + 8]))
        off += 4 + ln
    if off != end:
        raise ValueError("record lengths do not add up")
    return out


def function_entry(name, exported, nparams):
    # flag as current firmware writes it: 8, +1 if EXPORT, +16 per parameter
    flag = 8 | (1 if exported else 0) | (nparams << 4)
    body = (bytes.fromhex("44000000") + bytes.fromhex("0b024000") +
            name.encode("utf-16-le").ljust(64, b"\0") +
            struct.pack("<I", 8) + bytes.fromhex("05028000") + struct.pack("<I", flag))
    return struct.pack("<I", len(body)) + body


def build(source, functions):
    """source: PPL text; functions: [(name, exported, number of parameters)]
    in source order."""
    tpl = open(CONTAINER, "rb").read()
    out = bytearray(tpl[:HEADER])
    for off, ln, tag in records(tpl):
        rec = tpl[off:off + 4 + ln]
        if tag == FUNCS:
            body = FUNCS + b"".join(function_entry(*f) for f in functions)
            rec = struct.pack("<I", len(body)) + body
        elif tag == CODE:
            (p, sl, _), = records(tpl, off + 8, off + 4 + ln)
            m = tpl.index(MARK, p)
            data = source.encode("utf-16-le") + b"\0\0"
            sub = bytearray(tpl[p:m + 4]) + data
            struct.pack_into("<I", sub, 0, len(sub) - 4)
            struct.pack_into("<I", sub, m - 4 - p, len(data) + 4)
            body = CODE + bytes(sub)
            rec = struct.pack("<I", len(body)) + body
        out += rec
    return bytes(out)


def read(b):
    """(source, [function names]) from a file written by build() or the
    Connectivity Kit (first source block only)."""
    names, source = [], None
    for off, ln, tag in records(b):
        if tag == FUNCS:
            for p, sl, _ in records(b, off + 8, off + 4 + ln):
                names.append(b[p + 12:p + 76].decode("utf-16-le").split("\0")[0])
        elif tag == CODE and source is None:
            p, sl, _ = records(b, off + 8, off + 4 + ln)[0]
            m = b.index(MARK, p)
            n, = struct.unpack_from("<I", b, m - 4)
            if n != p + 4 + sl - m:
                raise ValueError("source length field is wrong")
            source = b[m + 4:p + 4 + sl - 2].decode("utf-16-le")
    return source, names
