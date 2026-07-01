import logging as _logging
_logger = _logging.getLogger(__name__)
try:
    from .sitr import install_encrypted_importer
    install_encrypted_importer(__file__)
except Exception:  # pragma: no cover
    _logger.exception("Failed to install encrypted importer")
# -*- coding: utf-8 -*-
from . import models
from . import controllers
