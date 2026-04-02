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
				:key="item.id"
				class="card bg-base-100 shadow-md"
			>
				<figure>
					<img :src="item.image" alt="Medicine Image" />
				</figure>
				<div class="card-body">
					<h2 class="card-title">{{ item.name }}</h2>
					<p>Amount: {{ item.amount }}</p>
					<div class="card-actions justify-end">
						<button
							class="btn btn-error"
							@click="removeItem(item.id)"
						>
							Remove
						</button>
					</div>
				</div>
			</div>
		</div>

		<AddMedicineBatchModal
			:isOpen="showAddModal"
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

export default {
	name: 'InventoryPage',
	components: {
		AddMedicineBatchModal,
		ConfirmRemoveModal,
	},
	data() {
		return {
			inventory: [
				{
					id: 1,
					name: 'Paracetamol',
					amount: 100,
					image: 'https://via.placeholder.com/150',
				},
				{
					id: 2,
					name: 'Ibuprofen',
					amount: 50,
					image: 'https://via.placeholder.com/150',
				},
				{
					id: 3,
					name: 'Amoxicillin',
					amount: 75,
					image: 'https://via.placeholder.com/150',
				},
			],
			showAddModal: false,
			showRemoveModal: false,
			newBatch: {
				name: '',
				amount: 0,
				expDate: '',
			},
			batchToRemove: null,
		};
	},
	methods: {
		removeItem(id) {
			if (confirm('Are you sure you want to remove this item?')) {
				this.inventory = this.inventory.filter(
					(item) => item.id !== id,
				);
			}
		},
		addMedicineBatch(batch) {
			console.log('Adding batch:', batch);
			this.showAddModal = false;
		},
		confirmRemove() {
			console.log('Removing batch:', this.batchToRemove);
			this.showRemoveModal = false;
		},
	},
};
</script>

<style scoped>
/* Add any specific styles for the inventory page here */
</style>
