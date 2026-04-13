<template>
	<div class="medicine-detail-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Medicine Details</h1>
		</header>
		<div class="max-w-2xl mx-auto">
			<div
				class="mb-6 flex flex-col gap-3 sm:flex-row sm:justify-between"
			>
				<button
					@click="$router.push('/medicine')"
					class="btn btn-primary"
				>
					Back to Medicine List
				</button>
				<button
					v-if="medicine"
					class="btn btn-outline"
					@click="showEditModal = true"
				>
					Edit Medicine
				</button>
			</div>
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

			<EditMedicineModal
				:isOpen="showEditModal"
				:medicine="medicine"
				@save="updateMedicine"
				@close="showEditModal = false"
			/>
		</div>
	</div>
</template>

<script>
import apiManager from '@/api/api_manager';
import EditMedicineModal from '@/components/modals/EditMedicineModal.vue';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
	name: 'MedicineDetailPage',
	components: {
		EditMedicineModal,
	},
	setup() {
		const route = useRoute();
		const medicine = ref(null);
		const error = ref(null);
		const loading = ref(true);
		const showEditModal = ref(false);

		const getAuthHeaders = () => {
			return apiManager.getAuthHeaders();
		};

		const fetchMedicine = async (id) => {
			loading.value = true;
			error.value = null;
			try {
				const response = await apiManager.get(`/api/medicines/${id}/`, {
					headers: getAuthHeaders(),
				});
				medicine.value = response.data;
			} catch (err) {
				error.value =
					'Failed to load medicine details. Please try again later.';
				console.error(err);
			} finally {
				loading.value = false;
			}
		};

		const updateMedicine = async (payload) => {
			error.value = null;
			try {
				const medicineId = route.params.id;
				const response = await apiManager.put(
					`/api/medicines/${medicineId}/`,
					payload,
					{
						headers: getAuthHeaders(),
					},
				);

				medicine.value = response.data;
				showEditModal.value = false;
			} catch (err) {
				error.value = 'Failed to update medicine details.';
				console.error(err);
			}
		};

		onMounted(() => {
			const medicineId = route.params.id;
			fetchMedicine(medicineId);
		});

		return {
			medicine,
			error,
			loading,
			showEditModal,
			updateMedicine,
		};
	},
};
</script>

<style scoped></style>
