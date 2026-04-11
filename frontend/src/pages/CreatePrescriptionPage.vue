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
					<span class="label-text">Medicines</span>
				</label>
				<table class="table-auto w-full bg-white shadow-md rounded">
					<thead>
						<tr>
							<th class="px-4 py-2">Batch ID</th>
							<th class="px-4 py-2">Medicine Name</th>
							<th class="px-4 py-2">Available Amount</th>
							<th class="px-4 py-2">Amount to Add</th>
							<th class="px-4 py-2">Actions</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="batch in medicineBatches" :key="batch.id">
							<td class="border px-4 py-2">{{ batch.id }}</td>
							<td class="border px-4 py-2">{{ batch.name }}</td>
							<td class="border px-4 py-2">
								{{ batch.availableAmount }}
							</td>
							<td class="border px-4 py-2">
								<input
									type="number"
									v-model.number="batch.amountToAdd"
									class="input input-bordered w-full"
									:min="0"
									:max="batch.availableAmount"
								/>
							</td>
							<td class="border px-4 py-2">
								<button
									class="btn btn-primary btn-sm"
									@click="addMedicine(batch)"
									type="button"
								>
									Add Medicine
								</button>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Doctor Name</span>
				</label>
				<input
					v-model="doctorName"
					type="text"
					placeholder="Enter doctor name"
					class="input input-bordered"
					required
				/>
			</div>
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Notes</span>
				</label>
				<textarea
					v-model="notes"
					placeholder="Enter notes"
					class="textarea textarea-bordered"
					required
				></textarea>
			</div>
			<div class="flex items-center gap-3">
				<button type="submit" class="btn btn-primary">
					Create Prescription
				</button>
				<button
					type="button"
					class="btn btn-outline"
					@click="goBackToPrescriptions"
				>
					Back to Prescriptions
				</button>
			</div>
		</form>
	</div>
</template>

<script>
import axios from 'axios';

const token = localStorage.getItem('authToken'); // Retrieve token from local storage

export default {
	data() {
		return {
			patientName: '',
			medicineBatches: [], // List of medicine batches
			selectedMedicines: [], // List of selected medicines with amounts
			doctorName: '', // Added doctor name field
			notes: '', // Changed from instructions to notes
		};
	},
	created() {
		this.fetchMedicineBatches(); // Fetch medicine batches on page load
	},
	methods: {
		goBackToPrescriptions() {
			this.$router.push('/prescriptions');
		},
		async fetchMedicineBatches() {
			try {
				const response = await axios.get(
					'http://localhost:8000/api/inventory/batches/list/',
					{
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);
				this.medicineBatches = response.data.results.map((batch) => ({
					id: batch.id,
					name: batch.medicine_name,
					availableAmount: batch.quantity,
					amountToAdd: 0, // Default amount to add
				}));
			} catch (error) {
				console.error('Error fetching medicine batches:', error);
			}
		},
		addMedicine(batch) {
			if (
				batch.amountToAdd > 0 && // Ensure amount is greater than 0
				batch.amountToAdd <= batch.availableAmount // Ensure amount does not exceed available stock
			) {
				this.selectedMedicines.push({
					batchId: batch.id,
					name: batch.name,
					amount: batch.amountToAdd,
					instruction: batch.instruction || '', // Ensure instruction is included
				});
				batch.availableAmount -= batch.amountToAdd; // Update available stock
				batch.amountToAdd = 0; // Reset input field
			} else {
				alert(
					`Invalid amount specified. Maximum available: ${batch.availableAmount}`,
				);
			}
		},
		async submitForm() {
			try {
				const payload = {
					patient_name: this.patientName, // Send patient name instead of ID
					items: this.selectedMedicines.map((med) => ({
						batch_id: med.batchId, // Send batch ID instead of medicine ID
						quantity: med.amount, // Send quantity
						instruction: med.instruction || '', // Include instruction
					})),
					notes: this.notes, // Include notes
				};

				console.log('Selected Medicines:', this.selectedMedicines); // Debug log to inspect selected medicines
				console.log('Payload being sent:', payload); // Debug log to inspect payload

				const response = await axios.post(
					'http://localhost:8000/api/prescriptions/', // Correct endpoint
					payload,
					{
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);
				console.log(
					'Prescription created successfully:',
					response.data,
				);
				this.$router.push('/prescriptions'); // Redirect to prescriptions list
			} catch (error) {
				console.error('Error creating prescription:', error);
			}
		},
	},
};
</script>

<style scoped></style>
