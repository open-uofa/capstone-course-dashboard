<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { variables } from '$lib/variables';
	import { writable } from 'svelte/store';
	import { Datatable } from 'svelte-simple-datatables';
	import Breadcrumbs from '$lib/Breadcrumbs.svelte';
	import DefaultLayout from '$lib/DefaultLayout.svelte';
	import Modal from './Modal.svelte';
	import ModalList from '$lib/ModalList.svelte';
	import ModalListItem from '$lib/ModalListItem.svelte';
	import SprintSelector from '$lib/SprintSelector.svelte';
	import RefreshButton from '$lib/RefreshButton.svelte';
	import { refresh } from '$lib/refresh.js';

	let courseName = getParameterByName('course');
	let teamName = getParameterByName('team_name');
	let sprint = 0;
	let student_commits = new Array();
	let commits_last_fetched_at = 'Never';
	let commits = new Array();
	let meetingMinutes = new Array();
	let teamComments = new Array();

	let rows = writable([]);
	let modal;
	let innerWidth = 0;
	let innerHeight = 0;

	//settings for datatable
	const setting = {
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

	var student_names = new Array();
	var student_data = {};
	var student_list = {};
	//fetch all students names from backend
	async function getStudentNames() {
		await fetch(`${variables.basePath}/students/${courseName}/${sprint}`, {
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

		for (var i = 0; i < student_list.length; i++) {
			student_names.push({
				full_name: student_list[i].full_name,
				user_name: student_list[i].source_control_username,
				email: student_list[i].email
			});
		}
	}

	// fetch one team's repo's data, fill it in student_commits
	async function getCommits() {
		await getStudentNames();

		await fetch(`${variables.basePath}/team/${courseName}/${sprint}/commits/${teamName}`, {
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
			.then((data) => {
				student_commits = new Array();
				for (let i = 0; i < data.student_commits.length; i++) {
					//use student's user name in student_namaes to get full name
					let full_name = 'Does not exist';
					let email = 'Does not exist';
					for (let j = 0; j < student_names.length; j++) {
						if (student_names[j].user_name == data.student_commits[i].username) {
							full_name = student_names[j].full_name;
							email = student_names[j].email;
							break;
						} else {
							full_name = data.student_commits[i].username + ' (Github)';
						}
					}

					student_commits.push({
						id: i,
						Student: full_name,
						Email: email,
						Commits: data.student_commits[i].number_of_commits
					});
				}
				if (data.last_fetched_at) {
					commits_last_fetched_at = new Date(data.last_fetched_at).toString();
				}
			})
			.catch((error) => {
				console.log('There has been a problem with your fetch operation: ', error.message);
			});
	}

	async function getMeetingMinutes() {
		return await fetch(`${variables.basePath}/minutes/${courseName}/${teamName}/${sprint}`, {
			headers: {
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			}
		}).then((res) => {
			if (res.status === 401) {
				refresh();
			}
			return res.status === 200 ? res.json() : {};
		});
	}

	async function updateMeetingMinutes() {
		// Request database update
		// Use GitHub owner from environment file. This is typically the organization
		// name that owns the repositories.
		await fetch(
			`${variables.basePath}/minutes/${courseName}/${variables.githubOwner}/${teamName}`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
				}
			}
		).then((response) => {
			if (response.status === 401) {
				refresh();
			}
		});

		meetingMinutes = await getMeetingMinutes();
	}

	//get team's TA notes
	async function getNotes() {
		if (teamComments) teamComments = new Array();

		await fetch(`${variables.basePath}/teams/${courseName}/${sprint}/${teamName}/comments`, {
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
			.then((data) => {
				for (let i = 0; i < data.length; i++) {
					data[i].created_at = new Date(data[i].created_at).toString().substr(0, 16);

					teamComments.push({
						id: data[i].id,
						comment: data[i].message,
						created: data[i].created_at,
						lastModified: data[i].last_modified_at
					});
				}
			})
			.catch((error) => {
				console.log(`Failed to retrieve notes: ${error.message}`);
			});

		teamComments = teamComments;
	}

	// changes in this function
	async function github() {
		const res = await fetch(variables.basePath + '/github/', {
			method: 'POST',
			headers: {
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt'),
				'Content-Type': 'application/json;charset=utf-8'
			},
			body: JSON.stringify({
				owner: variables.githubOwner,
				repo: teamName,
				course_name: courseName
			})
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				//update datatable & graph
				getBarGraph();
				getCommits();
				return response.json();
			})
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
	}

	async function getBarGraph() {
		var element = document.getElementById('loading');
		if (element) element.style.display = 'block';
		const res = await fetch(
			`${variables.basePath}/team/${courseName}/${sprint}/commits/${teamName}`,
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
			.then((data) => (commits = data.student_commits))
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});

		let x = [];
		let y = [];
		let a = [];
		let b = [];
		for (let i = 1; i < commits.length + 1; i++) {
			x.push({ Name: commits[i - 1].username });
			y.push({ Commits: commits[i - 1].number_of_commits });

			a.push(x[i - 1].Name);
			b.push(y[i - 1].Commits);
		}

		var data = [
			{
				x: a,
				y: b,
				type: 'bar'
			}
		];

		let commitPlot = document.getElementById('commit_plot');
		if (element) element.style.display = 'none';
		Plotly.newPlot(
			commitPlot,
			data,
			{ autosize: true, width: innerWidth * 0.42, height: innerHeight * 0.3 },
			{ showSendToCloud: false }
		);
	}

	function onButtonClick() {
		modal.show();
	}

	// Update database with comment
	async function updateNote(commentId) {
		let comment = document.querySelector(`dialog textarea[id="${commentId}"]`);
		let newNote = {
			message: comment.value,
			team: teamName,
			sprint_number: sprint
		};

		fetch(`${variables.basePath}/teams/${courseName}/comments/${comment.id}`, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			},
			body: JSON.stringify(newNote)
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				getNotes();
				return response.json();
			})
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
	}

	// Delete passed in comment
	async function deleteNote(commentId) {
		fetch(`${variables.basePath}/teams/${courseName}/comments/${commentId}`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			}
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				getNotes();
				return response.json();
			})
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
	}

	// Add TA note based on TA's input in text_area, sends POST request
	// to backend and call update notes list
	async function addNote() {
		//do post request to backend
		const note = document.getElementById('edit_notes');

		let newNote = {
			message: note.value,
			team: teamName,
			sprint_number: sprint
		};

		fetch(`${variables.basePath}/teams/${courseName}/comments`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			},
			body: JSON.stringify(newNote)
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
				getNotes();
				return response.json();
			})
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
		modal.hide();
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

	function sprint_changed(event) {
		sprint = event.detail.value;
		getNotes();
		getBarGraph();
		getCommits();
		getMeetingMinutes();
		updateMeetingMinutes();
	}

	onMount(async () => {
		getBarGraph();

		teamName = getParameterByName('team_name');
		courseName = getParameterByName('course');

		let script1 = document.createElement('script');
		script1.src = 'https://cdn.plot.ly/plotly-2.14.0.min.js';
		document.head.append(script1);
		script1.onload = () => {
			getBarGraph();
		};

		meetingMinutes = await getMeetingMinutes();

		// script to load muuri open source grids
		let script2 = document.createElement('script');
		script2.src = 'https://cdn.jsdelivr.net/npm/muuri@0.9.5/dist/muuri.min.js';
		document.head.append(script2);
		script2.onload = () => {
			var grid = new Muuri('.columns', {
				dragEnabled: true,
				dragHandle:
					'.students > h2,.github_commits >div> h2, .meeting-minutes >h2, .ta_notes > header > h2',
				layout: {
					rounding: false
				}
			});
		};
	});

	async function checkAuth() {
		fetch(`${variables.basePath}/auth/check`, {
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Bearer ' + window.localStorage.getItem('jwt')
			}
		})
			.then((response) => {
				if (response.status === 401) {
					refresh();
				}
			})
			.catch((error) => {
				console.log('Error fetching data', error.message);
			});
	}
</script>

<!-- Get height and width of window so graph can use it for its ratio -->
<svelte:window bind:innerWidth bind:innerHeight />

<svelte:head>
	<script src="https://cdn.plot.ly/plotly-2.14.0.min.js" type="text/javascript"></script>
</svelte:head>

<!--FIXME: DefaultLayout not initialized with proper variables-->
{#await checkAuth() then}
	<DefaultLayout {courseName}>
		<section>
			<Breadcrumbs>
				<a href="/dashboard">Dashboard</a>
				<a href="/dashboard/course?course={courseName}">{courseName}</a>
				<a href="/dashboard/teams?course={courseName}">Teams</a>
				<p>{teamName}</p>
			</Breadcrumbs>

			<section class="team_name">
				<section>
					<SprintSelector on:message={sprint_changed} {courseName} />
				</section>
				<h1>{teamName}</h1>
			</section>

			<section class="columns">
				<!--insert a table in the column-->
				<section class="students">
					<h2>Students</h2>
					<div class="studentsTable">
						{#await getCommits()}
							<center>
								<p class="loader" />
							</center>
						{:then data}
							<Datatable {setting} data={student_commits} bind:dataRows={rows}>
								<thead>
									<th style="padding: 2rem" data-key="Student"> Student</th>
									<th style="padding: 2rem" data-key="Commits"> Total Commits</th>
								</thead>
								<tbody>
									{#if rows}
										{#each $rows as row}
											<tr>
												<td
													><a
														href="/dashboard/students/personal_student?student={row.Student}&course={courseName}&email={row.Email}&Git-Count={row.Commits}"
														>{row.Student}</a
													>
												</td>
												<td>
													<p>
														{row.Commits}
													</p>
												</td>
											</tr>
										{/each}
									{/if}
								</tbody>
							</Datatable>
						{/await}
					</div>
				</section>

				<section class="github_commits">
					<div class="git-heading">
						<p>Last fetched:{commits_last_fetched_at.substr(0, 24)}</p>
						<h2>Github Commits</h2>
						<button title="Update the Data Table and Bar Chart" on:click={github}
							>Fetch from<br />GitHub</button
						>
					</div>
					<div class="plot">
						<section id="commit_plot">
							<p class="loader" id="loading" />
						</section>
					</div>
				</section>

				<!-- Display TA notes and meeting minutes boxes -->
				<section class="meeting-minutes">
					<h2>Meeting Minutes</h2>
					<RefreshButton on:click={updateMeetingMinutes} />
					{#await getMeetingMinutes()}
						<center>
							<p class="loader" />
						</center>
					{:then}
						<ModalList>
							{#each meetingMinutes as meeting}
								<ModalListItem>
									<h3>{meeting.title}</h3>
									<p>{meeting.body}</p>
								</ModalListItem>
							{/each}
						</ModalList>
					{/await}
				</section>

				<section class="ta_notes">
					<header>
						<h2>TA Notes</h2>
						<button class="notes-btn1" on:click={onButtonClick}>Add Note</button>
					</header>

					{#await getNotes()}
						<center>
							<p class="loader" />
						</center>
					{:then}
						<ModalList>
							{#each teamComments as comment}
								<ModalListItem>
									<h3>{comment.created}</h3>
									<textarea id={comment.id}>{comment.comment}</textarea>
									<div class="update_btns">
										<button class="notes-btn2" on:click={updateNote(comment.id)}>Update</button>
										<button class="notes-btn3" on:click={deleteNote(comment.id)}>Delete</button>
									</div>
								</ModalListItem>
							{/each}
						</ModalList>
					{/await}
				</section>
				<!-- Display add note pop up -->
				<Modal bind:this={modal}>
					<h3>Add Note</h3>
					<textarea id="edit_notes" placeholder="Enter new TA notes here" />
					<button class="notes-btn2" on:click={addNote}>Create New Note</button>
				</Modal>
			</section>
		</section>
	</DefaultLayout>
{/await}

<style>
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

	.team_name {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 1rem;
	}

	.team_name > section {
		font-size: 14pt;
		margin-bottom: 3rem;
	}

	.team_name > h1 {
		flex: 2;
		margin: 0;
		font-size: 20pt;
		font-weight: normal;
		text-align: center;
	}

	.columns {
		position: relative;
		height: auto;
		width: auto;
		border: 1px solid rgba(255, 255, 255, 0);
		border-radius: 1rem;
		margin-left: 2vw;
		min-height: 65vh;
		overflow: hidden;
	}

	.columns > section {
		position: absolute;
		min-width: 35vw;
		width: 43vw;
		height: 36vh;
		margin-left: 0.5rem;
		z-index: 0;
		border: 2px solid hsl(0, 0%, 50%);
		border-radius: 1rem;
		margin-top: 0.5vh;
		background: rgb(255, 255, 255);
		overflow: auto;
	}

	.columns > section > div {
		position: relative;
	}

	.studentsTable {
		height: 80%;
	}

	.ta_notes > header > h2 {
		margin-top: 0;
		font-size: 14pt;
	}

	.ta_notes > header > h2:hover {
		cursor: pointer;
	}

	.columns > section > h2 {
		font-size: 14pt;
		text-align: center;
	}

	.columns > section > h2:hover {
		cursor: pointer;
	}

	.plot {
		display: flex;
		align-items: center;
		justify-content: left;
		overflow-x: auto;
	}

	tr:nth-of-type(odd) {
		background-color: rgb(195, 226, 201);
	}

	td {
		text-align: center;
		padding: 0.5px 0;
		font-size: 12px;
	}

	.students :global(section) {
		z-index: 0;
	}

	.meeting-minutes {
		overflow-y: hidden;
	}

	.meeting-minutes > :global(:nth-child(2)) {
		margin-left: auto;
		margin-right: 5%;
	}

	.meeting-minutes p {
		margin: 0;
		white-space: pre-wrap;
	}

	.meeting-minutes h3 {
		margin-top: 0;
	}

	.meeting-minutes > h2 {
		margin-bottom: 0rem;
	}

	header {
		display: grid;
		grid-template-columns: 20fr 1fr;
		list-style: none;
		padding-top: 1rem;
		text-align: center;
		padding-left: 5rem;
		font-size: 1.3rem;
	}

	.notes-btn1 {
		justify-content: center;
		padding: 0.8em;

		width: 5rem;
		height: clamp(fit-content, 50pt, 2rem);
		margin-right: 1rem;
		margin-top: auto;
		margin-bottom: auto;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
	}

	.notes-btn2 {
		margin-top: 2em;
		margin-right: auto;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		width: 8em;
	}

	.notes-btn3 {
		margin-top: 2em;
		margin-right: auto;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: red;
		width: 8em;
		margin-right: 0;
	}

	.update_btns {
		display: flex;
		flex-direction: row;
	}

	textarea {
		font-size: 10pt;
		border: 0;
		width: 100%;
		min-height: max(20vh, 20rem);
	}

	:global(dialog) textarea {
		min-height: max(22vh, 22rem);
	}

	.git-heading {
		margin-top: 0.2rem;
		align-items: center;
		display: flex;
		justify-content: space-between;
	}

	.git-heading > p {
		font-size: smaller;
		font-style: italic;
		color: rgb(25, 25, 25);
		display: inline;
		width: 11rem;
		margin-left: 0.5em;
	}
	.git-heading > h2 {
		text-align: center;
		margin: auto;
		margin-top: 1rem;
		font-size: 14pt;
		text-align: center;
		margin-right: 15%;
		margin-left: 5%;
	}
	.git-heading > button {
		margin-right: 0.5em;
		margin-top: 0.5em;
		padding: 0.5em;
		cursor: pointer;
		border: none;
		border-radius: 0.5rem;
		background-color: hsl(54, 78%, 60%);
		width: 8em;
	}

	.github_commits > div > section {
		margin-left: auto;
		margin-right: auto;
	}

	.github_commits > div > h2:hover {
		cursor: pointer;
	}
</style>
