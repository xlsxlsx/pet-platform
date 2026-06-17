from enum import StrEnum


class UserRoleCode(StrEnum):
    CUSTOMER = "CUSTOMER"
    MERCHANT = "MERCHANT"
    HOSPITAL = "HOSPITAL"
    ADMIN = "ADMIN"


class AccountStatus(StrEnum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    PENDING_REVIEW = "PENDING_REVIEW"


class ReviewStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

