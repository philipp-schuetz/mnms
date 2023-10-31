<script>
	import { env } from '$env/dynamic/public';
	import { usernameStore } from '../../stores.js';

	async function login(username, password) {
		const response = await fetch(`${env.PUBLIC_API_PATH}/token`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			body: `grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`,
		});
		const data = await response.json();
		window.localStorage.setItem('token', data['access_token']);
		return response.status;
	}

	function logout() {
		window.localStorage.setItem('token', '');
		usernameStore.set('');
	}

	let username = '';
	let password = '';
	let message = '';
</script>

<form
	on:submit={async () => {
		const result = await login(username, password);
		if (result === 200) {
			usernameStore.set(username);
			message = 'Login successful';
			username = '';
			password = '';
		} else if (result === 401) {
			message = 'Wrong username or password';
		} else {
			message = 'Something went wrong';
		}
	}}
>
	<label for="username">Username:</label>
	<input
		type="text"
		id="username"
		bind:value={username}
	/>

	<label for="password">Password:</label>
	<input
		type="password"
		id="password"
		bind:value={password}
	/>

	<button type="submit">Abmelden</button>
</form>
<button on:click={logout}>Abmelden</button>

<p>{message}</p>
