<template>
	<div class="medicine-list-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Medicine List</h1>
			<p class="text-secondary mt-4">
				Browse through the available medicines.
			</p>
		</header>
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
				class="card bg-base-100 shadow-md"
			>
				<figure>
					<img :src="medicine.image" alt="Medicine Image" />
				</figure>
				<div class="card-body">
					<h2 class="card-title">{{ medicine.name }}</h2>
					<p>{{ medicine.description }}</p>
					<div class="card-actions justify-end">
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
				class="card bg-base-100 shadow-md flex items-center justify-center"
			>
				<button class="btn btn-primary" @click="showAddModal = true">
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
</template>

<script>
import axios from 'axios';
import AddMedicineModal from '@/components/modals/AddMedicineModal.vue';

export default {
	name: 'MedicineListPage',
	components: {
		AddMedicineModal,
	},
	data() {
		return {
			medicines: [],
			showAddModal: false,
		};
	},
	methods: {
		addMedicine(newMedicine) {
			console.log('Adding new medicine:', newMedicine);
			this.medicines.push({
				id: this.medicines.length + 1,
				...newMedicine,
				image: 'https://via.placeholder.com/150',
			});
			this.showAddModal = false;
		},
	},
};
</script>

<style scoped></style>
