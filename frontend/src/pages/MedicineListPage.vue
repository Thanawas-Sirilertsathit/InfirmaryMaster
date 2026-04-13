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
			<div
				class="mb-6 mx-auto flex max-w-2xl flex-col gap-3 md:flex-row md:items-center"
			>
				<input
					v-model.trim="searchQuery"
					type="text"
					placeholder="Search medicines by name or description..."
					class="input input-bordered w-full md:flex-grow"
					@keyup.enter="applySearch"
				/>
				<button class="btn btn-outline" @click="applySearch">
					Search
				</button>
				<button
					v-if="searchQuery"
					class="btn border-black bg-white text-red-600 hover:border-black hover:bg-red-50 hover:text-red-700"
					@click="clearSearch"
				>
					Clear
				</button>
			</div>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6 px-4">
				<div
					v-for="medicine in medicines"
					:key="medicine.id"
					class="medicine-card card h-full overflow-hidden bg-base-100 shadow-md"
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

				<div
					class="medicine-card card flex h-full min-h-80 items-center justify-center bg-base-100 shadow-md"
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

			<div
				class="mx-auto mt-6 flex max-w-6xl items-center justify-between gap-4 px-4"
			>
				<p class="text-sm text-gray-600">
					Page {{ currentPage }} of {{ totalPages }}
					<span v-if="totalCount">({{ totalCount }} medicines)</span>
				</p>
				<div class="flex gap-2">
					<button
						class="btn btn-outline btn-sm"
						@click="changePage(currentPage - 1)"
						:disabled="!hasPrevious"
					>
						Previous
					</button>
					<button
						class="btn btn-outline btn-sm"
						@click="changePage(currentPage + 1)"
						:disabled="!hasNext"
					>
						Next
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import apiManager from '@/api/api_manager';
import AddMedicineModal from '@/components/modals/AddMedicineModal.vue';
import { computed, onMounted, ref } from 'vue';

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
		const searchQuery = ref('');
		const currentPage = ref(1);
		const totalCount = ref(0);
		const hasNext = ref(false);
		const hasPrevious = ref(false);
		const pageSize = ref(20);

		const mapMedicines = (results) =>
			results.map((medicine) => ({
				id: medicine.id,
				name: medicine.name,
				description: medicine.description,
				category: medicine.category_name,
				dosage: medicine.dosage,
				minimum_stock: medicine.minimum_stock,
				image: medicine.image || 'https://via.placeholder.com/150',
				side_effects:
					medicine.side_effects || 'No side effects listed.',
			}));

		const fetchMedicines = async (page = 1) => {
			loading.value = true;
			error.value = null;
			medicines.value = [];
			try {
				const response = await apiManager.get('/api/medicines/list/', {
					params: {
						page,
						search: searchQuery.value || undefined,
					},
					headers: apiManager.getAuthHeaders(),
				});
				if (Array.isArray(response.data.results)) {
					medicines.value = mapMedicines(response.data.results);
					currentPage.value = page;
					totalCount.value = Number.isInteger(response.data.count)
						? response.data.count
						: response.data.results.length;
					hasNext.value = Boolean(response.data.next);
					hasPrevious.value = Boolean(response.data.previous);
				} else {
					error.value = 'Invalid data received from the server.';
					console.error('Invalid data format:', response.data);
				}
			} catch (err) {
				error.value =
					'Failed to load medicines. Please try again later.';
				console.error('API call failed:', err);
			} finally {
				loading.value = false;
			}
		};

		const applySearch = () => {
			fetchMedicines(1);
		};

		const clearSearch = () => {
			if (!searchQuery.value) {
				return;
			}

			searchQuery.value = '';
			fetchMedicines(1);
		};

		const changePage = (page) => {
			const totalPages = Math.max(
				1,
				Math.ceil(totalCount.value / pageSize.value),
			);

			if (page < 1 || page > totalPages || page === currentPage.value) {
				return;
			}

			fetchMedicines(page);
		};

		const addMedicine = async (newMedicine) => {
			try {
				await apiManager.post('/api/medicines/', newMedicine, {
					headers: apiManager.getAuthHeaders(),
				});
				await fetchMedicines(1);
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
			searchQuery,
			currentPage,
			totalCount,
			hasNext,
			hasPrevious,
			totalPages: computed(() =>
				Math.max(1, Math.ceil(totalCount.value / pageSize.value)),
			),
			fetchMedicines,
			applySearch,
			clearSearch,
			changePage,
			addMedicine,
		};
	},
};
</script>
