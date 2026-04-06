<template>
	<div class="medicine-detail-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Medicine Details</h1>
		</header>
		<div class="max-w-2xl mx-auto">
			<button
				@click="$router.push('/medicine')"
				class="btn btn-primary mb-6"
			>
				Back to Medicine List
			</button>
			<div v-if="loading" class="text-center py-10">
				<p>Loading medicine details...</p>
			</div>
			<div v-else-if="error" class="text-center py-10 text-red-500">
				<p>{{ error }}</p>
			</div>
			<div v-else class="bg-white p-6 rounded shadow">
				<figure class="mb-6">
					<img
						:src="medicine.image"
						alt="Medicine Image"
						class="rounded"
					/>
				</figure>
				<h2 class="text-2xl font-bold mb-4">{{ medicine.name }}</h2>
				<p class="text-gray-700 mb-4">{{ medicine.description }}</p>
				<p class="text-gray-700">Dosage: {{ medicine.dosage }}</p>
				<p class="text-gray-700">
					Minimum Stock: {{ medicine.minimum_stock }}
				</p>
				<p class="text-gray-700">Category: {{ medicine.category }}</p>
				<p class="text-gray-700">
					Side Effects:
					{{ medicine.side_effects || 'No side effects listed.' }}
				</p>
				<p class="text-gray-700">
					Created At:
					{{ new Date(medicine.created_at).toLocaleString() }}
				</p>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
	name: 'MedicineDetailPage',
	setup() {
		const route = useRoute();
		const medicine = ref(null);
		const error = ref(null);
		const loading = ref(true);

		const fetchMedicine = async (id) => {
			loading.value = true;
			error.value = null;
			try {
				const token = localStorage.getItem('authToken');
				if (!token) {
					throw new Error(
						'Authentication token is missing. Please log in.',
					);
				}
				const response = await axios.get(
					`http://localhost:8000/api/medicines/${id}/`,
					{
						headers: {
							Authorization: `Bearer ${token}`,
						},
					},
				);
				medicine.value = response.data;
			} catch (err) {
				error.value =
					'Failed to load medicine details. Please try again later.';
				console.error(err);
			} finally {
				loading.value = false;
			}
		};

		onMounted(() => {
			const medicineId = route.params.id; // Get dynamic ID from route params
			fetchMedicine(medicineId);
		});

		return {
			medicine,
			error,
			loading,
		};
	},
};
</script>

<style scoped>
/* Add any specific styles for the medicine detail page here */
</style>
