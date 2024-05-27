PAGINATION_LIMIT = '25'
VIEWER = 'viewer'
EDITOR = 'editor'
PAID = 'paid'
PENDING = 'pending'
DUE = 'due'
OVERDUE = 'overdue'
EXPIRY = 'expiry'
ACCEPTED = 'accepted'
REJECTED = 'rejected'
AWAITING = 'awaiting'
MEETING_SCHEDULED = 'meeting scheduled'
INITIATED = 'initiated'
TRIAL = 'trial'
SELECT_ALL='all'
EXPIRY = 'expiry'
CASH = 'cash'
ONLINE = 'online'
BANK_TRANSFER = 'bank_transfer'
ALL_ACCESS = 'all_access'


TRIAL_DURATION = 14

STAFF_ACCESS_ROLE_CHOICES = [(VIEWER, 'Viewer'), (EDITOR, 'Editor')]

PLAN_DURATION_CHOICES = [('1', 'Monthly'), ('12', 'Yearly')]

PAYMENT_MODE_CHOICES = [(CASH, 'Cash'), (ONLINE, 'Online'), (BANK_TRANSFER, 'Bank Transfer')]

PAYMENT_STATUS_CHOICES = [(PAID, 'Paid'), (PENDING, 'Payment due later')]

PROSPECT_STATUS_CHOICES = [
    (SELECT_ALL,'Select All'),
    (INITIATED, 'First Call'),
    (MEETING_SCHEDULED, 'Meeting Scheduled'),
    (AWAITING, 'Awaiting Response'),
    (TRIAL, 'On Trial Period'),
    (ACCEPTED, 'Responded Yes'),
    (REJECTED, 'Responded No'),
]

contact_sort_options = {
            "Customer Name (A-Z)": "name",
            "Customer Name (Z-A)": "-name",
            "Contact Created (Newest First)": "created_at",
            "Contact Created (Oldest First)": "-created_at",
            "Contact Updated (Newest First)": "-updated_at",
            "Contact Updated (Oldest First)": "updated_at",
        }
PROSPECT_SORT_CHOICES = {
    "Name (A-Z)": "name",
    "Name (Z-A)": "-name",
    "Record Updated (Newest First)": "-updated_at",
    "Record Updated (Oldest First)": "updated_at",
}
