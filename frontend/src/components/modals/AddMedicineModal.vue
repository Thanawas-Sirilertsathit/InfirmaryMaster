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
					<input
						v-model="category"
						type="text"
						placeholder="Enter category"
						class="input input-bordered"
						required
					/>
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
		};
	},
	methods: {
		submitForm() {
			const newMedicine = {
				name: this.medicineName,
				description: this.description,
				category: this.category,
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
