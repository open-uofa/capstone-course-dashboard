<script>
	import Breadcrumbs from '$lib/Breadcrumbs.svelte';
	import { Datatable } from 'svelte-simple-datatables';
	import DefaultLayout from '$lib/DefaultLayout.svelte';
	import ManageCourseButton from '$lib/ManageCourseButton.svelte';
	import SprintSelector from '$lib/SprintSelector.svelte';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { variables } from '$lib/variables';
	import { writable } from 'svelte/store';
	import { refresh } from '$lib/refresh';

	let courseName = getParameterByName('course');
	let rows = writable([]);
	let team_rows = writable([]);
	let student_data = {};
	let table_data = new Array();
	let team_table_data = new Array();
	let student_list = {};
	let team_data = {};
	let sprints_data = {};
	let sprint = 0;
	let link = '';

	async function getStudentInfo() {
		// replace with base path.. import basepath not working on my machine - vm
		await fetch(variables.basePath + '/students/' + courseName + '/' + sprint, {
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
			.then((data) => (student_data = data))
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});

		student_list = student_data.students;
		table_data = new Array();
		for (let i = 1; i < student_list.length + 1; i++) {
			table_data.push({
				Name: student_list[i - 1].full_name,
				Email: student_list[i - 1].email
			});
		}
	}

	async function getCommits() {
		const res = await fetch(
			variables.basePath + '/class/' + courseName + '/' + sprint + '/commits/',
			{
				headers: {
					Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
				}
			}
		)
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				return response.json();
			})
			.then((data) => (team_data = data))
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});

		team_table_data = new Array();
		for (let i = 1; i < team_data.length + 1; i++) {
			team_table_data.push({
				Name: team_data[i - 1].team_name
			});
		}
	}

	async function getForm() {
		await fetch(variables.basePath + '/form/' + courseName + '/' + sprint, {
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
			.then((data) => (link = data))
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
	}

	function getParameterByName(name, url) {
		if (!url) {
			url = $page.url.href;
		}
		let regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$())'),
			results = regex.exec(url);

		if (!results) return null;
		if (!results[2]) return '';
		return decodeURIComponent(results[2].replace(/\+/g, ' '));
	}

	const settings1 = {
		columnFilter: true,
		rowsPerPage: 40,
		sortable: true,
		scrollY: true,
		labels: {
			search: 'Search Team', // search input placeholer
			filter: 'Filter', // filter inputs placeholder
			noRows: 'No entries to found'
		}
	};

	const settings2 = {
		columnFilter: true,
		rowsPerPage: 40,
		sortable: true,
		scrollY: true,
		labels: {
			search: 'Search Student', // search input placeholer
			filter: 'Filter', // filter inputs placeholder
			noRows: 'No entries to found'
		}
	};

	function sprint_changed(event) {
		sprint = event.detail.value;

		getStudentInfo();
		getCommits();
		getForm();
	}

	onMount(() => {
		courseName = getParameterByName('course');
		// script to load muuri open source grids
		let script2 = document.createElement('script');
		script2.src = 'https://cdn.jsdelivr.net/npm/muuri@0.9.5/dist/muuri.min.js';
		document.head.append(script2);
		script2.onload = () => {
			var grid = new Muuri('.grid', {
				dragEnabled: true,
				dragHandle: '.grid-content > h3,.grid-content >div> h3, .item-content > h3 ',
				layout: {
					rounding: false
				}
			});
		};
	});
</script>

<DefaultLayout {courseName}>
	<section>
		<Breadcrumbs>
			<a href="/dashboard">Dashboard</a>
			<p>{courseName}</p>
		</Breadcrumbs>
	</section>
	<SprintSelector on:message={sprint_changed} {courseName} />
	<ManageCourseButton url={'/dashboard/course/course-data?courseName=' + courseName} />
	<section class="course-name">
		<h1>{courseName}</h1>
	</section>

	<div class="grid">
		<div class="item item1">
			<div class="item-content">
				<h3>Teams</h3>
				<section>
					{#await getCommits()}
						<p class="loader" />
					{:then data}
						<Datatable
							settings={settings1}
							data={team_table_data}
							bind:dataRows={team_rows}
							id={'team_table'}
						>
							<thead style="display:inline-table; width : 100%;">
								<th style="padding: 2rem;" data-key="Name"> Name</th>
							</thead>
							<tbody style="display:block;">
								{#if team_rows}
									{#each $team_rows as row}
										<tr>
											<td>
												<a href="/dashboard/teams/team?team_name={row.Name}&course={courseName}"
													>{row.Name}</a
												>
											</td>
										</tr>
									{/each}
								{/if}
							</tbody>
						</Datatable>
					{/await}
				</section>
			</div>
		</div>

		<div class="item item2">
			<div class="item-content">
				<h3>Students</h3>
				<section>
					{#await getStudentInfo()}
						<p class="loader" />
					{:then data}
						<Datatable
							settings={settings2}
							data={table_data}
							bind:dataRows={rows}
							id={'student_table'}
						>
							<thead style="display:inline-table; width : 100%;">
								<th style="padding: 2rem;" data-key="Name"> Name</th>
								<thead />
							</thead><tbody style="display:block;">
								{#if rows}
									{#each $rows as row}
										<tr>
											<td>
												<a
													href="/dashboard/students/personal_student?student={row.Name}&course={courseName}&email={row.Email}"
												>
													{row.Name}
												</a>
											</td>
										</tr>
									{/each}
								{/if}
							</tbody>
						</Datatable>
					{/await}
				</section>
			</div>
		</div>

		<div class="item item3">
			<div class="grid-content">
				<div>
					<h3>Form Submissions</h3>
				</div>
				<section>
					{#await getForm()}
						<p class="loader" />
					{:then}
						{#if sprint == 0}
							<h3>Please select a sprint</h3>
						{:else if link != ''}
							<iframe src={link} />
						{:else}
							<h1>No form submissions link for this sprint</h1>
						{/if}
					{/await}
				</section>
			</div>
		</div>
	</div>
</DefaultLayout>

<style>
	/* https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_loader */
	.loader {
		border: 8px solid #f3f3f3;
		border-radius: 50%;
		border-top: 8px solid hsl(139, 41%, 40%);
		width: 50px;
		height: 50px;
		-webkit-animation: spin 0.75s linear infinite; /* Safari */
		animation: spin 0.75s linear infinite;
	}

	/* Safari */
	@-webkit-keyframes spin {
		0% {
			-webkit-transform: rotate(0deg);
		}
		100% {
			-webkit-transform: rotate(360deg);
		}
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
	/* width */
	::-webkit-scrollbar {
		width: 4px;
		height: 4px;
	}

	/* Handle */
	::-webkit-scrollbar-thumb {
		background: rgba(0, 0, 0, 0.25);
	}
	::-webkit-scrollbar-track {
		margin-top: 10px;
		margin-bottom: 10px;
	}

	/* Handle on hover */
	::-webkit-scrollbar-thumb:hover {
		background: #555;
	}

	.course-name {
		display: flex;
		align-items: center;
		margin: 1rem 5rem;
		justify-content: center;
		margin-top: -1rem;
	}

	.course-name > h1 {
		font-weight: 400;
		flex: 2;
		font-size: 1.5rem;
		margin: 0;
		text-align: center;
	}

	tr:nth-of-type(odd) {
		background-color: rgb(195, 226, 201);
	}

	td {
		text-align: center;
		padding: 4px 0;
	}

	.grid {
		position: relative;
		height: auto;
		width: auto;
		border: 1px solid rgba(255, 255, 255, 0);
		border-radius: 1rem;
		margin-left: 2vw;
	}

	/* all grid items must have absolute positioning
	 however,  items>div>section can have relative positioning */
	.item1 {
		position: absolute;
		min-width: 20vw;
		width: 20vw;
		height: 75vh;
		margin-left: 0.5rem;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		margin-top: 0.5vh;
	}
	.item1 > div > section {
		position: relative;
		max-width: 100%;
		height: 90%;
		text-align: center;
		background: rgb(255, 255, 255);
		font-size: 15px;
		color: rgb(0, 0, 0);
		cursor: default;
		margin: auto;
	}
	.item1 > div > section > p {
		margin-left: auto;
		margin-right: auto;
	}

	.item2 {
		position: absolute;
		min-width: 20vw;
		width: 20vw;
		height: 75vh;
		margin-left: 0.5rem;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		margin-top: 0.5vh;
	}
	.item2 > div > section {
		position: relative;
		max-width: 100%;
		height: 90%;
		text-align: center;
		background: rgb(255, 255, 255);
		font-size: 15px;
		color: rgb(0, 0, 0);
		cursor: default;
		margin: auto;
	}
	.item2 > div > section > p {
		margin-left: auto;
		margin-right: auto;
	}

	.item3 {
		position: absolute;
		margin-bottom: auto;
		width: 46vw;
		height: 75vh;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		background-color: white;
		margin-left: 0.5rem;
		margin-top: 0.5vh;
		overflow: hidden;
	}

	.item3 > div > section {
		position: relative;
		max-width: 100%;
		height: 100%;
		text-align: center;
		background: rgb(255, 255, 255);
		font-size: 15px;
		color: rgb(0, 0, 0);
		cursor: pointer;
		margin: auto;
	}

	.item3 > div > section > iframe {
		width: 99%;
		height: 65vh;
	}
	.grid-content > div > h3 {
		text-align: center;
		font-size: 20px;
		color: rgb(0, 0, 0);
		width: auto;
		margin: auto;
		padding: 0.5rem;
	}

	.item-content {
		position: relative;
		height: 100%;
		text-align: center;
		background: rgb(255, 255, 255);
		color: white;
		margin: auto;
		cursor: pointer;
		border-radius: 1rem;
	}

	.item-content > h3 {
		text-align: center;
		font-size: 20px;
		color: rgb(0, 0, 0);
		width: auto;
		margin: auto;
		padding: 0.5rem;
	}

	.grid-content > div {
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.grid-content > div :hover {
		cursor: pointer;
	}

	.loader {
		margin-left: auto;
		margin-right: auto;
	}
</style>
