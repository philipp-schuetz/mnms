<script>
	export let groupName;

	import { env } from '$env/dynamic/public';
	import { onMount } from 'svelte';
	import { fetchData } from '../../../api.js';

	let participantsData = [];

	onMount(async () => {
		participantsData = await fetchData(`/groups/${groupName}/participants`);
	});

	async function setPresence(participantId, present) {
		try {
			const url = `/participants/set-present?participant_id=${participantId}&present=${present}`;
			const requestOptions = {method: 'PUT'};
			await fetch(`${env.PUBLIC_API_PATH}${url}`, requestOptions);
		} catch (error) {
			console.error('Error updating presence:', error);
		}
	}
</script>

<table class="table table-striped">
	<thead>
		<tr>
			<th scope="col">Vorname</th>
			<th scope="col">Nachname</th>
			<th scope="col">Anwesend</th>
		</tr>
	</thead>
	<tbody>
		{#each participantsData as participant (participant.id)}
		<tr>
			<td>{participant.firstname}</td>
			<td>{participant.lastname}</td>
			<td>
				<div class="form-check">
					<input class="form-check-input" type="checkbox" bind:checked={participant.present} on:change={() => setPresence(participant.id, participant.present)} />
				</div>
			</td>
		</tr>
		{/each}
	</tbody>
</table>
