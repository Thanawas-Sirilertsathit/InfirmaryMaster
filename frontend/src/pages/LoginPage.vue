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
import axios from 'axios';

export default {
	name: 'LoginPage',
	data() {
		return {
			emailOrUsername: '',
			password: '',
			errorMessage: '', // Add error message state
		};
	},
	methods: {
		async loginUser() {
			this.errorMessage = ''; // Reset error message
			try {
				const response = await axios.post(
					'http://localhost:8000/api/auth/login/',
					{
						username: this.emailOrUsername,
						password: this.password,
					},
				);
				console.log('Login successful:', response.data);
				// Handle successful login (e.g., redirect, store token)
			} catch (error) {
				console.error('Login failed:', error);
				this.errorMessage =
					error.response?.data?.error ||
					'Login failed. Please try again.'; // Display error message
			}
		},
	},
};
</script>

<style scoped>
/* Add any specific styles for the login page here */
</style>
