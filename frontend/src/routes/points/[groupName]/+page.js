export const ssr = false;
import { env } from '$env/dynamic/public';
import { redirect } from '@sveltejs/kit';

export async function load({ fetch, params }) {
    const groupName = params.groupName;
    const className = groupName.replace(/-\d$/, '');
    const groupNumber = groupName.replace(/^.*-/, '');

    async function fetchData(route) {
        const response = await fetch(`${env.PUBLIC_API_PATH}${route}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.localStorage.getItem('token')}`
            }
        });
        if (!response.ok) {
            throw redirect(307, '/login');
        }
        return response.json();
    }

    let classData = {};
    classData = await fetchData(`/classes/info?class_name=${className}`);

    let stationsData = [];
    const data = await fetchData(`/groups/${groupName}/stations`);
    stationsData = data.stations;

    let stationScores = [0, 0, 0, 0, 0, 0];
    let fairnessScore = 0;
    const scoreData = await fetchData(`/groups/${groupName}/scores`);
    stationScores = scoreData.station_scores;
    fairnessScore = scoreData.fairness_score;

    return {
        classData: classData,
        stationsData: stationsData,
        stationScores: stationScores,
        fairnessScore: fairnessScore,
        groupName: groupName,
        groupNumber: groupNumber,
        className: className
    };
}
