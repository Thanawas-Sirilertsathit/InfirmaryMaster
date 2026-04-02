<template>
	<div class="staff-table-page">
		<header class="text-center py-10">
			<h1 class="text-4xl font-bold text-primary">Staff Management</h1>
			<p class="text-secondary mt-4">Verify and manage staff accounts.</p>
		</header>
		<table
			class="table-auto w-full max-w-4xl mx-auto bg-white shadow-md rounded"
		>
			<thead>
				<tr>
					<th class="px-4 py-2">Staff ID</th>
					<th class="px-4 py-2">Name</th>
					<th class="px-4 py-2">Email</th>
					<th class="px-4 py-2">Status</th>
					<th class="px-4 py-2">Actions</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="staff in staffList" :key="staff.id">
					<td class="border px-4 py-2">{{ staff.id }}</td>
					<td class="border px-4 py-2">{{ staff.name }}</td>
					<td class="border px-4 py-2">{{ staff.email }}</td>
					<td class="border px-4 py-2">
						<span
							:class="
								staff.verified
									? 'text-green-500'
									: 'text-red-500'
							"
						>
							{{ staff.verified ? 'Verified' : 'Unverified' }}
						</span>
					</td>
					<td class="border px-4 py-2">
						<button
							v-if="!staff.verified"
							class="btn btn-primary btn-sm"
							@click="verifyStaff(staff.id)"
						>
							Verify
						</button>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	name: 'StaffTablePage',
	data() {
		return {
			staffList: [],
		};
	},
	created() {
		this.fetchStaff();
	},
	methods: {
		async fetchStaff() {
			try {
				const response = await axios.get(
					'http://localhost:8000/api/staff/',
				);
				this.staffList = response.data;
			} catch (error) {
				console.error('Error fetching staff:', error);
			}
		},
		async verifyStaff(id) {
			try {
				await axios.post(
					`http://localhost:8000/api/staff/${id}/verify/`,
				);
				const staff = this.staffList.find((s) => s.id === id);
				if (staff) {
					staff.verified = true;
				}
				alert('Staff verified successfully!');
			} catch (error) {
				console.error('Error verifying staff:', error);
			}
		},
	},
};
</script>

<style scoped>
/* Add any specific styles for the staff table page here */
</style>
