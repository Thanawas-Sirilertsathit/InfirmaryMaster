<template>
	<div class="patient-prescription-detail-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">
				Prescription Details
			</h1>
		</header>
		<div class="max-w-2xl mx-auto bg-white p-6 rounded shadow">
			<h2 class="text-2xl font-bold mb-4">
				Prescription ID: {{ prescription.id }}
			</h2>
			<p class="text-secondary mb-4">Date: {{ prescription.date }}</p>
			<p class="text-gray-700 mb-4">
				Doctor:
				{{
					prescription.doctor ||
					prescription.prescribed_by_name ||
					'-'
				}}
			</p>
			<h3 class="text-xl font-bold mb-2">Medicines:</h3>
			<ul class="list-disc pl-6">
				<li
					v-for="medicine in prescription.medicines"
					:key="medicine.id"
				>
					{{ medicine.name }} - {{ medicine.dosage }}
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	name: 'PatientPrescriptionDetailPage',
	data() {
		return {
			prescription: null,
		};
	},
	created() {
		this.fetchPrescriptionDetails();
	},
	methods: {
		async fetchPrescriptionDetails() {
			const prescriptionId = this.$route.params.id;
			try {
				const response = await axios.get(
					`http://localhost:8000/api/prescriptions/${prescriptionId}/`,
				);
				this.prescription = response.data;
			} catch (error) {
				console.error('Error fetching prescription details:', error);
			}
		},
	},
};
</script>

<style scoped>
/* Add any specific styles for the patient prescription detail page here */
</style>
