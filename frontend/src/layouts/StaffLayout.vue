<template>
	<div class="staff-layout">
		<StaffNavbar />
		<main>
			<router-view />
		</main>
	</div>
</template>

<script>
import StaffNavbar from '../components/StaffNavbar.vue';

export default {
	name: 'StaffLayout',
	components: {
		StaffNavbar,
	},
};
</script>

<style scoped>
.staff-layout {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
}

main {
	flex: 1;
	padding: 1rem;
}
</style>
