<template>
	<nav class="staff-navbar">
		<ul class="navbar-list">
			<li class="navbar-item">
				<router-link to="/prescriptions" class="navbar-link"
					>Prescriptions</router-link
				>
			</li>
			<li class="navbar-item">
				<router-link to="/inventory" class="navbar-link"
					>Inventory</router-link
				>
			</li>
			<li class="navbar-item">
				<router-link to="/medicine" class="navbar-link"
					>Medicines</router-link
				>
			</li>
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
	background: #f8f9fa;
	padding: 1rem;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-list {
	display: flex;
	flex-wrap: wrap;
	gap: 1rem;
	list-style: none;
	padding: 0;
	margin: 0;
}

.navbar-item {
	min-width: 180px;
}

.navbar-link {
	display: block;
	padding: 1rem 1.25rem;
	border-radius: 14px;
	background: #ffffff;
	border: 1px solid #e5e7eb;
	box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
	text-decoration: none;
	color: #334155;
	font-weight: 600;
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease,
		background-color 0.18s ease;
}

.navbar-link:hover {
	transform: translateY(-1px);
	border-color: #fda4af;
	box-shadow: 0 12px 24px rgba(244, 63, 94, 0.14);
}

.navbar-link.router-link-active {
	background: #ffe4e6;
	border-color: #fb7185;
	color: #9f1239;
}

@media (max-width: 640px) {
	.navbar-item {
		width: 100%;
	}
}
</style>
