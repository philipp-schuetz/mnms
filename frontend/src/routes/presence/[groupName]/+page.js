export const ssr = false;
import { env } from '$env/dynamic/public';
import { authToken } from '../../../stores.js'
import { redirect } from '@sveltejs/kit';

export async function load({ fetch, params }) {

    const groupName = params.groupName;
    const className = groupName.replace(/-\d$/, '');
    const groupNumber = groupName.replace(/^.*-/, '');

    let participantsData = [];

    let token;
    authToken.subscribe((value) => {
        token = value;
    });
    const response = await fetch(`${env.PUBLIC_API_PATH}/groups/${groupName}/participants`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) {
        throw redirect(307, '/login');
    }

    participantsData = await response.json();

    return {
        participantsData: participantsData,
        groupName: groupName,
        className: className,
        groupNumber: groupNumber,
    };
}
