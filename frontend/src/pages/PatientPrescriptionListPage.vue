<template>
	<div class="patient-prescription-list-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">My Prescriptions</h1>
			<p class="text-secondary mt-4">
				View and manage your prescriptions.
			</p>
		</header>
		<div class="form-control mb-6 max-w-md mx-auto">
			<input
				type="text"
				placeholder="Search prescriptions..."
				class="input input-bordered"
			/>
		</div>
		<table
			class="table-auto w-full max-w-4xl mx-auto bg-white shadow-md rounded"
		>
			<thead>
				<tr>
					<th class="px-4 py-2">Prescription ID</th>
					<th class="px-4 py-2">Date</th>
					<th class="px-4 py-2">Doctor</th>
					<th class="px-4 py-2">Actions</th>
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="prescription in prescriptions"
					:key="prescription.id"
				>
					<td class="border px-4 py-2">{{ prescription.id }}</td>
					<td class="border px-4 py-2">{{ prescription.date }}</td>
					<td class="border px-4 py-2">{{ prescription.doctor }}</td>
					<td class="border px-4 py-2">
						<router-link
							:to="`/prescription/${prescription.id}`"
							class="btn btn-primary btn-sm"
							>View</router-link
						>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	name: 'PatientPrescriptionListPage',
	data() {
		return {
			prescriptions: [],
		};
	},
	created() {
		this.fetchPrescriptions();
	},
	methods: {
		async fetchPrescriptions() {
			try {
				const response = await axios.get(
					'http://localhost:8000/api/prescriptions/',
				);
				this.prescriptions = response.data;
			} catch (error) {
				console.error('Error fetching prescriptions:', error);
			}
		},
	},
};
</script>

<style scoped>
/* Add any specific styles for the patient prescription list page here */
</style>
