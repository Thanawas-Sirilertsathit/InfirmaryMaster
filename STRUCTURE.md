# Infirmary Master Architecture

## Backend (Service based architecture)
- users (User)
- patients (Patient)
- medicines (Medicine and MedicineCategory)
- inventory (MedicineBatch and StockTransaction)
- prescriptions (Prescription and PrescriptionItem)
- reports (EmailNotification)

Doctor/Nurse prescribes the medicine -> PrescriptionItem created -> Inventory deducted amount of the medicine -> StockTransaction recorded

## Users Service
- Contain role and permission
- User authentication
- 3 roles: Patient, Staff and Admin
- Patient can only view his own prescriptions.
- Staff: can do all stuffs except managing users.
- Admin: verify staff registration.

## Patients Service
- Storing patient records and link them to user accounts
- Reference to prescriptions

## Medicines Service
- Categorizing medicine
- Storing dosage and description
- Setting minimum stock level
- Catalog management

## Inventory Service
- Track available stock
- Perform StockTransaction
- Track expiration date for MedicineBatch

## Prescriptions Service
- Store prescription records
- Link prescriptions to patients
- Trigger inventory deduction on created

## Reports Service
- Notification via email on low stock
- Notification via email on near expiration date of medicine
