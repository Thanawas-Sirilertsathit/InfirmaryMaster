<template>
	<div class="inventory-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Inventory</h1>
			<p class="text-secondary mt-4">
				Overview of all medicines in stock.
			</p>
		</header>
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6 px-4">
			<div
				v-for="item in inventory"
				:key="item?.id"
				class="card bg-base-100 shadow-md"
			>
				<figure>
					<img
						:src="item?.image"
						:alt="item?.name || 'Medicine Image'"
						onerror="
							this.onerror = null;
							this.src = 'default-image-path.jpg';
						"
					/>
				</figure>
				<div class="card-body">
					<h2 class="card-title">{{ item?.name }}</h2>
					<p>Amount: {{ item?.amount }}</p>
					<p>Expiration Date: {{ item?.expirationDate }}</p>
					<div class="card-actions justify-end">
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
				class="card bg-base-100 shadow-md flex items-center justify-center"
			>
				<button class="btn btn-primary" @click="showAddModal = true">
					Add Medicine Batch
				</button>
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

const token = localStorage.getItem('authToken'); // Retrieve token from local storage or other secure storage

export default {
	name: 'InventoryPage',
	components: {
		AddMedicineBatchModal,
		ConfirmRemoveModal,
	},
	data() {
		return {
			inventory: [],
			showAddModal: false,
			showRemoveModal: false,
			newBatch: {
				name: '',
				amount: 0,
				expDate: '',
			},
			batchToRemove: null,
			medicineList: [],
		};
	},
	methods: {
		async fetchInventory() {
			try {
				const response = await axios.get(
					'http://localhost:8000/api/inventory/batches/list/',
					{
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);
				console.log('Inventory API Response:', response.data); // Debugging log
				this.inventory = Array.isArray(response.data.results)
					? response.data.results.map((item) => ({
							id: item.id,
							name: item.medicine_name,
							amount: item.quantity,
							expirationDate: item.expiration_date,
							image: item.medicine_image,
						}))
					: [];
			} catch (error) {
				console.error('Error fetching inventory:', error);
			}
		},
		async fetchMedicineList() {
			try {
				const response = await axios.get(
					'http://localhost:8000/api/medicines/list/',
					{
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);
				console.log('Medicine List API Response:', response.data); // Debugging log
				this.medicineList = Array.isArray(response.data.results)
					? response.data.results // Keep full objects (id and name)
					: [];
				console.log('Populated Medicine List:', this.medicineList); // Debugging log
			} catch (error) {
				console.error('Error fetching medicine list:', error);
			}
		},
		async removeItem(id) {
			if (confirm('Are you sure you want to remove this item?')) {
				try {
					const response = await axios.delete(
						`http://localhost:8000/api/inventory/batches/${id}/delete/`,
						{
							headers: {
								Accept: 'application/json',
								Authorization: `Bearer ${token}`,
							},
						},
					);
					console.log('Batch removed successfully:', response.data);
					this.fetchInventory(); // Refresh inventory after removal
				} catch (error) {
					console.error('Error removing batch:', error);
				}
			}
		},
		async addMedicineBatch(batch) {
			try {
				const payload = {
					medicine: this.medicineList.find(
						(med) => med.name === batch.name,
					)?.id, // Map name to ID
					quantity: batch.amount,
					expiration_date: batch.expDate,
				};
				console.log('Payload to be sent:', payload); // Debugging log
				const response = await axios.post(
					'http://localhost:8000/api/inventory/batches/',
					payload,
					{
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);
				console.log('Batch added successfully:', response.data);
				this.fetchInventory(); // Refresh inventory after adding
			} catch (error) {
				console.error('Error adding medicine batch:', error);
			}
			this.showAddModal = false;
		},
		confirmRemove() {
			console.log('Removing batch:', this.batchToRemove);
			this.showRemoveModal = false;
		},
	},
	created() {
		this.fetchInventory();
		this.fetchMedicineList();
	},
};
</script>

<style scoped>
/* Add any specific styles for the inventory page here */
</style>
