import { createRouter, createWebHistory } from 'vue-router';
import StaffLayout from '../layouts/StaffLayout.vue';

const routes = [
	{ path: '/', component: () => import('../pages/LandingPage.vue') },
	{ path: '/register', component: () => import('../pages/RegisterPage.vue') },
	{ path: '/login', component: () => import('../pages/LoginPage.vue') },
	{
		path: '/staff/unverified',
		component: () => import('../pages/StaffUnverifiedPage.vue'),
	},
	{
		path: '/medicine',
		component: StaffLayout,
		meta: { requiresVerifiedStaff: true },
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
		meta: { requiresVerifiedStaff: true },
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
		meta: { requiresVerifiedStaff: true },
		children: [
			{
				path: '',
				component: () =>
					import('../pages/PatientPrescriptionListPage.vue'),
			},
		],
	},
	{
		path: '/my-prescriptions',
		component: () => import('../pages/MyPrescriptionListPage.vue'),
	},
	{
		path: '/my-prescriptions/:id',
		component: () => import('../pages/MyPrescriptionDetailPage.vue'),
	},
	{
		path: '/prescription/:id',
		meta: { requiresVerifiedStaff: true },
		component: () => import('../pages/PatientPrescriptionDetailPage.vue'),
	},
	{
		path: '/prescription/create',
		meta: { requiresVerifiedStaff: true },
		component: () => import('../pages/CreatePrescriptionPage.vue'),
	},
	{ path: '/staff', component: () => import('../pages/StaffTablePage.vue') },
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

router.beforeEach((to, from, next) => {
	const storedUser = localStorage.getItem('authUser');
	const user = storedUser ? JSON.parse(storedUser) : null;

	if (
		to.meta.requiresVerifiedStaff &&
		user?.role === 'staff' &&
		!user?.verified
	) {
		next('/staff/unverified');
		return;
	}

	if (
		to.path === '/staff/unverified' &&
		user?.role === 'staff' &&
		user?.verified
	) {
		next('/inventory');
		return;
	}

	if (
		user?.role === 'patient' &&
		(to.path === '/prescriptions' ||
			to.path === '/prescription/create' ||
			to.path.startsWith('/prescription/'))
	) {
		next('/my-prescriptions');
		return;
	}

	next();
});

export default router;
