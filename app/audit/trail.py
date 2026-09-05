import datetime
import json
import logging
from typing import List, Optional, Dict, Any
from app.models.audit import AuditEvent, AuditEventType

logger = logging.getLogger("commerce_agent.audit")

class AuditTrail:
    """In-memory and structured logging audit trail for money safety & governance."""
    _instance: Optional['AuditTrail'] = None

    def __init__(self):
        self.events: List[AuditEvent] = []

    @classmethod
    def get_instance(cls) -> 'AuditTrail':
        if cls._instance is None:
            cls._instance = AuditTrail()
        return cls._instance

    def log_event(
        self,
        session_id: str,
        event_type: AuditEventType,
        agent: str,
        tool: Optional[str] = None,
        transaction_id: Optional[str] = None,
        order_id: Optional[str] = None,
        amount: Optional[float] = None,
        currency: Optional[str] = None,
        authorization_state: Optional[str] = None,
        result: Optional[str] = None,
        error: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> AuditEvent:
        # Sanitize details to ensure sensitive fields are excluded
        clean_details = self._sanitize(details) if details else None
        
        event = AuditEvent(
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            session_id=session_id,
            event_type=event_type,
            agent=agent,
            tool=tool,
            transaction_id=transaction_id,
            order_id=order_id,
            amount=amount,
            currency=currency,
            authorization_state=authorization_state,
            result=result,
            error=error,
            details=clean_details
        )
        self.events.append(event)
        logger.info(f"AUDIT_TRAIL: {event.model_dump_json(exclude_none=True)}")
        return event

    def _sanitize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        sensitive_keys = {"card", "cvv", "api_key", "secret", "token", "password", "key"}
        sanitized = {}
        for k, v in data.items():
            if any(s in k.lower() for s in sensitive_keys):
                sanitized[k] = "[REDACTED]"
            elif isinstance(v, dict):
                sanitized[k] = self._sanitize(v)
            else:
                sanitized[k] = v
        return sanitized

    def get_session_events(self, session_id: str) -> List[AuditEvent]:
        return [e for e in self.events if e.session_id == session_id]

    def clear(self):
        self.events.clear()

def get_audit_trail() -> AuditTrail:
    return AuditTrail.get_instance()
