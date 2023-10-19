export const ssr = false;

import { fetchData } from '../../../api.js';

export async function load({ params }) {

    const groupName = params.groupName;
	const className = groupName.replace(/-\d$/, '');
	const groupNumber = groupName.replace(/^.*-/, '');

    let participantsData = [];
    participantsData = await fetchData(`/groups/${groupName}/participants`);


    // if (!post) throw error(404);

    return {
        participantsData: participantsData,
        groupName: groupName,
        className: className,
        groupNumber: groupNumber,
    };
}
