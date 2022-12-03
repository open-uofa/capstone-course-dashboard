<script>
	import Breadcrumbs from '$lib/Breadcrumbs.svelte';
	import DefaultLayout from '$lib/DefaultLayout.svelte';
	import ManageCourseButton from '$lib/ManageCourseButton.svelte';
	import git from '$lib/images/git-logo.svg';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import SprintSelector from '$lib/SprintSelector.svelte';
	import { variables } from '$lib/variables';
	import { refresh } from '$lib/refresh';

	let courseName = getParameterByName('course');
	let studentName = '';
	let sprint = 0;
	let teamName = '';
	let student_email = '';
	export const plotHeader = '';

	let student_data = {};
	let student_list = {};
	let sprint_data = {};
	let student_info = {};
	let peer_review_data = {};
	let peer_review_list = {};
	let innerWidth = 0;
	let innerHeight = 0;
	let git_name = '';
	let git_count = 0;

	let data_fetched = false;
	let commits = {};

	async function getStudentInfo() {
		student_list = {};
		sprint_data = {};
		peer_review_list = {};

		while (student_email == '') {
			await new Promise((r) => setTimeout(r, 5));
		}

		await fetch(
			variables.basePath + '/students/' + courseName + '/' + sprint + '/' + student_email,
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
			.then((data) => {
				student_data = data;

				student_list = student_data.students;
				sprint_data = student_data.sprint_data;
			})
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
		student_info = {};

		student_info['full_name'] = student_list[0].full_name;
		student_info['email'] = student_list[0].email;
		student_info['ta'] = student_list[0].ta;
		student_info['project'] = student_list[0].project;
		student_info['experience_survey'] = student_list[0].experience_survey;
		student_info['repo_name'] = student_list[0].repo_name;

		//watch over for sprint data with different sprint, the data strcutre
		//get its corresponding sprint in sprint_data
		if (sprint != 0) {
			for (let j = 0; j < sprint_data.length; j++) {
				if (sprint_data[j].sprint == sprint) {
					peer_review_data = sprint_data[j].received_peer_revs;
				}
			}
		} else {
			//gets save all sprints in sprint data to peer review data
			peer_review_data = sprint_data[0].received_peer_revs;
			for (var entry in peer_review_data) {
				peer_review_data[entry].rating = [peer_review_data[entry].rating];
				peer_review_data[entry].what_did_they_do = [peer_review_data[entry].what_did_they_do];
			}

			for (let j = 1; j < sprint_data.length; j++) {
				//same rating from same email under the same key of sprint_data[j].received_peer_revs
				for (var entry in sprint_data[j].received_peer_revs) {
					if (entry in peer_review_data) {
						//concat the rating and comment
						peer_review_data[entry].rating.push(sprint_data[j].received_peer_revs[entry].rating);

						peer_review_data[entry].what_did_they_do.push(
							sprint_data[j].received_peer_revs[entry].what_did_they_do
						);
					} else {
						peer_review_data[entry] = sprint_data[j].received_peer_revs[entry];
					}
				}
			}
		}

		var rating;
		var task;
		peer_review_list = {};

		//loop through each peer review
		for (var entry in peer_review_data) {
			rating = peer_review_data[entry].rating;
			task = peer_review_data[entry].what_did_they_do;
			peer_review_list[entry] = [task, rating];
		}

		const con = await fetch(
			variables.basePath + '/student/' + courseName + '/' + sprint + '/' + git_name + '/commits',
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
			.then((data) => (commits = data))
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
		data_fetched = true;
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

	async function getBoxPlot() {
		await getStudentInfo();
		var b = [];
		//for each key in peer_review_list
		if (sprint == 0) {
			for (var key in peer_review_list) {
				//if sprint is 0
				for (var i = 0; i < peer_review_list[key][1].length; i++) {
					b.push(peer_review_list[key][1][i]);
				}
			}
		} else {
			for (var key in peer_review_list) {
				b.push(peer_review_list[key][1]);
			}
		}
		var data2 = [
			{
				y: b,
				type: 'box',
				name: 'Peer Review Score',
				marker: {
					color: 'rgb(214,12,140)'
				}
			}
		];

		let scorePlot = document.getElementById('score_plot');
		Plotly.newPlot(
			scorePlot,
			data2,
			{ autosize: true, width: innerWidth * 0.4, height: innerHeight * 0.35 },
			{ responsive: true }
		);
	}

	function sprint_changed(event) {
		sprint = event.detail.value;

		getStudentInfo();
		getBoxPlot();
	}

	onMount(() => {
		try {
			studentName = getParameterByName('student');
			courseName = getParameterByName('course');
			teamName = getParameterByName('team_name');
			student_email = getParameterByName('email');
			git_name = getParameterByName('Git');
			git_count = getParameterByName('Git-Count');
		} catch (error) {
			console.log('Failed to get parameters');
		}
		let script1 = document.createElement('script');
		script1.src = 'https://cdn.plot.ly/plotly-2.14.0.min.js';
		document.head.append(script1);
		script1.onload = () => {
			getBoxPlot();
		};

		// script to load muuri open source grids
		let script2 = document.createElement('script');
		script2.src = 'https://cdn.jsdelivr.net/npm/muuri@0.9.5/dist/muuri.min.js';
		document.head.append(script2);
		script2.onload = () => {
			var grid = new Muuri('.grid', {
				dragEnabled: true,
				dragHandle: '.grid-content > h3,.grid-content >div> h3, .item-content>h3 ',
				layout: {
					rounding: false
				}
			});
		};
	});
</script>

<svelte:window bind:innerWidth bind:innerHeight />

<svelte:head>
	<script
		src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/1.33.1/plotly.min.js"
		type="text/javascript"
	></script>
</svelte:head>

<DefaultLayout {courseName}>
	<section>
		<Breadcrumbs>
			<a href="../">Dashboard</a>
			<a href="../course?course={courseName}">{courseName}</a>
			<a href="../students?course={courseName}">Students</a>
			<p>{studentName}</p>
		</Breadcrumbs>
	</section>

	<SprintSelector on:message={sprint_changed} {courseName} />

	<div style="visibility:hidden ;">
		<ManageCourseButton url={'/dashboard/course/course-data?courseName=' + courseName} />
	</div>

	<section class="student-name">
		<h1>{studentName}</h1>
	</section>

	<div class="grid">
		<div class="item item1">
			<div class="item-content">
				<h3>Details</h3>
				{#await getStudentInfo() then data}
					<p>loading...</p>

					<section>
						<p>Full Name: {student_info.full_name}</p>
						<p>Email: {student_info.email}</p>
						<p>Team: {student_info.project}</p>

						<p>TA: {student_info.ta}</p>
					</section>
				{/await}
			</div>
		</div>

		<div class="item item2">
			<div class="grid-content github-commits">
				<div>
					<h3><img src={git} alt="github-logo" /> Github Commits</h3>
				</div>
			</div>
			{#if git_count > 0}
				<p><center>{git_count}</center></p>
			{:else}
				<p>
					<center>
						{commits.number_of_commits}
					</center>
				</p>
			{/if}
		</div>
		<div class="item item3">
			<div class="grid-content">
				<div>
					<h3>Experience</h3>
				</div>
				{#await getStudentInfo() then data}
					<section>
						<p>Courses Taken: {student_info.experience_survey.course_work}</p>
						<p>Experience: {student_info.experience_survey.experience}</p>
						<p>{student_info.experience_survey.langs}</p>
						<p>Expectation: {student_info.experience_survey.hopes}</p>
						<p>{student_info.experience_survey.diffs}</p>
					</section>
				{/await}
			</div>
		</div>
		<div class="item item4">
			<div class="grid-content peer-review-score">
				<div>
					<h3>Peer Review Score</h3>
				</div>
				<section id="plotly">
					<div id="score_plot" />
					<p class="loader" id="loading2" />
				</section>
			</div>
		</div>
		<div class="item item5">
			<div class="grid-content">
				<div>
					<h3>Peer Review Content</h3>
				</div>
				<section>
					{#if sprint == 0}
						<p>
							<center>Please Select a Sprint to View This Student's Peer Review Ratings</center>
						</p>
					{:else}
						Peer Reviews:
						{#each Object.keys(peer_review_list) as key}
							<p>email:{key}</p>

							<p>rating: {peer_review_list[key][1]}</p>
							<p>comment: {peer_review_list[key][0]}</p>
							<br />
						{/each}
					{/if}
				</section>
			</div>
		</div>
	</div>
</DefaultLayout>

<style>
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
	.student-name {
		display: flex;
		align-items: center;
		margin: 1rem 5rem;
		justify-content: center;
		margin-top: -1rem;
	}

	.student-name > h1 {
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
		min-width: 35vw;
		width: 43vw;
		height: 30vh;
		margin-left: 0.5rem;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		margin-top: 0.5vh;
		background: rgb(255, 255, 255);
		overflow: auto;
	}

	.item1 > div {
		height: auto;
	}
	.item1 > div > section {
		position: relative;

		height: 100%;
		text-align: center;
		background: rgb(255, 255, 255);
		font-size: 15px;
		color: rgb(0, 0, 0);
		cursor: pointer;
		margin: auto;
	}
	.item1 > div > section > p {
		margin-left: auto;
		margin-right: auto;
	}
	.item2 {
		position: absolute;
		width: 43vw;
		height: 20vh;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		background-color: white;
		margin-left: 0.5rem;
		overflow: auto;
		margin-top: 0.5vh;
	}
	.item2 > p {
		font-size: 1.5rem;
	}

	.item3 {
		position: absolute;
		margin-bottom: auto;
		width: 43vw;
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
		cursor: pointer;
		margin: auto;
		/* overflow: auto; */
	}

	.item4 {
		position: absolute;
		width: 43vw;
		height: 65vh;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		background-color: white;
		margin-left: 0.5rem;
		overflow: auto;
		margin-top: 0.5vh;
	}

	.item4 > div > section {
		position: relative;
		max-width: fit-content;
		height: 100%;
		text-align: center;
		background: rgb(255, 255, 255);
		font-size: 15px;
		color: rgb(0, 0, 0);
		cursor: pointer;
		margin: auto;
		/* overflow: auto; */
	}

	.item5 {
		position: absolute;
		margin-bottom: auto;
		width: 43vw;
		height: 37vh;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		background-color: white;
		margin-left: 0.5rem;
		overflow: auto;
		margin-top: 0.5vh;
	}

	.item5 > div > section {
		position: relative;
		max-width: fit-content;
		height: 100%;
		text-align: center;
		background: rgb(255, 255, 255);
		font-size: 15px;
		color: rgb(0, 0, 0);
		cursor: pointer;
		margin: auto;
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

	.grid-content > div > h3 {
		cursor: pointer;
	}
</style>
