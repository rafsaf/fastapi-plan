from typing import Optional
import tortoise.fields.data as fields
from tortoise.models import Model


class User(Model):
    """
    The User model
    """

    id: int = fields.IntField(pk=True)
    email: str = fields.CharField(max_length=50, unique=True)
    name: Optional[str] = fields.CharField(max_length=50, null=True, default=None)
    family_name: Optional[str] = fields.CharField(
        max_length=50, null=True, default=None
    )
    password_hash: str = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    def full_name(self) -> str:
        """
        Returns the best name
        """
        if self.name or self.family_name:
            return f"{self.name or ''} {self.family_name or ''}".strip()
        return self.email

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash"]
