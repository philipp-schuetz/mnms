<script>
	export let groupName;

	import { onMount } from 'svelte';
	import { fetchData } from '../../../api.js'

	let participantsData = [];

	onMount(async () => {
			participantsData = await fetchData(`/groups/${groupName}/participants`);
		});
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
		{#each participantsData as participant (participant.firstname)} <!-- api should provide a unique id for each participant, use this as and identifiere here instead of firstname-->
			<tr>
				<td>{participant.firstname}</td>
				<td>{participant.lastname}</td>
				{#if participant.present === true}
					<td>
						<div class="form-check">
							<input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" checked>
						</div>
					</td>
				{:else}
					<td>
						<div class="form-check">
							<input class="form-check-input" type="checkbox" value="" id="flexCheckChecked">
						</div>
					</td>
				{/if}
			</tr>
		{/each}
	</tbody>
  </table>
