# app/tools/ordem_servico/__init__.py

from app.tools.ordem_servivo.count_os_tecnico import (
    contar_os_concluidas_por_tecnico,
    listar_os_por_tecnico_periodo
)

__all__ = [
    'contar_os_concluidas_por_tecnico',
    'listar_os_por_tecnico_periodo'
]