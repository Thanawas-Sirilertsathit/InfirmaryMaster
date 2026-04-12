<template>
	<div class="patient-prescription-list-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">My Prescriptions</h1>
			<p class="text-secondary mt-4">
				View and manage your prescriptions.
			</p>
		</header>
		<div
			class="form-control mb-6 max-w-4xl mx-auto flex flex-col gap-3 md:flex-row md:items-center md:justify-between"
		>
			<div class="flex w-full flex-col gap-3 md:flex-row md:items-center">
				<input
					v-model.trim="searchQuery"
					type="text"
					placeholder="Search by medicine, doctor, patient, or notes"
					class="input input-bordered w-full md:flex-grow"
					@keyup.enter="applySearch"
				/>
				<button class="btn btn-outline" @click="applySearch">
					Search
				</button>
				<button
					v-if="searchQuery"
					class="btn border-black bg-white text-red-600 hover:border-black hover:bg-red-50 hover:text-red-700"
					@click="clearSearch"
				>
					Clear
				</button>
			</div>
			<button class="btn btn-primary" @click="createPrescription">
				Create Prescription
			</button>
		</div>
		<table
			class="table-auto w-full max-w-4xl mx-auto bg-white shadow-md rounded"
		>
			<thead>
				<tr>
					<th class="px-4 py-2">Prescription ID</th>
					<th class="px-4 py-2">Date</th>
					<th class="px-4 py-2">Doctor</th>
					<th class="px-4 py-2">Patient</th>
					<th class="px-4 py-2">Notes</th>
					<th class="px-4 py-2">Medicines</th>
					<th class="px-4 py-2">Actions</th>
				</tr>
			</thead>
			<tbody>
				<tr v-if="!prescriptions.length">
					<td
						class="border px-4 py-6 text-center text-gray-500"
						colspan="7"
					>
						No prescriptions found.
					</td>
				</tr>
				<tr
					v-for="prescription in prescriptions"
					:key="prescription.id"
				>
					<td class="border px-4 py-2">{{ prescription.id }}</td>
					<td class="border px-4 py-2">
						{{ formatDate(prescription.created_at) }}
					</td>
					<td class="border px-4 py-2">
						{{ getDoctorName(prescription) }}
					</td>
					<td class="border px-4 py-2">
						{{ getPatientName(prescription) }}
					</td>
					<td class="border px-4 py-2">
						{{ prescription.notes || '-' }}
					</td>
					<td class="border px-4 py-2">
						{{ getMedicineSummary(prescription) }}
					</td>
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
		<div
			class="max-w-4xl mx-auto mt-6 flex items-center justify-between gap-4"
		>
			<p class="text-sm text-gray-600">
				Page {{ currentPage }} of {{ totalPages }}
				<span v-if="totalCount">({{ totalCount }} prescriptions)</span>
			</p>
			<div class="flex gap-2">
				<button
					class="btn btn-outline btn-sm"
					@click="changePage(currentPage - 1)"
					:disabled="!hasPrevious"
				>
					Previous
				</button>
				<button
					class="btn btn-outline btn-sm"
					@click="changePage(currentPage + 1)"
					:disabled="!hasNext"
				>
					Next
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios';

const token = localStorage.getItem('authToken');

export default {
	name: 'PatientPrescriptionListPage',
	data() {
		return {
			prescriptions: [],
			searchQuery: '',
			currentPage: 1,
			totalCount: 0,
			hasNext: false,
			hasPrevious: false,
			pageSize: 20,
		};
	},
	computed: {
		totalPages() {
			const total = Math.ceil(this.totalCount / this.pageSize);
			return total || 1;
		},
	},
	created() {
		this.fetchPrescriptions();
	},
	methods: {
		applySearch() {
			this.fetchPrescriptions(1);
		},
		changePage(page) {
			if (
				page < 1 ||
				page > this.totalPages ||
				page === this.currentPage
			) {
				return;
			}

			this.fetchPrescriptions(page);
		},
		createPrescription() {
			this.$router.push('/prescription/create'); // Navigate to the create prescription page
		},
		clearSearch() {
			if (!this.searchQuery) {
				return;
			}

			this.searchQuery = '';
			this.fetchPrescriptions(1);
		},
		getDoctorName(prescription) {
			return (
				prescription?.doctor || prescription?.prescribed_by_name || '-'
			);
		},
		getPatientName(prescription) {
			const fullName = [
				prescription?.patient_first_name,
				prescription?.patient_last_name,
			]
				.filter(Boolean)
				.join(' ')
				.trim();

			return fullName || prescription?.patient_name || '-';
		},
		getMedicineSummary(prescription) {
			if (
				!Array.isArray(prescription?.items) ||
				!prescription.items.length
			) {
				return '-';
			}

			return prescription.items
				.map((item) => {
					const medicineName =
						item.medicine_name || 'Unknown medicine';
					const dosage = item.medicine_dosage
						? ` (${item.medicine_dosage})`
						: '';
					const quantity = item.quantity ? ` x${item.quantity}` : '';
					return `${medicineName}${dosage}${quantity}`;
				})
				.join(', ');
		},
		formatDate(value) {
			if (!value) {
				return '-';
			}

			return new Date(value).toLocaleDateString();
		},
		async fetchPrescriptions(page = 1) {
			try {
				const response = await axios.get(
					'http://localhost:8000/api/prescriptions/list/',
					{
						params: {
							page,
							search: this.searchQuery || undefined,
						},
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);
				const results = Array.isArray(response.data?.results)
					? response.data.results.filter(Boolean)
					: Array.isArray(response.data)
						? response.data.filter(Boolean)
						: [];

				this.prescriptions = results;
				this.currentPage = page;
				this.totalCount = Number.isInteger(response.data?.count)
					? response.data.count
					: results.length;
				this.hasNext = Boolean(response.data?.next);
				this.hasPrevious = Boolean(response.data?.previous);
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
