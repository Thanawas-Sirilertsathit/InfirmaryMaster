<template>
	<nav class="staff-navbar">
		<ul class="navbar-list">
			<li>
				<router-link to="/prescriptions">Prescriptions</router-link>
			</li>
			<li><router-link to="/inventory">Inventory</router-link></li>
			<li><router-link to="/medicine">Medicines</router-link></li>
		</ul>
	</nav>
</template>

<script>
export default {
	name: 'StaffNavbar',
};
</script>

<style scoped>
.staff-navbar {
	background-color: #f8f9fa;
	padding: 1rem;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-list {
	display: flex;
	list-style: none;
	padding: 0;
	margin: 0;
}

.navbar-list li {
	margin-right: 1rem;
}

.navbar-list li a {
	text-decoration: none;
	color: #007bff;
}

.navbar-list li a:hover {
	text-decoration: underline;
}
</style>
