from math import log


def size_convertor(bytes_size):
    """
    Convert bytes into a more readable format (e.g., KB, MB, GB).

    Args:
        bytes_size (int): Size in bytes.

    Returns:
        str: Readable size format with appropriate units.
    """
    if bytes_size < 0:
        raise ValueError("Size cannot be negative")
    if bytes_size == 0:
        return '0 Byte'

    size_name = ('Byte', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(log(bytes_size, 1024))
    p = pow(1024, i)
    s = round(bytes_size / p, 2)

    return f'{s} {size_name[i]}'
