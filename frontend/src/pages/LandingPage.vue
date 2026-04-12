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

<style scoped>
.landing-copy-block {
	padding: 2rem;
	border: 1px solid #e5e7eb;
	border-radius: 1.5rem;
	background: rgba(255, 255, 255, 0.92);
	box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease;
}

.landing-copy-block:hover {
	transform: translateY(-1px);
	border-color: #fda4af;
	box-shadow: 0 12px 24px rgba(244, 63, 94, 0.14);
}

.landing-gif {
	max-width: min(100%, 24rem);
	height: auto;
	object-fit: contain;
	margin-bottom: 1rem;
	border-radius: 1.25rem;
}
</style>
