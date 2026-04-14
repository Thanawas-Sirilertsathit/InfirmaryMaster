# Infirmary Master

This project aims to erase the problem that patients get defect medicine or the infirmary has no such medicine to provide to the patients. Therefore, Infirmary Master is a solution to this problem by tracking medicine with prescription and stock management systems. Moreover, we offer the alert notification when the medicine is less than the criteria level that we have set, when the medicine is near expiration date (30 days) and when the medicine has completely run out.

## User roles

- patient: Reading his/her own prescriptions that staff issued
- staff: Managing medicines and prescriptions in the infirmary
- admin: Verifying newly registered staff

## Technology stack

- Backend is powered by Django Python with REST framework.
- Frontend is powered by Vue JS with Tailwind along with DaisyUI.
- Database is MySQL as a relational database.
- Containerization is Docker for easy deployment.

## How to install and run

- Follow the guide in [Installation Guide](INSTALLATION.md) step by step to make it run via docker.

## System architecture (Hybrid between layer and service-based architecture)

1. Backend has been divided into 6 services which each of them has its own responsibility according to service-based architecture.

- Inventory service: Handle stock transactions and medicine batches related tasks.
- Medicines service: Holding medicine information and low stock criteria of each medicine. Responsible for adding, editing and reading medicine detail.
- Patients service: Wiring patient when prescription is created although there is no account yet for the patient side.
- Prescriptions service: Prescriptions creation, getting information of prescriptions and trigger stock transactions.
- Reports service: Notification for low stock, run out of the stock and near expire medicine batch.
- Users service: Handle authentication actions. Patient creation is wired through the first name and last name matching.

2. All services are wired into the API endpoints to serve the frontend.
3. Frontend has an api_manager.js to handle API operations like GET, POST, PUT and DELETE.
4. Frontend pages call api_manager to call the API to backend.

## Screenshots of the application

- Once your application is running, the first page you should see is LandingPage.
  ![LandingPage](/screenshots/Landing.png)

### Staff views

- After login as staff and verified, the first page you should see is InventoryPage where you can search and remove the medicine batch.
  ![InventoryPage](/screenshots/Inventory.png)
  
- In this page, you can see the last block says "ADD MEDICINE BATCH", you can press it to add more medicine batch.
  ![MedicineBatch](/screenshots/AddMedicineBatch.png)
  
- On the top right corner, there is a bell icon for notification. This one is for notifying when medicine in the stock is lower than the criteria, running out or near to expiration date (30 days). You can click on the block to read it and it will not become red anymore.
  ![Notification](/screenshots/Notification.png)
  
- Navigating through the navigation bar above to the Medicines, this will let you see all kinds of medicines we have in the infirmary. You can search by the search bar above.
  ![MedicineList](/screenshots/Medicine.png)
  
- Pressing "ADD NEW MEDICINE" will pop up the modal that will let you create new medicine into the infirmary system.
  ![CreateMedicine](/screenshots/AddNewMedicine.png)
- Pressing "DETAILS" in the medicine will show the medicine information of specific medicine you chose.
  ![MedicineDetail](/screenshots/MedicineDetail.png)
  
- In medicine detail page, you can edit the detail of the medicine by clicking "EDIT MEDICINE" above.
  ![EditMedicine](/screenshots/EditMedicine.png)
  
- The last block in the navigation bar is Prescriptions. This page allows you to see all prescriptions in the infirmary.
  ![Prescriptions](/screenshots/PrescriptionList.png)
  
- You can create prescription using the button "CREATE PRESCRIPTION" and it will lead you to fill the form.
  ![CreatePrescription](/screenshots/CreatePrescription.png)
  
- In the Prescription list page, you can view the detail of the prescription by clicking "VIEW" and it will show more information of this prescription.
  ![PrescriptionDetail](/screenshots/PrescriptionDetail.png)

### Patient view
- Patient can see only his/her own prescriptions but can also see the detail of the prescriptions like staff view.
  ![MyPrescription](/screenshots/MyPrescription.png)

### Admin view
- You are allowed only to view StaffTable where you can verify the new registered staff to allow them to get into the system or not.
  ![StaffTable](/screenshots/StaffTable.png)
