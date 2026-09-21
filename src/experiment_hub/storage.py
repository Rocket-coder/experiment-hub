from uuid import UUID

from experiment_hub.models import Run


runs: dict[UUID, Run] = {}