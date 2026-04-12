<template>
	<div class="min-h-screen bg-base-200 px-4 py-16">
		<div
			class="not-found-card mx-auto max-w-2xl rounded-2xl border border-base-300 bg-base-100 p-8 shadow-xl"
		>
			<div
				class="mb-6 inline-flex rounded-full border border-base-300 bg-base-200 px-3 py-1 text-sm font-semibold text-base-content/80"
			>
				Error 404
			</div>
			<h1 class="text-5xl font-bold text-primary">Page Not Found</h1>
			<div class="mt-6 flex justify-center">
				<img
					src="/SumiSerina.png"
					alt="Sumi Serina"
					class="not-found-image"
				/>
			</div>
			<p class="mt-4 text-base-content/80">
				Serina can't find the page you requested.
			</p>
			<p class="mt-3 text-base-content/70">
				Return to the landing page or go back to the previous screen.
			</p>

			<div class="mt-8 flex flex-col gap-3 sm:flex-row">
				<router-link to="/" class="btn btn-primary">
					Go Home
				</router-link>
				<button type="button" class="btn btn-outline" @click="goBack">
					Go Back
				</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'NotFoundPage',
	methods: {
		goBack() {
			this.$router.back();
		},
	},
};
</script>

<style scoped>
.not-found-card {
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease;
}

.not-found-card:hover {
	transform: translateY(-1px);
	border-color: #fda4af;
	box-shadow: 0 12px 24px rgba(244, 63, 94, 0.14);
}
.not-found-image {
	max-width: min(100%, 18rem);
	height: auto;
	object-fit: contain;
	border-radius: 1.25rem;
}
</style>
