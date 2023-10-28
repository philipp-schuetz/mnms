import { env } from '$env/dynamic/public';
import { authToken } from './stores.js'

/**
 * @param {string} url
 */
export async function fetchData(url) {
	let token;
	authToken.subscribe((value) => {
		token = value;
	});
	try {
		const response = await fetch(`${env.PUBLIC_API_PATH}${url}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${token}`
			}
		});
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('Error fetching data:', error);
	}
}

/**
 * @param {string} username
 * @param {string} password
 */
export async function login(username, password) {
	try {
		const response = await fetch(`${env.PUBLIC_API_PATH}/token`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: `grant_type=&username=${username}&password=${password}&scope=&client_id=&client_secret=`,
		});
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json();
		authToken.update(data['access_token']);
		return response.status;
	} catch (error) {
		console.error('Error while authenticating user:', error);
	}
}
