<script>
	import { variables } from '$lib/variables';
	import { createEventDispatcher } from 'svelte';
	import { refresh } from '$lib/refresh';

	export let sprint_list_data = new Array();

	const dispatch = createEventDispatcher();
	var sprint_list = new Array();

	let selected_sprint = 0;

	export let courseName = 'course1';
	async function get_sprint_list() {
		await fetch(variables.basePath + '/courses/' + courseName + '/sprints', {
			headers: {
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			}
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				return response.json();
			})
			.then((data) => (sprint_list_data = data))
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});

		for (let i = 0; i < sprint_list_data.length; i++) {
			sprint_list.push({
				sprint_id: sprint_list_data[i].sprint_number,
				sprint_name: 'Sprint ' + sprint_list_data[i].sprint_number
			});
		}
	}

	function selectSprint() {
		dispatch('message', { value: selected_sprint });
	}
</script>

<select bind:value={selected_sprint} on:change={selectSprint} class="sprint-selector">
	<option value="0"> All Sprints</option>
	{#await get_sprint_list() then data}
		{#each sprint_list as spr}
			<option value={spr.sprint_id}> {spr.sprint_name}</option>
		{/each}
	{/await}
</select>

<style>
	.sprint-selector {
		display: flex;
		margin-left: 3rem;
		height: auto;
		widows: auto;
		position: absolute;
		padding: 0.2rem;
		margin-top: 1rem;
		font-size: large;
		background-color: white;
		border: 0px;
		border-radius: 0.4rem;
	}
</style>
