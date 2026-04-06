<template>
	<div v-if="isOpen" class="modal modal-open">
		<div class="modal-box">
			<h3 class="font-bold text-lg">Add New Medicine</h3>
			<form @submit.prevent="submitForm">
				<div class="form-control">
					<label class="label">
						<span class="label-text">Medicine Name</span>
					</label>
					<input
						v-model="medicineName"
						type="text"
						placeholder="Enter medicine name"
						class="input input-bordered"
						required
					/>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Description</span>
					</label>
					<textarea
						v-model="description"
						placeholder="Enter description"
						class="textarea textarea-bordered"
						required
					></textarea>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Category</span>
					</label>
					<select
						v-model="category"
						class="select select-bordered"
						required
					>
						<option value="">Select category</option>
						<option value="powder">Powder</option>
						<option value="liquid">Liquid</option>
						<option value="pill">Pill</option>
						<option value="capsule">Capsule</option>
					</select>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Dosage</span>
					</label>
					<input
						v-model="dosage"
						type="text"
						placeholder="Enter dosage"
						class="input input-bordered"
						required
					/>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Minimum Stock</span>
					</label>
					<input
						v-model="minimumStock"
						type="number"
						placeholder="Enter minimum stock"
						class="input input-bordered"
						required
					/>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Image URL</span>
					</label>
					<input
						v-model="image"
						type="url"
						placeholder="Enter image URL"
						class="input input-bordered"
						required
					/>
				</div>
				<div class="form-control">
					<label class="label">
						<span class="label-text">Side Effects</span>
					</label>
					<textarea
						v-model="sideEffects"
						placeholder="Enter side effects"
						class="textarea textarea-bordered"
						required
					></textarea>
				</div>
				<div class="modal-action">
					<button type="submit" class="btn btn-primary">Add</button>
					<button type="button" class="btn" @click="closeModal">
						Cancel
					</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		isOpen: {
			type: Boolean,
			required: true,
		},
	},
	data() {
		return {
			medicineName: '',
			description: '',
			category: '',
			dosage: '',
			minimumStock: '',
			image: '',
			sideEffects: '',
		};
	},
	methods: {
		submitForm() {
			if (!this.category || typeof this.category !== 'string') {
				alert('Please select a valid category.');
				return;
			}
			const newMedicine = {
				name: this.medicineName,
				description: this.description,
				category: this.category,
				dosage: this.dosage,
				minimum_stock: this.minimumStock,
				image: this.image,
				side_effects: this.sideEffects,
			};
			this.$emit('add-medicine', newMedicine);
			this.closeModal();
		},
		closeModal() {
			this.$emit('close');
		},
	},
};
</script>

<style scoped>
.modal {
	display: flex;
	align-items: center;
	justify-content: center;
}
</style>
