<template>
	<div class="p-4">
		<h1 class="text-2xl font-bold mb-4">Create Prescription</h1>
		<form @submit.prevent="submitForm">
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Patient First Name</span>
				</label>
				<input
					v-model="patientFirstName"
					type="text"
					placeholder="Enter patient first name"
					class="input input-bordered"
					required
				/>
			</div>
			<div class="form-control mb-4">
				<label class="label">
					<span class="label-text">Patient Last Name</span>
				</label>
				<input
					v-model="patientLastName"
					type="text"
					placeholder="Enter patient last name"
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
							<th class="px-4 py-2">Expiration Date</th>
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
								{{ formatDate(batch.expirationDate) }}
							</td>
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
import apiManager from '@/api/api_manager';

export default {
	data() {
		return {
			patientFirstName: '',
			patientLastName: '',
			medicineBatches: [],
			selectedMedicines: [],
			doctorName: '',
			notes: '',
		};
	},
	created() {
		this.fetchMedicineBatches();
	},
	methods: {
		goBackToPrescriptions() {
			this.$router.push('/prescriptions');
		},
		async fetchMedicineBatches() {
			try {
				const response = await apiManager.get(
					'/api/inventory/batches/list/',
					{
						headers: apiManager.getAuthHeaders(),
					},
				);
				this.medicineBatches = response.data.results.map((batch) => ({
					id: batch.id,
					name: batch.medicine_name,
					expirationDate: batch.expiration_date,
					availableAmount: batch.quantity,
					amountToAdd: 0,
				}));
			} catch (error) {
				console.error('Error fetching medicine batches:', error);
			}
		},
		formatDate(value) {
			if (!value) {
				return '-';
			}

			return new Date(value).toLocaleDateString();
		},
		addMedicine(batch) {
			if (
				batch.amountToAdd > 0 &&
				batch.amountToAdd <= batch.availableAmount
			) {
				this.selectedMedicines.push({
					batchId: batch.id,
					name: batch.name,
					amount: batch.amountToAdd,
					instruction: batch.instruction || '',
				});
				batch.availableAmount -= batch.amountToAdd;
				batch.amountToAdd = 0;
			} else {
				alert(
					`Invalid amount specified. Maximum available: ${batch.availableAmount}`,
				);
			}
		},
		async submitForm() {
			try {
				const payload = {
					patient_first_name: this.patientFirstName,
					patient_last_name: this.patientLastName,
					items: this.selectedMedicines.map((med) => ({
						batch_id: med.batchId,
						quantity: med.amount,
						instruction: med.instruction || '',
					})),
					notes: this.notes,
				};

				await apiManager.post('/api/prescriptions/', payload, {
					headers: apiManager.getAuthHeaders(),
				});
				this.$router.push('/prescriptions');
			} catch (error) {
				console.error('Error creating prescription:', error);
			}
		},
	},
};
</script>

<style scoped></style>
