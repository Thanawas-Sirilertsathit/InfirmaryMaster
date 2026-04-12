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

		<ConfirmVerifyStaffModal
			:isOpen="showVerifyModal"
			:staffName="staffToVerify?.name"
			@confirm-verify="confirmVerifyStaff"
			@close="closeVerifyModal"
		/>
	</div>
</template>

<script>
import ConfirmVerifyStaffModal from '@/components/modals/ConfirmVerifyStaffModal.vue';
import axios from 'axios';

const token = localStorage.getItem('authToken');

export default {
	name: 'StaffTablePage',
	components: {
		ConfirmVerifyStaffModal,
	},
	data() {
		return {
			staffList: [],
			showVerifyModal: false,
			staffToVerify: null,
		};
	},
	created() {
		this.fetchStaff();
	},
	methods: {
		getStaffName(staff) {
			return (
				[staff.first_name, staff.last_name].filter(Boolean).join(' ') ||
				staff.username ||
				'-'
			);
		},
		async fetchStaff() {
			try {
				const response = await axios.get(
					'http://localhost:8000/api/auth/staff/',
					{
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);
				this.staffList = response.data.map((staff) => ({
					...staff,
					name: this.getStaffName(staff),
				}));
			} catch (error) {
				console.error('Error fetching staff:', error);
			}
		},
		verifyStaff(id) {
			this.staffToVerify =
				this.staffList.find((staff) => staff.id === id) || null;
			this.showVerifyModal = Boolean(this.staffToVerify);
		},
		closeVerifyModal() {
			this.showVerifyModal = false;
			this.staffToVerify = null;
		},
		async confirmVerifyStaff() {
			if (!this.staffToVerify) {
				return;
			}

			try {
				await axios.post(
					'http://localhost:8000/api/auth/staff/verify/',
					{ id: this.staffToVerify.id },
					{
						headers: {
							Accept: 'application/json',
							Authorization: `Bearer ${token}`,
						},
					},
				);
				await this.fetchStaff();
			} catch (error) {
				console.error('Error verifying staff:', error);
			} finally {
				this.closeVerifyModal();
			}
		},
	},
};
</script>

<style scoped>
/* Add any specific styles for the staff table page here */
</style>
