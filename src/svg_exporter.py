"""
Модуль для экспорта D2-разметки в SVG через утилиту d2.
"""
import os
import subprocess
from typing import Optional

from errors import ConfigError

D2_COMMAND = 'd2'
SVG_EXTENSION = '.svg'
D2_EXTENSION = '.d2'


def export_to_svg(
    d2_file_path: str,
    svg_file_path: Optional[str] = None
) -> str:
    """
    Конвертирует D2-файл в SVG через утилиту d2.
    """
    if svg_file_path is None:
        base = d2_file_path
        if base.endswith(D2_EXTENSION):
            base = base[:-len(D2_EXTENSION)]
        svg_file_path = base + SVG_EXTENSION

    command = [D2_COMMAND, d2_file_path, svg_file_path]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        raise ConfigError(
            "d2 utility not found. Install from d2lang.com"
        )
    except subprocess.CalledProcessError as e:
        raise ConfigError(
            f"d2 conversion failed: {e.stderr}"
        )

    return svg_file_path


def generate_and_export(
    d2_content: str,
    output_svg: str
) -> str:
    """
    Создаёт D2-файл и конвертирует его в SVG.
    """
    d2_path = output_svg
    if d2_path.endswith(SVG_EXTENSION):
        d2_path = d2_path[:-len(SVG_EXTENSION)] + D2_EXTENSION

    from d2_generator import save_d2_file
    save_d2_file(d2_content, d2_path)

    if os.path.exists(d2_path):
        return export_to_svg(d2_path, output_svg)

    return output_svg