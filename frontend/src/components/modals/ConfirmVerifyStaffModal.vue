<template>
	<div v-if="isOpen" class="modal modal-open">
		<div class="modal-box">
			<h3 class="text-lg font-bold">Confirm Staff Verification</h3>
			<p class="py-2">
				Are you sure you want to verify
				<span class="font-semibold">{{
					staffName || 'this staff member'
				}}</span>
				?
			</p>
			<div class="modal-action">
				<button class="btn btn-primary" @click="confirmVerify">
					Verify
				</button>
				<button class="btn" @click="closeModal">Cancel</button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'ConfirmVerifyStaffModal',
	props: {
		isOpen: {
			type: Boolean,
			required: true,
		},
		staffName: {
			type: String,
			default: '',
		},
	},
	methods: {
		confirmVerify() {
			this.$emit('confirm-verify');
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
