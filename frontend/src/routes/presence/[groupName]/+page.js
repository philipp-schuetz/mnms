export const ssr = false;

import { fetchData } from '../../../api.js';

export async function load({ params }) {

    let participantsData = [];
    participantsData = await fetchData(`/groups/${params.groupName}/participants`);


    // if (!post) throw error(404);

    return {
        participantsData: participantsData,
    };
}
