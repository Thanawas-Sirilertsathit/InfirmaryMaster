import { createRouter, createWebHistory } from 'vue-router';

const routes = [
	{ path: '/', component: () => import('../pages/LandingPage.vue') },
	{ path: '/register', component: () => import('../pages/RegisterPage.vue') },
	{ path: '/login', component: () => import('../pages/LoginPage.vue') },
	{
		path: '/medicine',
		component: () => import('../pages/MedicineListPage.vue'),
	},
	{
		path: '/medicine/:id',
		component: () => import('../pages/MedicineDetailPage.vue'),
	},
	{
		path: '/inventory',
		component: () => import('../pages/InventoryPage.vue'),
	},
	{
		path: '/prescriptions',
		component: () => import('../pages/PatientPrescriptionListPage.vue'),
	},
	{
		path: '/prescription/:id',
		component: () => import('../pages/PatientPrescriptionDetailPage.vue'),
	},
	{ path: '/staff', component: () => import('../pages/StaffTablePage.vue') },
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
