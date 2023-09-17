import { env } from '$env/dynamic/public';

async function fetchData(url) {
	try {
		const response = await fetch(`${env.PUBLIC_API_PATH}${url}`);
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json();
		return data;
	} catch (error) {
		console.error('Error fetching data:', error);
	}
}

export { fetchData };
