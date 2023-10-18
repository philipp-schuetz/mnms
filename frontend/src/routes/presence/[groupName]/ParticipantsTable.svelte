<script>
	export let participantsData;

	import { env } from '$env/dynamic/public';
	import { onMount } from 'svelte';

	let mounted = false;
	let isConnected = false;

	let showWarning = false;

	onMount(async () => {
		mounted = true;

		isConnected = navigator.onLine;
		window.addEventListener('online', () => {
			console.log('online');
			isConnected = true;
			showWarning = false;
		});
		window.addEventListener('offline', () => {
			console.log('offline');
			isConnected = false;
			showWarning = true;
		});

		window.addEventListener('beforeunload', (event) => {
			if (!isConnected) {
				event.preventDefault();
				event.returnValue =
					'You may have unsaved data. Are you sure you want to leave?';
			}
		});
	});

	async function setPresence(participantId, present) {
		try {
			const url = `/participants/set-present?participant_id=${participantId}&present=${present}`;
			const requestOptions = { method: 'PUT' };
			await fetch(`${env.PUBLIC_API_PATH}${url}`, requestOptions);
		} catch (error) {
			console.error('Error updating presence:', error);
		}
	}
</script>

{#if showWarning}
	<div class="warning">
		<p>
			By leaving the site data could be lost due to missing network connection.
		</p>
	</div>
{/if}

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
						<input
							class="form-check-input"
							type="checkbox"
							bind:checked={participant.present}
							on:change={() => {
								if (isConnected) {
									setPresence(participant.id, participant.present);
								}
							}}
						/>
					</div>
				</td>
			</tr>
		{/each}
	</tbody>
</table>
