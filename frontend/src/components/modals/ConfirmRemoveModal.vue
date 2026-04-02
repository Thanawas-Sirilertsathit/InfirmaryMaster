<template>
	<div v-if="isOpen" class="modal modal-open">
		<div class="modal-box">
			<h3 class="font-bold text-lg">Confirm Removal</h3>
			<p>Are you sure you want to remove this batch?</p>
			<div class="modal-action">
				<button @click="confirmRemove" class="btn btn-error">
					Remove
				</button>
				<button @click="closeModal" class="btn">Cancel</button>
			</div>
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
	methods: {
		confirmRemove() {
			this.$emit('confirm-remove');
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
