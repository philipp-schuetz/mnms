export const ssr = false;
import { env } from '$env/dynamic/public';
import { authToken } from '../../stores.js';
import { redirect } from '@sveltejs/kit';

export async function load({ fetch, params }) {
	let token;
	authToken.subscribe((value) => {
		token = value;
	});

	const response = await fetch(`${env.PUBLIC_API_PATH}/groups/get-all`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'Authorization': `Bearer ${token}`
		}
	});

	let groups = [];
	let group_scores = {};
	groups = await response.json();

	for (let group of groups) {
		const response = await fetch(`${env.PUBLIC_API_PATH}/groups/${group}/scores`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				'Authorization': `Bearer ${token}`
			}
		});
		if (!response.ok) {
			throw redirect(307, '/login');
		}
		group_scores[group] = await response.json();
	}

	return {
		groups: groups,
		group_scores: group_scores
	};
}
