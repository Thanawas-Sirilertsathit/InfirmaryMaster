# Infirmary Master

This is a web application for managing and tracking medicine in infirmary efficiently.

## User roles

- patient: Reading his/her own prescriptions that staff issued
- staff: Managing medicines and prescriptions in the infirmary
- admin: Verifying newly registered staff

## Technology stack

- Backend is powered by Django Python with REST framework.
- Frontend is powered by Vue JS with Tailwind along with DaisyUI.

## How to install and run

- [Installation Guide](INSTALLATION.md)

## System architecture (Hybrid between layer and service-based architecture)

1. Backend has been divided into 6 services which each of them has its own responsibility according to service-based architecture.

- Inventory service: Handle stock transactions and medicine batches related tasks.
- Medicines service: Holding medicine information and low stock criteria of each medicine. Responsible for adding, editing and reading medicine detail.
- Patients service: Wiring patient when prescription is created.
- Prescriptions service: Prescriptions creation, getting information of prescriptions and trigger stock transactions.
- Reports service: Notification for low stock, run out of the stock and near expire medicine batch.
- Users service: Handle authentication actions.

2. All services are wired into the API endpoints to serve the frontend.
3. Frontend has an api_manager.js to handle API operations like GET, POST, PUT and DELETE.
4. Frontend pages call api_manager to call the API to backend.

## Screenshots of the application

- Once your application is running, the first page you should see is LandingPage.
  [LandingPage](/screenshots/Landing.png)
