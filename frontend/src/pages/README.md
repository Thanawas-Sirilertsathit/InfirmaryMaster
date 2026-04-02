# Pages Directory

This directory contains all the Vue components for the pages in the application. Each page corresponds to a route in the application. Below is the structure of the pages based on the information provided in `PAGES.md`:

## Auth Related Pages

- `LandingPage.vue`: Displays the website overview and navigation to register and login pages.
- `RegisterPage.vue`: Allows staff/patients to register. Staff registration requires admin verification.
- `LoginPage.vue`: Enables users to log in with email/username and password.

## Staff Pages

- `MedicineListPage.vue`: Lists all medicines in a card layout with a search bar.
- `MedicineDetailPage.vue`: Displays detailed information about a specific medicine.
- `InventoryPage.vue`: Shows a summary of medicines in the inventory.
- `PrescriptionListPage.vue`: Displays prescriptions in a table format with search and filter options.
- `PrescriptionDetailPage.vue`: Shows detailed information about a specific prescription.
- `CreatePrescriptionPage.vue`: Provides a form to create a prescription for a patient.

### Modals

- `AddMedicineModal.vue`: Modal for adding a new type of medicine.
- `AddMedicineBatchModal.vue`: Modal for adding a new batch of medicine to the inventory.
- `RemoveMedicineBatchModal.vue`: Modal for confirming the removal of a medicine batch.

## Patient Pages

- `PatientPrescriptionListPage.vue`: Displays the patient's prescriptions in a table format with search and filter options.
- `PatientPrescriptionDetailPage.vue`: Shows detailed information about a specific prescription for the patient.

## Admin Page

- `StaffTablePage.vue`: Displays a list of staff users with their verification status and a button to verify new staff.

---

### Notes

- Each page should call the appropriate backend API to fetch and display data.
- Components should be modular and reusable where possible.
- Use Tailwind CSS and DaisyUI for consistent styling.
