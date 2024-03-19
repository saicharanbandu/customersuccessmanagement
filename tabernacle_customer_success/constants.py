PAGINATION_LIMIT = '10'

VIEWER = 'viewer'
EDITOR = 'editor'

STAFF_ACCESS_ROLE_CHOICES = [(VIEWER, 'Viewer'), (EDITOR, 'Editor')]


PLAN_DURATION_CHOICES = [('1', 'Monthly'), ('12', 'Yearly')]

PAID = 'paid'
PENDING = 'pending'
DUE = 'due'
OVERDUE = 'overdue'
EXPIRY = 'expiry'

PAYMENT_STATUS_CHOICES = [(PAID, 'Paid'), (PENDING, 'Pending')]

TRIAL_DURATION = 14