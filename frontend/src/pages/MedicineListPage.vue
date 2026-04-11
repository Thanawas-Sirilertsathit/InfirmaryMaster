<template>
	<div class="medicine-list-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Medicine List</h1>
			<p class="text-secondary mt-4">
				Browse through the available medicines.
			</p>
		</header>
		<div v-if="loading" class="text-center py-10">
			<p>Loading medicines...</p>
		</div>
		<div v-else-if="error" class="text-center py-10 text-red-500">
			<p>{{ error }}</p>
		</div>
		<div v-else>
			<div class="form-control mb-6 max-w-md mx-auto">
				<input
					type="text"
					placeholder="Search medicines..."
					class="input input-bordered"
				/>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6 px-4">
				<div
					v-for="medicine in medicines"
					:key="medicine.id"
					class="card h-full overflow-hidden bg-base-100 shadow-md"
				>
					<figure class="h-56 w-full bg-base-200">
						<img
							:src="medicine.image"
							alt="Medicine Image"
							class="h-full w-full object-cover"
						/>
					</figure>
					<div class="card-body flex h-full flex-col">
						<h2 class="card-title">{{ medicine.name }}</h2>
						<p>{{ medicine.description }}</p>
						<div class="card-actions mt-auto justify-end">
							<router-link
								:to="`/medicine/${medicine.id}`"
								class="btn btn-primary"
								>Details</router-link
							>
						</div>
					</div>
				</div>

				<!-- Add Medicine Modal Trigger -->
				<div
					class="card flex h-full min-h-80 items-center justify-center bg-base-100 shadow-md"
				>
					<button
						class="btn btn-primary"
						@click="showAddModal = true"
					>
						Add New Medicine
					</button>
				</div>
			</div>

			<AddMedicineModal
				:isOpen="showAddModal"
				@add-medicine="addMedicine"
				@close="showAddModal = false"
			/>
		</div>
	</div>
</template>

<script>
import axios from 'axios';
import AddMedicineModal from '@/components/modals/AddMedicineModal.vue';
import { ref, onMounted } from 'vue';

export default {
	name: 'MedicineListPage',
	components: {
		AddMedicineModal,
	},
	setup() {
		const medicines = ref([]);
		const loading = ref(true);
		const error = ref(null);
		const showAddModal = ref(false);

		const fetchMedicines = async () => {
			loading.value = true;
			error.value = null;
			medicines.value = []; // Clear the medicines array before fetching new data
			console.log('Fetching medicines...'); // Debugging log
			try {
				const token = localStorage.getItem('authToken'); // Retrieve the token from localStorage
				if (!token) {
					throw new Error(
						'Authentication token is missing. Please log in.',
					);
				}
				const response = await axios.get(
					'http://localhost:8000/api/medicines/list/?page=1',
					{
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`, // Include the token in the Authorization header
						},
					},
				); // Updated to match Swagger example
				console.log('API response:', response.data); // Debugging log
				if (Array.isArray(response.data.results)) {
					medicines.value = response.data.results.map((medicine) => ({
						id: medicine.id,
						name: medicine.name,
						description: medicine.description,
						category: medicine.category_name,
						dosage: medicine.dosage,
						minimum_stock: medicine.minimum_stock,
						image:
							medicine.image || 'https://via.placeholder.com/150',
						side_effects:
							medicine.side_effects || 'No side effects listed.',
					}));
					console.log('Mapped medicines:', medicines.value); // Debugging log
				} else {
					error.value = 'Invalid data received from the server.';
					console.error('Invalid data format:', response.data); // Debugging log
				}
			} catch (err) {
				error.value =
					'Failed to load medicines. Please try again later.';
				console.error('API call failed:', err); // Debugging log
			} finally {
				loading.value = false;
			}
		};

		const addMedicine = async (newMedicine) => {
			console.log('Adding new medicine:', newMedicine);
			try {
				const token = localStorage.getItem('authToken'); // Retrieve the token from localStorage
				if (!token) {
					throw new Error(
						'Authentication token is missing. Please log in.',
					);
				}
				await axios.post(
					'http://localhost:8000/api/medicines/', // Added trailing slash to match Django's APPEND_SLASH behavior
					newMedicine,
					{
						headers: {
							Authorization: `Bearer ${token}`, // Include the token in the Authorization header
						},
					},
				);
				await fetchMedicines();
			} catch (err) {
				error.value = 'Failed to add medicine. Please try again later.';
				console.error(err);
			}
			showAddModal.value = false;
		};

		onMounted(fetchMedicines);

		return {
			medicines,
			loading,
			error,
			showAddModal,
			fetchMedicines,
			addMedicine,
		};
	},
};
</script>

<style scoped></style>
