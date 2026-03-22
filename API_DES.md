# Infirmary Master API Design (Django REST Framework)

## Authentication
- JWT-based authentication for all endpoints except login/register via email and password.
- Roles: patient, staff, admin.
- Permissions enforced via DRF permission classes.

## Endpoints

### Users
- POST /api/auth/login/ - Login (username, password) → JWT token
- POST /api/auth/register/ - Register (role-based, admin verification for staff)
- POST /api/auth/logout/ - Logout
- GET /api/users/ - Admin: List users (staff/admin only)
- PUT /api/users/{id}/ - Admin: Update user role/status

### Patients
- POST /api/patients/ - Staff/Admin: Create patient profile (linked to user)
- GET /api/patients/search/?fname=...&lname=... - Staff/Admin: Search patients
- GET /api/patients/{id}/ - Staff/Admin: Get patient details
- PUT /api/patients/{id}/ - Staff/Admin: Update patient profile
- GET /api/patients/{id}/prescriptions/ - Patient (own only) / Staff/Admin: Get prescriptions

### Prescriptions
- POST /api/prescriptions/ - Staff: Create prescription with items (triggers inventory deduction)
- GET /api/prescriptions/ - Staff/Admin: List all prescriptions (with filters: ?medicine=...&patient_name=...)
- GET /api/prescriptions/{id}/ - Staff/Admin: Get prescription details
- GET /api/patients/{patient_id}/prescriptions/ - Patient: View own prescriptions

### Medicines
- POST /api/medicines/categories/ - Staff/Admin: Create category
- GET /api/medicines/categories/ - List categories
- POST /api/medicines/ - Staff/Admin: Create medicine
- GET /api/medicines/ - List medicines
- PUT /api/medicines/{id}/ - Staff/Admin: Update medicine (incl. low stock)
- GET /api/medicines/{id}/ - Get medicine details

### Inventory
- POST /api/inventory/batches/ - Staff/Admin: Add new batch
- PUT /api/inventory/batches/{id}/ - Staff/Admin: Update batch quantity
- DELETE /api/inventory/batches/{id}/ - Staff/Admin: Remove batch
- GET /api/inventory/batches/?medicine=... - Staff/Admin: List batches for medicine
- GET /api/inventory/summary/ - Staff/Admin: Stock summary per medicine (grouped by expiration)

### Reports
- POST /api/reports/trigger-low-stock/ - Staff/Admin: Send low stock email
- POST /api/reports/trigger-expiration/ - Staff/Admin: Send near-expiration email
- GET /api/reports/status/ - Check last notification status

## Response Formats
- Success: { "data": {...}, "message": "..." }
- Error: { "error": "description", "code": 400 }

## Permissions
- Patient: Read own data only.
- Staff: All except user management.
- Admin: Full access but mainly for verify the staff registration.