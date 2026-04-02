<template>
	<div class="register-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Register</h1>
			<p class="text-secondary mt-4">Create an account to get started.</p>
		</header>
		<form class="max-w-lg mx-auto mt-10 bg-white p-6 rounded shadow">
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Full Name</span>
				</label>
				<input
					type="text"
					placeholder="Enter your full name"
					class="input input-bordered"
				/>
			</div>
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Email</span>
				</label>
				<input
					type="email"
					placeholder="Enter your email"
					class="input input-bordered"
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
				/>
			</div>
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Confirm Password</span>
				</label>
				<input
					type="password"
					placeholder="Confirm your password"
					class="input input-bordered"
				/>
			</div>
			<button class="btn btn-primary w-full">Register</button>
		</form>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	name: 'RegisterPage',
	data() {
		return {
			fullName: '',
			email: '',
			password: '',
			confirmPassword: '',
		};
	},
	methods: {
		async registerUser() {
			if (this.password !== this.confirmPassword) {
				alert('Passwords do not match!');
				return;
			}
			try {
				const response = await axios.post(
					'http://localhost:8000/api/auth/register/',
					{
						full_name: this.fullName,
						email: this.email,
						password: this.password,
					},
				);
				console.log('Registration successful:', response.data);
				// Handle successful registration (e.g., redirect, show success message)
			} catch (error) {
				console.error('Registration failed:', error);
			}
		},
	},
};
</script>

<style scoped>
/* Add any specific styles for the register page here */
</style>
