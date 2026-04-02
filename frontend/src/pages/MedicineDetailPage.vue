<template>
	<div class="medicine-detail-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Medicine Details</h1>
		</header>
		<div class="max-w-2xl mx-auto bg-white p-6 rounded shadow">
			<figure class="mb-6">
				<img
					:src="medicine.image"
					alt="Medicine Image"
					class="rounded"
				/>
			</figure>
			<h2 class="text-2xl font-bold mb-4">{{ medicine.name }}</h2>
			<p class="text-secondary mb-4">{{ medicine.description }}</p>
			<p class="text-gray-700">Dosage: {{ medicine.dosage }}</p>
			<p class="text-gray-700">
				Side Effects: {{ medicine.sideEffects }}
			</p>
		</div>
	</div>
</template>

<script>
export default {
	name: 'MedicineDetailPage',
	data() {
		return {
			medicine: {
				id: 1,
				name: 'Paracetamol',
				description: 'Pain reliever and fever reducer.',
				image: 'https://via.placeholder.com/300',
				dosage: '500mg every 4-6 hours',
				sideEffects: 'Nausea, rash, liver damage (rare)',
			},
		};
	},
};
</script>

<style scoped>
/* Add any specific styles for the medicine detail page here */
</style>
