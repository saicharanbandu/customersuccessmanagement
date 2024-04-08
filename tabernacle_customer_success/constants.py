PAGINATION_LIMIT = "25"
VIEWER = "viewer"
EDITOR = "editor"
PAID = "paid"
PENDING = "pending"
DUE = "due"
OVERDUE = "overdue"
EXPIRY = "expiry"
ACCEPTED = "accepted"
REJECTED = "rejected"
AWAITING = "awaiting"
MEETING_SCHEDULED = "meeting scheduled"
INITIATED = "initiated"
TRIAL = "trial"
EXPIRY = "expiry"


TRIAL_DURATION = 14

STAFF_ACCESS_ROLE_CHOICES = [(VIEWER, "Viewer"), (EDITOR, "Editor")]

PLAN_DURATION_CHOICES = [("1", "Monthly"), ("12", "Yearly")]

PAYMENT_STATUS_CHOICES = [(PAID, "Paid"), (PENDING, "Pending")]

PROSPECT_STATUS_CHOICES = [
    (INITIATED, "First Call"),
    (MEETING_SCHEDULED, "Meeting Scheduled"),
    (AWAITING, "Awaiting Response"),
    (TRIAL, "On Trial Period"),
    (ACCEPTED, "Responded Yes"),
    (REJECTED, "Responded No"),
]


PROSPECT_SORT_CHOICES = [
    ("name", "Name (A-Z)"),
    ("-name", "Name (Z-A)"),
    ("-updated_at", "Record Updated (Newest First)"),
    ("updated_at", "Record Updated (Oldest First)"),
]
