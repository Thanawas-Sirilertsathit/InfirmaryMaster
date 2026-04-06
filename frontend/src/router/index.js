import { createRouter, createWebHistory } from 'vue-router';
import StaffLayout from '../layouts/StaffLayout.vue';

const routes = [
	{ path: '/', component: () => import('../pages/LandingPage.vue') },
	{ path: '/register', component: () => import('../pages/RegisterPage.vue') },
	{ path: '/login', component: () => import('../pages/LoginPage.vue') },
	{
		path: '/medicine',
		component: StaffLayout,
		children: [
			{
				path: '',
				component: () => import('../pages/MedicineListPage.vue'),
			},
			{
				path: ':id',
				component: () => import('../pages/MedicineDetailPage.vue'),
			},
		],
	},
	{
		path: '/inventory',
		component: StaffLayout,
		children: [
			{
				path: '',
				component: () => import('../pages/InventoryPage.vue'),
			},
		],
	},
	{
		path: '/prescriptions',
		component: StaffLayout,
		children: [
			{
				path: '',
				component: () =>
					import('../pages/PatientPrescriptionListPage.vue'),
			},
		],
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
