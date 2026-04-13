<template>
	<div class="landing-page" data-theme="mytheme">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary mb-6">
				Welcome to InfirmaryMaster
			</h1>
			<div class="landing-copy-block mx-auto max-w-3xl">
				<div class="flex justify-center mb-4">
					<img src="/serina3.gif" alt="Serina" class="landing-gif" />
				</div>
				<p class="text-primary">
					An infirmary inventory and prescription management system
					for tracking medicine stock, monitoring batches, and
					managing patient prescriptions in one place.
				</p>
				<p class="text-primary mt-3">
					Register or log in to manage daily infirmary operations more
					efficiently.
				</p>
			</div>
		</header>
		<div class="flex justify-center mt-3">
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
