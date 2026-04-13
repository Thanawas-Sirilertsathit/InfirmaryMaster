<template>
	<nav class="staff-navbar">
		<div class="navbar-inner">
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

			<div class="notification-area">
				<div class="nav-actions">
					<button
						type="button"
						class="notification-button"
						@click="toggleNotifications"
					>
						<svg
							class="notification-icon"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="1.8"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<path
								d="M15 17h5l-1.4-1.4a2 2 0 0 1-.6-1.4V11a6 6 0 1 0-12 0v3.2a2 2 0 0 1-.6 1.4L4 17h5"
							/>
							<path d="M9 17a3 3 0 0 0 6 0" />
						</svg>
						<span v-if="unreadCount" class="notification-badge">
							{{ unreadCount }}
						</span>
					</button>

					<button
						type="button"
						class="logout-button"
						@click="logoutUser"
					>
						Log Out
					</button>
				</div>

				<div v-if="showNotifications" class="notification-panel">
					<div class="notification-panel-header">
						<div>
							<p class="notification-title">Notifications</p>
							<p class="notification-subtitle">
								{{ unreadCount }} unread
							</p>
						</div>
						<button
							type="button"
							class="notification-refresh"
							@click="fetchNotifications"
						>
							Refresh
						</button>
					</div>

					<div
						v-if="isLoadingNotifications"
						class="notification-empty"
					>
						Loading notifications...
					</div>

					<div
						v-else-if="!notifications.length"
						class="notification-empty"
					>
						No notifications right now.
					</div>

					<ul v-else class="notification-list">
						<li
							v-for="notification in notifications"
							:key="notification.id"
						>
							<button
								type="button"
								class="notification-item"
								:class="{
									'notification-item-read':
										notification.is_read,
								}"
								@click="markNotificationRead(notification.id)"
							>
								<div class="notification-item-top">
									<span class="notification-item-title">
										{{ notification.title }}
									</span>
									<span
										v-if="!notification.is_read"
										class="notification-pill"
									>
										Unread
									</span>
								</div>
								<p class="notification-item-message">
									{{ notification.message }}
								</p>
								<p class="notification-item-time">
									{{
										formatDateTime(notification.created_at)
									}}
								</p>
							</button>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</nav>
</template>

<script>
import apiManager from '@/api/api_manager';

export default {
	name: 'StaffNavbar',
	data() {
		return {
			notifications: [],
			unreadCount: 0,
			showNotifications: false,
			isLoadingNotifications: false,
			pollTimerId: null,
		};
	},
	mounted() {
		this.fetchNotifications();
		this.pollTimerId = window.setInterval(() => {
			this.fetchNotifications();
		}, 60000);
	},
	beforeUnmount() {
		if (this.pollTimerId) {
			window.clearInterval(this.pollTimerId);
		}
	},
	methods: {
		clearStoredAuth() {
			localStorage.removeItem('authToken');
			localStorage.removeItem('authUser');
			localStorage.removeItem('refreshToken');
		},
		async fetchNotifications() {
			this.isLoadingNotifications = true;
			try {
				const response = await apiManager.get(
					'/api/reports/notifications/',
					{
						headers: apiManager.getAuthHeaders(),
					},
				);
				this.notifications = Array.isArray(response.data?.results)
					? response.data.results
					: [];
				this.unreadCount = Number(response.data?.unread_count || 0);
			} catch (error) {
				console.error('Error fetching notifications:', error);
			} finally {
				this.isLoadingNotifications = false;
			}
		},
		async markNotificationRead(notificationId) {
			try {
				await apiManager.post(
					`/api/reports/notifications/${notificationId}/read/`,
					{},
					{
						headers: apiManager.getAuthHeaders(),
					},
				);
				await this.fetchNotifications();
			} catch (error) {
				console.error('Error marking notification as read:', error);
			}
		},
		toggleNotifications() {
			this.showNotifications = !this.showNotifications;
			if (this.showNotifications) {
				this.fetchNotifications();
			}
		},
		async logoutUser() {
			const refreshToken = localStorage.getItem('refreshToken');

			try {
				if (refreshToken) {
					await apiManager.post('/api/auth/logout/', {
						refresh: refreshToken,
					});
				}
			} catch (error) {
				console.error('Logout failed:', error);
			} finally {
				this.clearStoredAuth();
				this.showNotifications = false;
				this.$router.push('/');
			}
		},
		formatDateTime(value) {
			if (!value) {
				return '-';
			}

			return new Date(value).toLocaleString();
		},
	},
};
</script>

<style scoped>
.staff-navbar {
	background: #f8f9fa;
	padding: 1rem;
	box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-inner {
	display: flex;
	align-items: flex-start;
	justify-content: space-between;
	gap: 1rem;
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

.notification-area {
	position: relative;
	flex-shrink: 0;
}

.nav-actions {
	display: flex;
	align-items: center;
	gap: 0.75rem;
}

.notification-button {
	position: relative;
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 3.25rem;
	height: 3.25rem;
	border-radius: 14px;
	border: 1px solid #e5e7eb;
	background: #ffffff;
	box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
	color: #334155;
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease;
}

.notification-button:hover {
	transform: translateY(-1px);
	border-color: #fda4af;
	box-shadow: 0 12px 24px rgba(244, 63, 94, 0.14);
}

.logout-button {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	height: 3.25rem;
	padding: 0 1rem;
	border-radius: 14px;
	border: 1px solid #fecdd3;
	background: #fff1f2;
	color: #9f1239;
	font-weight: 700;
	box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
	transition:
		transform 0.18s ease,
		box-shadow 0.18s ease,
		border-color 0.18s ease,
		background-color 0.18s ease;
}

.logout-button:hover {
	transform: translateY(-1px);
	border-color: #fb7185;
	background: #ffe4e6;
	box-shadow: 0 12px 24px rgba(244, 63, 94, 0.14);
}

.notification-icon {
	width: 1.35rem;
	height: 1.35rem;
}

.notification-badge {
	position: absolute;
	top: -0.3rem;
	right: -0.3rem;
	min-width: 1.35rem;
	height: 1.35rem;
	padding: 0 0.35rem;
	border-radius: 999px;
	background: #e11d48;
	color: #ffffff;
	font-size: 0.75rem;
	font-weight: 700;
	display: inline-flex;
	align-items: center;
	justify-content: center;
}

.notification-panel {
	position: absolute;
	right: 0;
	top: calc(100% + 0.75rem);
	width: min(26rem, 85vw);
	padding: 1rem;
	border-radius: 18px;
	border: 1px solid #e5e7eb;
	background: #ffffff;
	box-shadow: 0 16px 36px rgba(15, 23, 42, 0.14);
	z-index: 20;
}

.notification-panel-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	margin-bottom: 0.75rem;
}

.notification-title {
	margin: 0;
	font-weight: 700;
	color: #0f172a;
}

.notification-subtitle {
	margin: 0.15rem 0 0;
	font-size: 0.85rem;
	color: #64748b;
}

.notification-refresh {
	border: 0;
	background: transparent;
	font-size: 0.85rem;
	font-weight: 600;
	color: #be123c;
}

.notification-list {
	display: flex;
	flex-direction: column;
	gap: 0.75rem;
	list-style: none;
	padding: 0;
	margin: 0;
	max-height: 22rem;
	overflow-y: auto;
}

.notification-item {
	width: 100%;
	text-align: left;
	padding: 0.85rem 0.95rem;
	border-radius: 14px;
	border: 1px solid #e5e7eb;
	background: #fff1f2;
	transition:
		border-color 0.18s ease,
		background-color 0.18s ease;
}

.notification-item:hover {
	border-color: #fb7185;
}

.notification-item-read {
	background: #f8fafc;
}

.notification-item-top {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 0.75rem;
	margin-bottom: 0.35rem;
}

.notification-item-title {
	font-weight: 700;
	color: #0f172a;
}

.notification-pill {
	flex-shrink: 0;
	padding: 0.15rem 0.5rem;
	border-radius: 999px;
	background: #ffe4e6;
	color: #9f1239;
	font-size: 0.75rem;
	font-weight: 700;
}

.notification-item-message {
	margin: 0;
	color: #475569;
	font-size: 0.9rem;
	line-height: 1.4;
}

.notification-item-time,
.notification-empty {
	margin: 0.45rem 0 0;
	font-size: 0.8rem;
	color: #64748b;
}

@media (max-width: 640px) {
	.navbar-inner {
		flex-direction: column;
	}

	.navbar-item {
		width: 100%;
	}

	.notification-area {
		width: 100%;
	}

	.nav-actions {
		width: 100%;
	}

	.notification-button {
		flex: 0 0 auto;
	}

	.logout-button {
		flex: 1 1 auto;
	}

	.notification-panel {
		left: 0;
		right: auto;
		width: 100%;
	}
}
</style>
