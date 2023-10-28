<script>
	import { login } from '../../api.js';

	let username = '';
	let password = '';
	let message = '';
</script>

<form
	on:submit={() => {
		const result = login(username, password);
		if (result === 200) {
			message = 'Login successful';
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

	<button type="submit">Login</button>
</form>

<p>{message}</p>
