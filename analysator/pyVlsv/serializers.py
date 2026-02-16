import struct
import numpy as np

def parse_herm_spectrum_bytes(buf: bytes, size_t_fmt='Q', real_fmt='d'):
    """Parse one HermSpectrum struct from bytes (little-endian memcpy layout).
    Returns (parsed_dict, bytes_consumed).
    """
    offset = 0
    le = '<'
    blen = len(buf)
    def need(n):
        if offset + n > blen:
            raise ValueError('overflow')

    need(4)
    N_hermite_harmonic = struct.unpack_from(le + 'i', buf, offset)[0]; offset += 4
    need(4)
    vth = struct.unpack_from(le + 'f', buf, offset)[0]; offset += 4
    need(12)
    u = struct.unpack_from(le + '3f', buf, offset); offset += 12

    size_fmt = le + size_t_fmt
    size_sz = struct.calcsize(size_fmt)
    need(size_sz)
    (vec_size,) = struct.unpack_from(size_fmt, buf, offset); offset += size_sz

    herm_bytes = 4 * int(vec_size)
    need(herm_bytes)
    herm_spectrum = np.frombuffer(buf, dtype=np.float32, count=int(vec_size), offset=offset).copy(); offset += herm_bytes

    real_fmt_full = le + (real_fmt * 6)
    real_sz = struct.calcsize(real_fmt_full)
    need(real_sz)
    v_limits = struct.unpack_from(real_fmt_full, buf, offset); offset += real_sz

    shape_fmt = le + (size_t_fmt * 3)
    shape_sz = struct.calcsize(shape_fmt)
    need(shape_sz)
    shape = struct.unpack_from(shape_fmt, buf, offset); offset += shape_sz

    # reshape if possible
    try:
        prod = int(np.prod(shape))
        if prod == int(vec_size) and prod > 0:
            herm_spectrum = herm_spectrum.reshape(tuple(int(s) for s in shape))
    except Exception:
        pass

    parsed = {
        'N_hermite_harmonic': int(N_hermite_harmonic),
        'vth': float(vth),
        'u': np.array(u, dtype=np.float32),
        'HermSpectrum': herm_spectrum,
        'v_limits': np.array(v_limits),
        'shape': tuple(int(s) for s in shape),
    }
    return parsed, offset


def parse_herm_spectrum_sequence(blob: bytes, size_t_fmt='Q', real_fmt='d', max_items=None):
    """Parse a sequence of HermSpectrum structs from a bytes blob.
    Returns list of parsed dicts and total bytes consumed.
    """
    out = []
    idx = 0
    blen = len(blob)
    count = 0
    while idx < blen:
        try:
            parsed, used = parse_herm_spectrum_bytes(blob[idx:], size_t_fmt=size_t_fmt, real_fmt=real_fmt)
        except Exception:
            break
        out.append(parsed)
        idx += used
        count += 1
        if max_items is not None and count >= max_items:
            break
    return out, idx
