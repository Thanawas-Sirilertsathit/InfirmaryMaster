<template>
	<div class="min-h-screen bg-base-200 px-4 py-16">
		<div
			class="mx-auto max-w-2xl rounded-2xl border border-base-300 bg-base-100 p-8 shadow-xl"
		>
			<div
				class="mb-6 inline-flex rounded-full border border-warning/30 bg-warning/10 px-3 py-1 text-sm font-semibold text-warning-content"
			>
				Staff account pending verification
			</div>
			<h1 class="text-4xl font-bold text-primary">
				Verification Required
			</h1>
			<p class="mt-4 text-base-content/80">
				Your staff account has been created, but an administrator still
				needs to verify it before you can access staff tools.
			</p>
			<p class="mt-3 text-base-content/70">
				Please contact an administrator and return after your account
				has been approved.
			</p>

			<div class="mt-8 flex flex-col gap-3 sm:flex-row">
				<router-link to="/login" class="btn btn-primary">
					Back to Login
				</router-link>
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
import axios from 'axios';

export default {
	name: 'StaffUnverifiedPage',
	methods: {
		clearStoredAuth() {
			localStorage.removeItem('authToken');
			localStorage.removeItem('authUser');
			localStorage.removeItem('refreshToken');
		},
		async logoutUser() {
			const refreshToken = localStorage.getItem('refreshToken');

			try {
				if (refreshToken) {
					await axios.post('http://localhost:8000/api/auth/logout/', {
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

<style scoped></style>
