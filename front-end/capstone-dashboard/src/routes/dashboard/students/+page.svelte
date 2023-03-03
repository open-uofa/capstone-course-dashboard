<script>
	import { onMount } from 'svelte';
	import Breadcrumbs from '$lib/Breadcrumbs.svelte';
	import ManageCourseButton from '$lib/ManageCourseButton.svelte';
	import SprintSelector from '$lib/SprintSelector.svelte';
	import { writable } from 'svelte/store';
	import { variables } from '$lib/variables';
	import { Datatable } from 'svelte-simple-datatables';
	import { page } from '$app/stores';
	import DefaultLayout from '$lib/DefaultLayout.svelte';
	import refreshImg from '$lib/images/refresh-plot.svg';
	import { refresh } from '$lib/refresh';
	// use current_course in all backend calls when user session is active
	let current_course = '';
	let current_path = current_course + ' - Students';
	export let plotHeader = '';

	let rows = writable([]);
	var student_data = {};
	var student_list = {};
	var table_data = new Array();
	let selected_sprint = 0;
	let data_fetched = false;
	let threshold_bar = '';
	let innerWidth = 0;
	let innerHeight = 0;

	// function  to populate the table with data and store data for plotly
	async function getStudentInfo() {
		data_fetched = false;
		// replace course1 with current_course when user session is working
		const res = await fetch(
			variables.basePath + '/students/' + current_course + '/' + selected_sprint,
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
			.then((data) => (student_data = data))
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
		student_list = student_data.students;

		// store all student information in table_data
		table_data = new Array();
		for (let i = 1; i < student_list.length + 1; i++) {
			table_data.push({
				id: i,
				Email: student_list[i - 1].email,
				Name: student_list[i - 1].full_name,
				Project: student_list[i - 1].project,
				Git: student_list[i - 1].source_control_username,
				Avg_score: 0,
				Count: 0
			});
		}

		// add average score and count to table_data
		for (let k = 1; k < student_data.sprint_data.length + 1; k++) {
			for (let i = 1; i < student_data.students.length + 1; i++) {
				if (table_data[i - 1].Email === student_data.sprint_data[k - 1].email) {
					table_data[i - 1].Avg_score =
						table_data[i - 1].Avg_score + student_data.sprint_data[k - 1].avg_rating;
					table_data[i - 1].Count = table_data[i - 1].Count + 1;
					break;
				}
			}
		}

		// calculate average score
		for (let i = 1; i < student_data.students.length + 1; i++) {
			table_data[i - 1].Avg_score = (table_data[i - 1].Avg_score / table_data[i - 1].Count).toFixed(
				2
			);
		}

		// set data_fetched to true so that plotly can be rendered
		data_fetched = true;
	}

	// use this function to update bar graph once getsStudentInfo() fetches all data
	// this function is not making api calls to backend
	// using the data fetched by getStudentInfo() to reduce network usage and increase performance
	async function getBarGraph() {
		// initially show that data is loading
		var element = document.getElementById('loading');
		element.style.display = 'block';

		// check for data_fetched to be true and once it is true, render the plotly
		while (data_fetched != true) {
			await new Promise((r) => setTimeout(r, 5));
		}
		var x = [];
		var y = [];
		var a = [];
		var b = [];

		// store student names and average scores in x and y
		// then transform the data so that it can be used with plotly format
		for (let i = 1; i < student_list.length + 1; i++) {
			x.push({ Name: table_data[i - 1].Name });
			y.push({ Avg_score: table_data[i - 1].Avg_score });

			a.push(x[i - 1].Name);
			b.push(y[i - 1].Avg_score);
		}

		var modified_data = [
			{
				x: a,
				y: b,
				type: 'bar',
				marker: {
					color: y.map((d) => (d.Avg_score > threshold_bar ? 'royalblue' : 'red'))
				}
			}
		];

		let plotDiv = document.getElementById('plotDiv');
		element.style.display = 'none';
		Plotly.newPlot(
			plotDiv,
			modified_data,
			{
				autosize: true,
				width: innerWidth * 0.4,
				height: innerHeight * 0.35
			},

			{ responsive: true }
		);
	}

	// use this function to update boxplot graph once getsStudentInfo() fetches all data
	// this function is not making api calls to backend
	// using the data fetched by getStudentInfo() to reduce network usage and increase performance
	async function getBoxPlot() {
		var element = document.getElementById('loading2');
		element.style.display = 'block';
		while (data_fetched != true) {
			await new Promise((r) => setTimeout(r, 5));
		}
		var y = [];

		var b = [];
		for (let i = 1; i < table_data.length + 1; i++) {
			y.push({ Avg_score: table_data[i - 1].Avg_score });

			b.push(y[i - 1].Avg_score);
		}

		var modified_data = [
			{
				y: b,
				type: 'box',
				name: 'Peer Score',
				marker: {
					color: 'rgb(214,12,140)'
				}
			}
		];

		let plotDiv2 = document.getElementById('myDiv');
		element.style.display = 'none';
		Plotly.newPlot(
			plotDiv2,
			modified_data,
			{ autosize: true, width: innerWidth * 0.4, height: innerHeight * 0.35 },
			{ responsive: true }
		);
		data_fetched = false;
	}

	// settings are used in the data table
	const settings = {
		columnFilter: true,
		rowsPerPage: 20,
		sortable: true,
		scrollY: true,
		labels: {
			search: 'Search Student', // search input placeholer
			filter: 'Filter', // filter inputs placeholder
			noRows: 'No entries to found'
		}
	};

	// this function updates the graphs and data table once the user selects a project
	function sprint_changed(event) {
		selected_sprint = event.detail.value;
		student_data = {};
		student_list = {};
		getStudentInfo();
		getBarGraph();
		getBoxPlot();
	}

	// this function is used to display red flags on bar graph
	function red_flag_bar_graph() {
		data_fetched = true;
		getBarGraph();
		data_fetched = false;
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

	async function get_course_name() {
		current_course = getParameterByName('course');
		current_path = current_course + ' Students';
	}

	onMount(() => {
		// with svelte routing module, when you navigate around, plotly goes out of wack.
		// this is a hacky fix to make it work
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
				dragHandle: '.grid-content > h3,.grid-content >div> h3, .item-content > h3 ',
				layout: {
					rounding: false
				}
			});
		};
	});
</script>

<svelte:head>
	<script src="https://cdn.plot.ly/plotly-2.14.0.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/muuri@0.9.5/dist/muuri.min.js"></script>
</svelte:head>
<svelte:window bind:innerWidth bind:innerHeight />
<DefaultLayout courseName={current_course}>
	<section class="crumbs">
		<Breadcrumbs>
			<a href="./">Dashboard</a>
			<a href="./course?course={current_course}">{current_course}</a>
			<p>Students</p>
		</Breadcrumbs>
	</section>

	{#await get_course_name() then data}
		<SprintSelector on:message={sprint_changed} courseName={current_course} />
	{/await}

	<!-- <SprintSelector on:message={sprint_changed} courseName={current_course} /> -->
	<div style="visibility:hidden ;">
		<ManageCourseButton url={'/dashboard/course/course-data?courseName=' + current_course} />
	</div>

	<section class="course-name">
		<h1>{current_path}</h1>
	</section>

	<div class="grid">
		<div class="item item1">
			<div class="item-content">
				<h3>Student Info</h3>
				<section>
					{#await getStudentInfo()}
						<p class="loader" />
					{:then data}
						<Datatable {settings} data={table_data} bind:dataRows={rows}>
							<thead style="display:inline-table; width : 100%;">
								<!-- keys are used to sort data -->
								<th style="padding: 2rem;" data-key="Name"> Name</th>
								<th style="padding: 2rem;" data-key="Project"> Project</th>
								<th style="padding: 2rem;" data-key="Avg_score">Avg. Peer rating</th>
							</thead>
							<tbody style="display:block;">
								{#if rows}
									{#each $rows as row}
										<tr>
											<td
												><a
													href="/dashboard/students/personal_student?student={row.Name}&course={current_course}&email={row.Email}&Git={row.Git}"
													>{row.Name}</a
												></td
											>
											<td style="width: 100px; word-wrap: break-word;">{row.Project}</td>
											<td>{row.Avg_score}</td>
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
					<h3>Avg. Peer Score</h3>
					<input
						bind:value={threshold_bar}
						placeholder="Red Flag Threshold"
						type="number"
						step="0.1"
						min="0"
						on:change={red_flag_bar_graph}
					/>
					<img
						src={refreshImg}
						alt="re-render bar graph"
						title="Sort Bar Graph"
						on:click={red_flag_bar_graph}
					/>
				</div>

				<section id="plotDiv">
					<p class="loader" id="loading" />
					<!-- Plotly chart will be drawn inside this DIV -->
				</section>
			</div>
		</div>

		<div class="item item3">
			<div class="grid-content">
				<h3>Peer Score</h3>
				<section id="myDiv">
					<p class="loader" id="loading2" />
					<!-- Plotly chart will be drawn inside this DIV -->
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

	:global(body) {
		background-color: hsl(0, 0%, 90%);
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
	.grid-content > div > input {
		margin-left: 00.5rem;
	}

	.grid-content > div > h3 {
		cursor: pointer;
	}

	.item3 > div > h3 {
		cursor: pointer;
	}
	.grid-content > div > img {
		height: 20px;
		width: 2rem;
		display: inline;
	}

	.grid-content > div > img:hover {
		background: rgb(228, 228, 228);
		cursor: pointer;
	}
</style>
