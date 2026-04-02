<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
	<div class="min-h-screen bg-base-100 text-neutral">
		<header class="p-4 bg-primary text-secondary">
			<h1 class="text-center text-2xl font-bold">Infirmary Master</h1>
		</header>

		<main class="p-4">
			<RouterView />
		</main>

		<footer class="p-4 bg-secondary text-primary text-center">
			<p>&copy; 2026 Infirmary Master. All rights reserved.</p>
		</footer>
	</div>
</template>

<style scoped>
/* Add any additional styles here if needed */
</style>
