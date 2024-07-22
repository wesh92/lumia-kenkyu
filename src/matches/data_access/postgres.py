from typing import Any, Optional, Sequence
from supabase import create_client, Client
from data_access.dao import AbstractDAO
from CONSTS import get_secrets, DAOType, Environment
