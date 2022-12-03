<script>
	import Breadcrumbs from '$lib/Breadcrumbs.svelte';
	import { Datatable } from 'svelte-simple-datatables';
	import DefaultLayout from '$lib/DefaultLayout.svelte';
	import ManageCourseButton from '$lib/ManageCourseButton.svelte';
	import git from '$lib/images/git-logo.svg';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import SprintSelector from '$lib/SprintSelector.svelte';
	import { variables } from '$lib/variables';
	import { writable } from 'svelte/store';
	import refreshImg from '$lib/images/refresh-plot.svg';
	import { refresh } from '$lib/refresh.js';

	let rows = writable([]);
	let team_data = {};
	let table_data = new Array();
	let courseName = getParameterByName('course');
	let sprint = 0;
	let innerWidth = 0;
	let innerHeight = 0;
	let student_data = {};
	let student_list = {};
	let student_table_data = new Array();
	let data_fetched = false;

	// function  to populate the table with data and store data for plotly
	async function getStudentInfo() {
		const res = await fetch(variables.basePath + '/students/' + courseName + '/' + sprint, {
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

		// store all student information in table_data
		for (let i = 1; i < student_list.length + 1; i++) {
			student_table_data.push({
				id: i,
				Email: student_list[i - 1].email,
				Name: student_list[i - 1].full_name,
				Project: student_list[i - 1].project,
				repo_name: student_list[i - 1].repo_name,
				Avg_score: 0,
				Count: 0
			});
		}

		// add average score and count to table_data
		for (let k = 1; k < student_data.sprint_data.length + 1; k++) {
			for (let i = 1; i < student_data.students.length + 1; i++) {
				if (student_table_data[i - 1].Email === student_data.sprint_data[k - 1].email) {
					student_table_data[i - 1].Avg_score =
						student_table_data[i - 1].Avg_score + student_data.sprint_data[k - 1].avg_rating;
					student_table_data[i - 1].Count = student_table_data[i - 1].Count + 1;
					break;
				}
			}
		}

		// calculate average score
		for (let i = 1; i < student_data.students.length + 1; i++) {
			student_table_data[i - 1].Avg_score = (
				student_table_data[i - 1].Avg_score / student_table_data[i - 1].Count
			).toFixed(2);
		}
	}

	async function getCommits() {
		data_fetched = false;
		await getStudentInfo();
		// replace with base path.. import basepath not working on my machine - vm
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

		table_data = new Array();
		for (let i = 1; i < team_data.length + 1; i++) {
			table_data.push({
				id: i,
				Name: team_data[i - 1].team_name,
				Commits: team_data[i - 1].number_of_commits,
				Avg_score_array: [],
				Avg_score_mean: 0,
				Count: 0
			});
		}

		// add each student's calculated avg score to array
		// sum calculated avg
		for (let j = 1; j < table_data.length + 1; j++) {
			for (let i = 1; i < student_table_data.length + 1; i++) {
				if (student_table_data[i - 1].repo_name == table_data[j - 1].Name) {
					if (student_table_data[i - 1].Avg_score != 'NaN') {
						table_data[j - 1].Avg_score_array.push(student_table_data[i - 1].Avg_score);
						table_data[j - 1].Avg_score_mean =
							parseFloat(table_data[j - 1].Avg_score_mean) +
							parseFloat(student_table_data[i - 1].Avg_score);

						table_data[j - 1].Count = table_data[j - 1].Count + 1;
					}
				}
			}
		}

		// calculated mean score for the team
		for (let j = 1; j < table_data.length + 1; j++) {
			table_data[j - 1].Avg_score_mean = (
				table_data[j - 1].Avg_score_mean / table_data[j - 1].Count
			).toFixed(2);
		}

		data_fetched = true;
	}

	async function getBarGraph() {
		// initially show that data is loading
		var element = document.getElementById('loading');
		element.style.display = 'block';
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

		let x = [];
		let y = [];
		let a = [];
		let b = [];
		for (let i = 1; i < team_data.length + 1; i++) {
			x.push({ Name: team_data[i - 1].team_name });
			y.push({ Commits: team_data[i - 1].number_of_commits });

			a.push(x[i - 1].Name);
			b.push(y[i - 1].Commits);
		}

		var modified_data = [
			{
				x: a,
				y: b,
				type: 'bar'
			}
		];

		let plotDiv = document.getElementById('plotDiv');
		element.style.display = 'none';
		Plotly.newPlot(
			plotDiv,
			modified_data,
			{ autosize: true, width: innerWidth * 0.4, height: innerHeight * 0.3 },
			{ responsive: true }
		);
	}

	async function getBoxPlot() {
		var element = document.getElementById('loading2');
		element.style.display = 'block';
		while (data_fetched != true) {
			await new Promise((r) => setTimeout(r, 5));
		}
		var box_data = new Array();
		for (let i = 1; i < table_data.length + 1; i++) {
			box_data.push({
				y: table_data[i - 1].Avg_score_array,
				type: 'box',
				name: table_data[i - 1].Name
			});
		}
		let plotDiv2 = document.getElementById('myDiv');
		element.style.display = 'none';
		Plotly.newPlot(
			plotDiv2,
			box_data,
			{ autosize: true, width: innerWidth * 0.4, height: innerHeight * 0.35 },
			{ responsive: true }
		);
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

	const settings = {
		columnFilter: true,
		rowsPerPage: 30,
		sortable: true,
		labels: { search: 'Search Team' }
	};

	function sprint_changed(event) {
		sprint = event.detail.value;
		team_data = {};
		student_data = {};
		student_list = {};
		student_table_data = new Array();
		getCommits();
		getBarGraph();
		getBoxPlot();
	}

	function re_render_box_plot() {
		data_fetched = true;
		getBoxPlot();
		data_fetched = false;
	}

	function re_render_bar_graph() {
		let a = [];
		let b = [];
		for (let i = 1; i < table_data.length + 1; i++) {
			a.push(table_data[i - 1].Name);
			b.push(table_data[i - 1].Commits);
		}

		var modified_data = [
			{
				x: a,
				y: b,
				type: 'bar'
			}
		];

		let plotDiv = document.getElementById('plotDiv');
		Plotly.newPlot(
			plotDiv,
			modified_data,
			{ autosize: true, width: innerWidth * 0.4, height: innerHeight * 0.3 },
			{ responsive: true }
		);
	}

	onMount(() => {
		courseName = getParameterByName('course');
		let script1 = document.createElement('script');
		script1.src = 'https://cdn.plot.ly/plotly-2.14.0.min.js';
		document.head.append(script1);
		script1.onload = () => {
			getBarGraph();
			getBoxPlot();
		};

		// script to load muuri open source grids
		let script2 = document.createElement('script');
		script2.src = 'https://cdn.jsdelivr.net/npm/muuri@0.9.5/dist/muuri.min.js';
		document.head.append(script2);
		script2.onload = () => {
			var grid = new Muuri('.grid', {
				dragEnabled: true,
				dragHandle: '.grid-content > h3, .item-content > h3, .grid-content > div > h3',
				layout: {
					rounding: false
				}
			});
		};
	});
</script>

<svelte:head>
	<script src="https://cdn.plot.ly/plotly-2.14.0.min.js" type="text/javascript"></script>
</svelte:head>
<svelte:window bind:innerWidth bind:innerHeight />
<DefaultLayout {courseName}>
	<section>
		<Breadcrumbs>
			<a href="/dashboard">Dashboard</a>
			<a href="/dashboard/course?course={courseName}">{courseName}</a>
			<p>Teams</p>
		</Breadcrumbs>
	</section>

	<SprintSelector on:message={sprint_changed} {courseName} />

	<div style="visibility:hidden ;">
		<ManageCourseButton url={'/dashboard/course/course-data?courseName=' + courseName} />
	</div>

	<section class="team-name">
		<h1>{courseName + ' Teams'}</h1>
	</section>

	<div class="grid">
		<!--insert a table in the column-->
		<div class="item item1">
			<div class="item-content">
				<h3>Teams Info</h3>
				<!--insert a bar chart for team score-->
				<section>
					{#await getCommits()}
						<p class="loader" />
					{:then data}
						<Datatable {settings} data={table_data} bind:dataRows={rows}>
							<thead style="display:inline-table; width : 100%;">
								<th style="padding: 2rem" data-key="Name"> Team Name</th>
								<th style="padding: 2rem" data-key="Commits"> Total Commits</th>
								<th style="padding: 2rem" data-key="Avg_score_mean">Mean Peer Score</th>
							</thead>
							<tbody style="display:block;">
								{#if rows}
									{#each $rows as row}
										<tr>
											<td>
												<a href="/dashboard/teams/team?team_name={row.Name}&course={courseName}"
													>{row.Name}</a
												>
											</td>
											<td>
												{row.Commits}
											</td>
											<td>
												{row.Avg_score_mean}
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
			<div class="grid-content">
				<div>
					<h3>
						<img title="Github Logo" src={git} alt="github-logo" /> Github Commits
						<img
							src={refreshImg}
							title="Sort Bar Graph"
							alt="Sort Bar Graph"
							on:click={re_render_bar_graph}
						/>
					</h3>
				</div>

				<section id="plotDiv">
					<p class="loader" id="loading" />
				</section>
			</div>
		</div>
		<div class="item item3">
			<div class="grid-content">
				<h3>
					Team Avg. Peer Score <img
						on:click={re_render_box_plot}
						title="Sort Box Plot"
						src={refreshImg}
						alt="Sort Boxplot"
					/>
				</h3>
				<section id="myDiv">
					<p class="loader" id="loading2" />
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
	tr:nth-of-type(odd) {
		background-color: rgb(195, 226, 201);
	}

	td {
		text-align: center;
		padding: 4px 0;
	}

	.team-name {
		display: flex;
		margin: 1rem min(5rem, 5vw);
		align-items: center;
		justify-content: center;
	}
	.team-name {
		display: flex;
		align-items: center;
		margin: 1rem 5rem;
		justify-content: center;
		margin-top: -1rem;
	}
	.team-name > h1 {
		flex: 2;
		margin: 0;
		font-size: 24pt;
		font-weight: normal;
		text-align: center;
	}

	/* TODO: Responsive mobile layout will require columns to be stacked
             (use media query) */
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
		min-width: 45vw;
		width: 45vw;
		height: 75vh;
		margin-left: 0.5rem;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		margin-top: 0.5vh;
	}
	.item1 > div > section {
		position: relative;
		width: 100%;
		height: 90%;
		text-align: center;
		background: rgb(255, 255, 255);
		font-size: 1rem;
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
		width: 42vw;
		height: 37vh;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		background-color: white;
		margin-left: 0.5rem;
		overflow: auto;
		margin-top: 0.5vh;
	}
	.item2 > div > section {
		position: relative;
		max-width: fit-content;
		height: 100%;
		text-align: center;
		background: rgb(255, 255, 255);
		font-size: 15px;
		color: rgb(0, 0, 0);
		cursor: default;
		margin: auto;
		/* overflow: auto; */
	}

	.item3 {
		position: absolute;
		margin-bottom: auto;
		width: 42vw;
		height: 37vh;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		background-color: white;
		margin-left: 0.5rem;
		overflow: auto;
		margin-top: 0.5vh;
	}
	.item3 > div > section {
		position: relative;
		max-width: fit-content;
		height: 100%;
		text-align: center;
		background: rgb(255, 255, 255);
		font-size: 15px;
		color: rgb(0, 0, 0);
		cursor: default;
		margin: auto;
		/* overflow: auto; */
	}
	.grid-content > h3 {
		text-align: center;
		font-size: 20px;
		color: rgb(0, 0, 0);
		width: auto;
		margin: auto;
		padding: 0.5rem;
		cursor: pointer;
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

	.grid-content > h3 > img {
		height: 20px;
		width: 2rem;
		display: inline;
	}
	.grid-content > h3 > img:hover {
		background: rgb(228, 228, 228);
	}

	.grid-content > div > h3 > img {
		height: 20px;
		width: 2rem;
		display: inline;
	}

	.grid-content > div > h3 > img:hover {
		background: rgb(228, 228, 228);
	}
	.grid-content > div {
		display: flex;
		justify-content: center;
		align-items: center;
		cursor: pointer;
	}
	.team-name > h1 {
		font-weight: 400;
		flex: 2;
		font-size: 1.5rem;
		margin: 0;
		text-align: center;
	}
</style>
