export const ssr = false;
import { env } from '$env/dynamic/public';
import { redirect } from '@sveltejs/kit';

function sortByGroup(persons) {
    return persons.sort((a, b) => {
        if (a.group < b.group) {
            return -1;
        }
        if (a.group > b.group) {
            return 1;
        }
        return 0;
    });
}

export async function load({ fetch }) {
    let participantsData = [];

    const response = await fetch(`${env.PUBLIC_API_PATH}/participants/get-all`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${window.localStorage.getItem('token')}`
        }
    });
    if (!response.ok) {
        throw redirect(307, '/login');
    }
    participantsData = await response.json();
    participantsData = sortByGroup(participantsData);

    return {
        participantsData: participantsData
    };
}
