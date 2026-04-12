<template>
	<div class="inventory-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Inventory</h1>
			<p class="text-secondary mt-4">
				Overview of all medicines in stock.
			</p>
		</header>

		<div
			class="mx-auto mb-6 flex max-w-2xl flex-col gap-3 px-4 md:flex-row md:items-center"
		>
			<input
				v-model.trim="searchQuery"
				type="text"
				placeholder="Search inventory by medicine name or description..."
				class="input input-bordered w-full md:flex-grow"
				@keyup.enter="applySearch"
			/>
			<button class="btn btn-outline" @click="applySearch">Search</button>
			<button
				v-if="searchQuery"
				class="btn border-black bg-white text-red-600 hover:border-black hover:bg-red-50 hover:text-red-700"
				@click="clearSearch"
			>
				Clear
			</button>
		</div>

		<div v-if="loading" class="py-10 text-center">
			<p>Loading inventory...</p>
		</div>
		<div v-else-if="error" class="py-10 text-center text-red-500">
			<p>{{ error }}</p>
		</div>
		<div v-else>
			<div class="grid grid-cols-1 gap-6 px-4 md:grid-cols-3">
				<div
					v-for="item in inventory"
					:key="item?.id"
					class="inventory-card card h-full overflow-hidden bg-base-100 shadow-md"
				>
					<figure class="h-56 w-full bg-base-200">
						<img
							:src="item?.image"
							:alt="item?.name || 'Medicine Image'"
							class="h-full w-full object-cover"
							onerror="
								this.onerror = null;
								this.src = 'default-image-path.jpg';
							"
						/>
					</figure>
					<div class="card-body flex h-full flex-col">
						<h2 class="card-title">{{ item?.name }}</h2>
						<p>Amount: {{ item?.amount }}</p>
						<p>Expiration Date: {{ item?.expirationDate }}</p>
						<div class="card-actions mt-auto justify-end">
							<button
								class="btn btn-error"
								@click="removeItem(item?.id)"
							>
								Remove
							</button>
						</div>
					</div>
				</div>

				<!-- Add Medicine Batch Card -->
				<div
					class="inventory-card card flex h-full min-h-80 items-center justify-center bg-base-100 shadow-md"
				>
					<button
						class="btn btn-primary"
						@click="showAddModal = true"
					>
						Add Medicine Batch
					</button>
				</div>
			</div>

			<p
				v-if="!inventory.length"
				class="px-4 py-8 text-center text-gray-500"
			>
				No inventory items found.
			</p>

			<div
				class="mx-auto mt-6 flex max-w-6xl items-center justify-between gap-4 px-4"
			>
				<p class="text-sm text-gray-600">
					Page {{ currentPage }} of {{ totalPages }}
					<span v-if="totalCount">({{ totalCount }} batches)</span>
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

		<AddMedicineBatchModal
			:isOpen="showAddModal"
			:medicineList="medicineList"
			@add-batch="addMedicineBatch"
			@close="showAddModal = false"
		/>

		<ConfirmRemoveModal
			:isOpen="showRemoveModal"
			@confirm-remove="confirmRemove"
			@close="showRemoveModal = false"
		/>
	</div>
</template>

<script>
import AddMedicineBatchModal from '@/components/modals/AddMedicineBatchModal.vue';
import ConfirmRemoveModal from '@/components/modals/ConfirmRemoveModal.vue';
import axios from 'axios';

export default {
	name: 'InventoryPage',
	components: {
		AddMedicineBatchModal,
		ConfirmRemoveModal,
	},
	computed: {
		totalPages() {
			return Math.max(1, Math.ceil(this.totalCount / this.pageSize));
		},
	},
	data() {
		return {
			inventory: [],
			loading: false,
			error: null,
			showAddModal: false,
			showRemoveModal: false,
			searchQuery: '',
			currentPage: 1,
			totalCount: 0,
			hasNext: false,
			hasPrevious: false,
			pageSize: 20,
			batchToRemove: null,
			medicineList: [],
		};
	},
	methods: {
		getAuthHeaders() {
			const authToken = localStorage.getItem('authToken');

			if (!authToken) {
				throw new Error(
					'Authentication token is missing. Please log in.',
				);
			}

			return {
				Accept: 'application/json',
				Authorization: `Bearer ${authToken}`,
			};
		},
		mapInventory(results) {
			return results.map((item) => ({
				id: item.id,
				name: item.medicine_name,
				amount: item.quantity,
				expirationDate: item.expiration_date,
				image: item.medicine_image,
			}));
		},
		async fetchInventory(page = 1) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					'http://localhost:8000/api/inventory/batches/list/',
					{
						params: {
							page,
							search: this.searchQuery || undefined,
						},
						headers: this.getAuthHeaders(),
					},
				);
				const results = Array.isArray(response.data.results)
					? response.data.results
					: [];

				this.inventory = this.mapInventory(results);
				this.currentPage = page;
				this.totalCount = Number.isInteger(response.data.count)
					? response.data.count
					: results.length;
				this.hasNext = Boolean(response.data.next);
				this.hasPrevious = Boolean(response.data.previous);
			} catch (error) {
				this.error =
					'Failed to load inventory. Please try again later.';
				console.error('Error fetching inventory:', error);
				this.inventory = [];
				this.totalCount = 0;
				this.hasNext = false;
				this.hasPrevious = false;
			} finally {
				this.loading = false;
			}
		},
		async fetchMedicineList() {
			try {
				let nextUrl = 'http://localhost:8000/api/medicines/list/';
				const medicines = [];

				while (nextUrl) {
					const response = await axios.get(nextUrl, {
						headers: this.getAuthHeaders(),
					});
					const results = Array.isArray(response.data.results)
						? response.data.results
						: [];

					medicines.push(...results);
					nextUrl = response.data.next;
				}

				this.medicineList = medicines;
			} catch (error) {
				console.error('Error fetching medicine list:', error);
			}
		},
		removeItem(id) {
			this.batchToRemove = id; // Set the batch to remove
			this.showRemoveModal = true; // Show the ConfirmRemoveModal
		},
		async confirmRemove() {
			if (this.batchToRemove) {
				try {
					const response = await axios.delete(
						`http://localhost:8000/api/inventory/batches/${this.batchToRemove}/delete/`,
						{
							headers: this.getAuthHeaders(),
						},
					);
					console.log('Batch removed successfully:', response.data);
					const fallbackPage =
						this.inventory.length === 1 && this.currentPage > 1
							? this.currentPage - 1
							: this.currentPage;
					await this.fetchInventory(fallbackPage);
				} catch (error) {
					console.error('Error removing batch:', error);
				} finally {
					this.batchToRemove = null; // Reset the batch to remove
				}
			}
			this.showRemoveModal = false; // Close the ConfirmRemoveModal
		},
		async addMedicineBatch(batch) {
			try {
				const payload = {
					medicine: batch.medicineId,
					quantity: batch.amount,
					expiration_date: batch.expDate,
				};
				console.log('Payload to be sent:', payload); // Debugging log
				const response = await axios.post(
					'http://localhost:8000/api/inventory/batches/',
					payload,
					{
						headers: this.getAuthHeaders(),
					},
				);
				console.log('Batch added successfully:', response.data);
				await this.fetchInventory(1);
			} catch (error) {
				console.error('Error adding medicine batch:', error);
			}
			this.showAddModal = false;
		},
		applySearch() {
			this.fetchInventory(1);
		},
		clearSearch() {
			if (!this.searchQuery) {
				return;
			}

			this.searchQuery = '';
			this.fetchInventory(1);
		},
		changePage(page) {
			if (
				page < 1 ||
				page > this.totalPages ||
				page === this.currentPage
			) {
				return;
			}

			this.fetchInventory(page);
		},
	},
	created() {
		this.fetchInventory(1);
		this.fetchMedicineList();
	},
};
</script>

<style scoped>
.inventory-card {
	border: 1px solid #e5e7eb;
	box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease;
}

.inventory-card:hover {
	transform: translateY(-1px);
	border-color: #fda4af;
	box-shadow: 0 12px 24px rgba(244, 63, 94, 0.14);
}
</style>
