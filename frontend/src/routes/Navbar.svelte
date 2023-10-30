<script>
	import { onMount } from 'svelte';
	import { env } from '$env/dynamic/public';
	import { usernameStore } from '../stores.js';

	let groups = [];
	let username = '';
	let loggedIn = false;
	onMount(async () => {
		const groupsData = await fetch(`${env.PUBLIC_API_PATH}/groups/get-all`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
		});
		groups = await groupsData.json();

		const userData = await fetch(`${env.PUBLIC_API_PATH}/users/current`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${window.localStorage.getItem('token')}`,
			},
		});
		if (userData.ok) {
			loggedIn = true;
			const tmp = await userData.json();
			usernameStore.set(tmp['username']);
		}
	});
</script>

<nav class="navbar navbar-expand-lg bg-body-tertiary">
	<div class="container-fluid">
		<a
			class="navbar-brand"
			href="/">MNMS</a
		>
		<button
			class="navbar-toggler"
			type="button"
			data-bs-toggle="collapse"
			data-bs-target="#navbarSupportedContent"
			aria-controls="navbarSupportedContent"
			aria-expanded="false"
			aria-label="Toggle navigation"
		>
			<span class="navbar-toggler-icon" />
		</button>
		<div
			class="collapse navbar-collapse"
			id="navbarSupportedContent"
		>
			<ul class="navbar-nav me-auto mb-2 mb-lg-0">
				<li class="nav-item">
					<a
						class="nav-link"
						aria-current="page"
						href="/evaluation">Auswertung</a
					>
				</li>
				<li class="nav-item dropdown">
					<a
						class="nav-link dropdown-toggle"
						href="/points"
						role="button"
						data-bs-toggle="dropdown"
						aria-expanded="false"
					>
						Punkte
					</a>
					<ul class="dropdown-menu">
						{#each groups as group}
							<li>
								<a
									class="dropdown-item"
									href="/points/{group}">{group}</a
								>
							</li>
						{/each}
					</ul>
				</li>
				<li class="nav-item dropdown">
					<a
						class="nav-link dropdown-toggle"
						href="/presence"
						role="button"
						data-bs-toggle="dropdown"
						aria-expanded="false"
					>
						Anwesenheit
					</a>
					<ul class="dropdown-menu">
						{#each groups as group}
							<li>
								<a
									class="dropdown-item"
									href="/presence/{group}">{group}</a
								>
							</li>
						{/each}
						<li><hr class="dropdown-divider" /></li>
						<li>
							<a
								class="dropdown-item"
								href="/presence/check">Überprüfen</a
							>
						</li>
					</ul>
				</li>
				<li class="nav-item">
					<a
						class="nav-link"
						aria-current="page"
						href="/login"
					>
						{#if $usernameStore != ''}
							Angemeldet als {$usernameStore}
						{:else}
							Anmelden
						{/if}
					</a>
				</li>
			</ul>
		</div>
	</div>
</nav>
