"""
Decoupled Session State & Memory Store
Supports horizontal scaling across serverless Cloud Run instances.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.config import settings

class SessionStore(ABC):
    @abstractmethod
    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def append_message(self, session_id: str, role: str, content: str):
        pass

class InMemorySessionStore(SessionStore):
    def __init__(self):
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self._store.get(session_id, [])

    def append_message(self, session_id: str, role: str, content: str):
        if session_id not in self._store:
            self._store[session_id] = []
        self._store[session_id].append({"role": role, "content": content})

def get_session_store() -> SessionStore:
    # Pluggable backend: In production, switch to AlloyDB/Cloud SQL pgvector client
    return InMemorySessionStore()

session_store = get_session_store()

