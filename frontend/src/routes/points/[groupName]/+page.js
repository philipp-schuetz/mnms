export const ssr = false;

import { fetchData } from '../../../api.js';

export async function load({ params }) {
    const groupName = params.groupName;
	const className = groupName.replace(/-\d$/, '');
	const groupNumber = groupName.replace(/^.*-/, '');

    let classData = {};
    classData = await fetchData(`/classes/info?class_name=${className}`);


    let stationsData = [];
	let stationScores = [0, 0, 0, 0, 0, 0];
	let fairnessScore = 0;
    const data = await fetchData(`/groups/${groupName}/stations`);
    stationsData = data.stations;
    const scoreData = await fetchData(`/groups/${groupName}/scores`);
    stationScores = scoreData.station_scores;
    fairnessScore = scoreData.fairness_score;


    // if (!post) throw error(404);

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
