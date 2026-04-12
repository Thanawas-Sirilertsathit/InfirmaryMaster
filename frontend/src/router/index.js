import { createRouter, createWebHistory } from 'vue-router';
import StaffLayout from '../layouts/StaffLayout.vue';

const routes = [
	{ path: '/', component: () => import('../pages/LandingPage.vue') },
	{ path: '/register', component: () => import('../pages/RegisterPage.vue') },
	{ path: '/login', component: () => import('../pages/LoginPage.vue') },
	{
		path: '/unauthorized',
		component: () => import('../pages/UnauthorizedPage.vue'),
	},
	{
		path: '/staff/unverified',
		meta: { requiresAuth: true, allowedRoles: ['staff'] },
		component: () => import('../pages/StaffUnverifiedPage.vue'),
	},
	{
		path: '/medicine',
		component: StaffLayout,
		meta: {
			requiresAuth: true,
			allowedRoles: ['staff', 'admin'],
			requiresVerifiedStaff: true,
		},
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
		meta: {
			requiresAuth: true,
			allowedRoles: ['staff', 'admin'],
			requiresVerifiedStaff: true,
		},
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
		meta: {
			requiresAuth: true,
			allowedRoles: ['staff', 'admin'],
			requiresVerifiedStaff: true,
		},
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
		meta: { requiresAuth: true, allowedRoles: ['patient'] },
		component: () => import('../pages/MyPrescriptionListPage.vue'),
	},
	{
		path: '/my-prescriptions/:id',
		meta: { requiresAuth: true, allowedRoles: ['patient'] },
		component: () => import('../pages/MyPrescriptionDetailPage.vue'),
	},
	{
		path: '/prescription/:id',
		meta: {
			requiresAuth: true,
			allowedRoles: ['staff', 'admin'],
			requiresVerifiedStaff: true,
		},
		component: () => import('../pages/PatientPrescriptionDetailPage.vue'),
	},
	{
		path: '/prescription/create',
		meta: {
			requiresAuth: true,
			allowedRoles: ['staff', 'admin'],
			requiresVerifiedStaff: true,
		},
		component: () => import('../pages/CreatePrescriptionPage.vue'),
	},
	{
		path: '/staff',
		meta: { requiresAuth: true, allowedRoles: ['admin'] },
		component: () => import('../pages/StaffTablePage.vue'),
	},
	{
		path: '/:pathMatch(.*)*',
		component: () => import('../pages/NotFoundPage.vue'),
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

router.beforeEach((to, from, next) => {
	const storedUser = localStorage.getItem('authUser');
	const user = storedUser ? JSON.parse(storedUser) : null;
	const allowedRoles = Array.isArray(to.meta.allowedRoles)
		? to.meta.allowedRoles
		: [];

	if (to.meta.requiresAuth && !user) {
		next('/login');
		return;
	}

	if (allowedRoles.length && !allowedRoles.includes(user?.role)) {
		next('/unauthorized');
		return;
	}

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
		next('/unauthorized');
		return;
	}

	next();
});

export default router;
