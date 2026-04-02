<template>
	<div class="p-4">
		<h1 class="text-2xl font-bold mb-4">Create Prescription</h1>
		<form @submit.prevent="submitForm">
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Patient Name</span>
				</label>
				<input
					v-model="patientName"
					type="text"
					placeholder="Enter patient name"
					class="input input-bordered"
					required
				/>
			</div>
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Medicine</span>
				</label>
				<input
					v-model="medicine"
					type="text"
					placeholder="Enter medicine"
					class="input input-bordered"
					required
				/>
			</div>
			<div class="form-control mb-4">
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
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Instructions</span>
				</label>
				<textarea
					v-model="instructions"
					placeholder="Enter instructions"
					class="textarea textarea-bordered"
					required
				></textarea>
			</div>
			<button type="submit" class="btn btn-primary">
				Create Prescription
			</button>
		</form>
	</div>
</template>

<script>
export default {
	data() {
		return {
			patientName: '',
			medicine: '',
			dosage: '',
			instructions: '',
		};
	},
	methods: {
		submitForm() {
			const prescription = {
				patientName: this.patientName,
				medicine: this.medicine,
				dosage: this.dosage,
				instructions: this.instructions,
			};
			// Replace with actual API call
			console.log('Prescription created:', prescription);
			this.$router.push('/prescriptions');
		},
	},
};
</script>

<style scoped></style>
