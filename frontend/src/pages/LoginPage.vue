<template>
	<div class="login-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Login</h1>
			<p class="text-secondary mt-4">Access your account to continue.</p>
		</header>
		<form
			class="max-w-lg mx-auto mt-10 bg-white p-6 rounded shadow"
			@submit.prevent="loginUser"
		>
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Email or Username</span>
				</label>
				<input
					type="text"
					placeholder="Enter your email or username"
					class="input input-bordered"
					v-model="emailOrUsername"
				/>
			</div>
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Password</span>
				</label>
				<input
					type="password"
					placeholder="Enter your password"
					class="input input-bordered"
					v-model="password"
				/>
			</div>
			<p v-if="errorMessage" class="text-red-500 text-sm mb-4">
				{{ errorMessage }}
			</p>
			<button class="btn btn-primary w-full">Login</button>
		</form>
	</div>
</template>

<script>
import apiManager from '@/api/api_manager';

export default {
	name: 'LoginPage',
	data() {
		return {
			emailOrUsername: '',
			password: '',
			errorMessage: '',
		};
	},
	methods: {
		async loginUser() {
			this.errorMessage = '';
			try {
				const response = await apiManager.post('/api/auth/login/', {
					username: this.emailOrUsername,
					password: this.password,
				});

				const accessToken = response.data.access;
				const refreshToken = response.data.refresh;
				const authenticatedUser = response.data.user;
				if (accessToken && refreshToken) {
					localStorage.setItem('authToken', accessToken);
					localStorage.setItem('refreshToken', refreshToken);
					localStorage.setItem(
						'authUser',
						JSON.stringify(authenticatedUser),
					);
				} else {
					throw new Error(
						'Authentication tokens are missing in the response.',
					);
				}

				const userRole = authenticatedUser.role;

				if (userRole === 'admin') {
					this.$router.push('/staff');
				} else if (userRole === 'staff') {
					this.$router.push(
						authenticatedUser.verified
							? '/inventory'
							: '/staff/unverified',
					);
				} else if (userRole === 'patient') {
					this.$router.push('/my-prescriptions');
				} else {
					this.$router.push('/');
				}
			} catch (error) {
				console.error('Login failed:', error);
				this.errorMessage =
					error.response?.data?.error ||
					'Login failed. Please try again.';
			}
		},
	},
};
</script>

<style scoped></style>
