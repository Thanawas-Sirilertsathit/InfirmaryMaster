<template>
	<div class="patient-prescription-detail-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">
				Prescription Details
			</h1>
		</header>
		<div class="max-w-4xl mx-auto px-4 pb-10">
			<button @click="goBackToPrescriptions" class="btn btn-outline mb-6">
				Back to Prescriptions
			</button>

			<div
				v-if="loading"
				class="detail-card bg-white p-6 rounded shadow text-center"
			>
				<p>Loading prescription details...</p>
			</div>

			<div
				v-else-if="error"
				class="detail-card bg-white p-6 rounded shadow text-center text-red-500"
			>
				<p>{{ error }}</p>
			</div>

			<div v-else-if="prescription" class="space-y-6">
				<div class="detail-card bg-white p-6 rounded shadow">
					<div
						class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between"
					>
						<div>
							<p
								class="text-sm uppercase tracking-wide text-gray-500 mb-2"
							>
								Prescription Record
							</p>
							<h2 class="text-2xl font-bold text-gray-900">
								Prescription #{{ prescription.id }}
							</h2>
							<p class="text-secondary mt-2">
								Created
								{{ formatDateTime(prescription.created_at) }}
							</p>
						</div>
						<div
							class="badge badge-primary badge-outline self-start"
						>
							{{ itemCountLabel }}
						</div>
					</div>
				</div>

				<div class="grid gap-6 md:grid-cols-2">
					<div
						class="detail-card bg-white p-6 rounded shadow space-y-4"
					>
						<h3 class="text-xl font-bold">Prescription Summary</h3>
						<div>
							<p class="text-sm text-gray-500">Patient</p>
							<p class="text-gray-800 font-medium">
								{{ patientName }}
							</p>
						</div>
						<div>
							<p class="text-sm text-gray-500">Prescribed By</p>
							<p class="text-gray-800 font-medium">
								{{ doctorName }}
							</p>
						</div>
						<div>
							<p class="text-sm text-gray-500">Issue Date</p>
							<p class="text-gray-800 font-medium">
								{{ formatDate(prescription.created_at) }}
							</p>
						</div>
					</div>

					<div class="detail-card bg-white p-6 rounded shadow">
						<h3 class="text-xl font-bold mb-4">Clinical Notes</h3>
						<p class="text-gray-700 whitespace-pre-line">
							{{
								prescription.notes ||
								'No notes provided for this prescription.'
							}}
						</p>
					</div>
				</div>

				<div class="detail-card bg-white p-6 rounded shadow">
					<div
						class="flex flex-col gap-2 mb-4 md:flex-row md:items-center md:justify-between"
					>
						<h3 class="text-xl font-bold">Medicine Items</h3>
						<p class="text-sm text-gray-500">
							Detailed medicines included in this prescription.
						</p>
					</div>

					<div
						v-if="!prescription.items || !prescription.items.length"
						class="text-gray-500"
					>
						No medicines were attached to this prescription.
					</div>

					<div v-else class="overflow-x-auto">
						<table class="table-auto w-full">
							<thead>
								<tr>
									<th class="border px-4 py-2 text-left">
										Medicine
									</th>
									<th class="border px-4 py-2 text-left">
										Dosage
									</th>
									<th class="border px-4 py-2 text-left">
										Quantity
									</th>
								</tr>
							</thead>
							<tbody>
								<tr
									v-for="item in prescription.items"
									:key="item.id"
								>
									<td class="border px-4 py-3">
										<div class="font-medium text-gray-900">
											{{
												item.medicine_name ||
												'Unknown medicine'
											}}
										</div>
										<div class="text-xs text-gray-500">
											Medicine ID:
											{{ item.medicine || '-' }}
										</div>
									</td>
									<td class="border px-4 py-3">
										{{ item.medicine_dosage || '-' }}
									</td>
									<td class="border px-4 py-3">
										{{ item.quantity || 0 }}
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

const token = localStorage.getItem('authToken');

export default {
	name: 'MyPrescriptionDetailPage',
	data() {
		return {
			prescription: null,
			loading: true,
			error: '',
		};
	},
	computed: {
		doctorName() {
			return (
				this.prescription?.doctor ||
				this.prescription?.prescribed_by_name ||
				'-'
			);
		},
		patientName() {
			const fullName = [
				this.prescription?.patient_first_name,
				this.prescription?.patient_last_name,
			]
				.filter(Boolean)
				.join(' ')
				.trim();

			return fullName || this.prescription?.patient_name || '-';
		},
		itemCountLabel() {
			const itemCount = Array.isArray(this.prescription?.items)
				? this.prescription.items.length
				: 0;
			return `${itemCount} medicine${itemCount === 1 ? '' : 's'}`;
		},
	},
	created() {
		this.fetchPrescriptionDetails();
	},
	methods: {
		goBackToPrescriptions() {
			this.$router.push('/my-prescriptions');
		},
		formatDateTime(value) {
			if (!value) {
				return '-';
			}

			return new Date(value).toLocaleString();
		},
		formatDate(value) {
			if (!value) {
				return '-';
			}

			return new Date(value).toLocaleDateString();
		},
		async fetchPrescriptionDetails() {
			const prescriptionId = this.$route.params.id;
			this.loading = true;
			this.error = '';
			try {
				if (!token) {
					throw new Error('Authentication token is missing.');
				}

				const response = await axios.get(
					`http://localhost:8000/api/prescriptions/mine/${prescriptionId}/`,
					{
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);
				this.prescription = response.data;
			} catch (error) {
				this.error =
					'Failed to load prescription details. Please try again later.';
				console.error('Error fetching prescription details:', error);
			} finally {
				this.loading = false;
			}
		},
	},
};
</script>

<style scoped>
.detail-card {
	border: 1px solid #e5e7eb;
	box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease;
}

.detail-card:hover {
	transform: translateY(-1px);
	border-color: #fda4af;
	box-shadow: 0 12px 24px rgba(244, 63, 94, 0.14);
}
</style>
