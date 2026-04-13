<template>
	<div class="min-h-screen bg-base-200 px-4 py-16">
		<div
			class="unauthorized-card mx-auto max-w-2xl rounded-2xl border border-base-300 bg-base-100 p-8 shadow-xl"
		>
			<div
				class="mb-6 inline-flex rounded-full border border-error/30 bg-error/10 px-3 py-1 text-sm font-semibold text-error"
			>
				Access restricted
			</div>
			<h1 class="text-4xl font-bold text-primary">Wrong Role</h1>

			<div class="mt-6 flex justify-center">
				<img
					src="/serinabreak.png"
					alt="Serina"
					class="unauthorized-image"
				/>
			</div>

			<p class="mt-4 text-base-content/80">
				Serina caught that your account does not have permission to open
				this page.
			</p>
			<p class="mt-3 text-base-content/70">
				Use the button below to return to the correct area for your
				account.
			</p>

			<div class="mt-8 flex flex-col gap-3 sm:flex-row">
				<button type="button" class="btn btn-primary" @click="goToHome">
					Go to My Area
				</button>
				<button
					type="button"
					class="btn btn-outline"
					@click="logoutUser"
				>
					Log Out
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import apiManager from '@/api/api_manager';

export default {
	name: 'UnauthorizedPage',
	computed: {
		storedUser() {
			const rawUser = localStorage.getItem('authUser');
			return rawUser ? JSON.parse(rawUser) : null;
		},
		homePath() {
			if (this.storedUser?.role === 'admin') {
				return '/staff';
			}

			if (this.storedUser?.role === 'staff') {
				return this.storedUser?.verified
					? '/inventory'
					: '/staff/unverified';
			}

			if (this.storedUser?.role === 'patient') {
				return '/my-prescriptions';
			}

			return '/login';
		},
	},
	methods: {
		clearStoredAuth() {
			localStorage.removeItem('authToken');
			localStorage.removeItem('authUser');
			localStorage.removeItem('refreshToken');
		},
		goToHome() {
			this.$router.push(this.homePath);
		},
		async logoutUser() {
			const refreshToken = localStorage.getItem('refreshToken');

			try {
				if (refreshToken) {
					await apiManager.post('/api/auth/logout/', {
						refresh: refreshToken,
					});
				}
			} catch (error) {
				console.error('Logout failed:', error);
			} finally {
				this.clearStoredAuth();
				this.$router.push('/');
			}
		},
	},
};
</script>
