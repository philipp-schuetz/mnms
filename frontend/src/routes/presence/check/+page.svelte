<script>
	import { onMount } from 'svelte';
	import { fetchData } from '../../../api.js';

	let participantsData = [];
	let not_present_switch = false;

	onMount(async () => {
		participantsData = await fetchData(`/participants/get-all`);
	});
</script>

<button
	type="button"
	class="btn btn-primary"
	on:click={() => (not_present_switch = !not_present_switch)}
>
	{#if not_present_switch}
		Not Present
	{:else}
		All
	{/if}
</button>
<table class="table table-striped">
	<thead>
		<tr>
			<th scope="col">Gruppe</th>
			<th scope="col">Vorname</th>
			<th scope="col">Nachname</th>
			<th scope="col">Anwesend</th>
		</tr>
	</thead>
	<tbody>
		{#each participantsData as participant}
			{#if not_present_switch}
				{#if !participant.present}
					<tr>
						<td>{participant.firstname}</td>
						<td>{participant.lastname}</td>
						<td>{participant.group}</td>
						<td>
							<div class="form-check">
								<input
									class="form-check-input"
									type="checkbox"
									bind:checked={participant.present}
									disabled
								/>
							</div>
						</td>
					</tr>
				{/if}
			{:else}
				<tr>
					<td>{participant.firstname}</td>
					<td>{participant.lastname}</td>
					<td>{participant.group}</td>
					<td>
						<div class="form-check">
							<input
								class="form-check-input"
								type="checkbox"
								bind:checked={participant.present}
								disabled
							/>
						</div>
					</td>
				</tr>
			{/if}
		{/each}
	</tbody>
</table>
