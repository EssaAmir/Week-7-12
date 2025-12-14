class ITTicket:
    """Represents an IT support ticket."""

    def __init__(self, ticket_id: int, title: str, priority: str, status: str, assigned_to: str):
        self._id = ticket_id
        self._title = title
        self._priority = priority
        self._status = status
        self._assigned_to = assigned_to

    def assign_to(self, staff: str) -> None:
        self._assigned_to = staff

    def close_ticket(self) -> None:
        self._status = "Closed"

    def get_status(self) -> str:
        return self._status

    def __str__(self) -> str:
        return f"Ticket {self._id}: {self._title} [{self._priority}]"