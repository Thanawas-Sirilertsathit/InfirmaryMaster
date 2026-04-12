<template>
	<div class="landing-page" data-theme="mytheme">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">
				Welcome to Our Website
			</h1>
			<p class="text-secondary mt-4">
				Navigate to register or login to continue.
			</p>
		</header>
		<div class="flex justify-center mt-10">
			<router-link
				to="/register"
				class="btn btn-primary mx-2 border-2 border-base-content"
				>Register</router-link
			>
			<router-link
				to="/login"
				class="btn btn-secondary mx-2 border-2 border-base-content"
				>Login</router-link
			>
		</div>
	</div>
</template>

<script>
export default {
	name: 'LandingPage',
};
</script>

<style scoped>
/* Add any specific styles for the landing page here */
</style>
