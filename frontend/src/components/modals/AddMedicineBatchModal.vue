<template>
	<div v-if="isOpen" class="modal modal-open">
		<div class="modal-box">
			<h3 class="font-bold text-lg">Add Medicine Batch</h3>
			<form @submit.prevent="submitForm">
				<div class="form-control">
					<label class="label">Medicine Name</label>
					<input
						v-model="newBatch.name"
						class="input input-bordered"
					/>
				</div>
				<div class="form-control">
					<label class="label">Amount</label>
					<input
						v-model="newBatch.amount"
						type="number"
						class="input input-bordered"
					/>
				</div>
				<div class="form-control">
					<label class="label">Expiration Date</label>
					<input
						v-model="newBatch.expDate"
						type="date"
						class="input input-bordered"
					/>
				</div>
				<div class="modal-action">
					<button type="submit" class="btn btn-primary">Add</button>
					<button @click="closeModal" class="btn">Cancel</button>
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
			newBatch: {
				name: '',
				amount: 0,
				expDate: '',
			},
		};
	},
	methods: {
		submitForm() {
			this.$emit('add-batch', this.newBatch);
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
