#!/usr/bin/env python3

import os


def is_root() -> bool:
    """Comprueba si el proceso actual se está ejecutando con privilegios de root.

    Returns:
        True si el UID efectivo es 0 (root), False en caso contrario.
    """
    return os.geteuid() == 0
