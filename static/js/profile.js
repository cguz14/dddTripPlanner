'use strict';

function replaceUsername(results) {
	document.querySelector('#username-span').innerHTML = results;
	document.querySelector('#username-header-span').innerHTML = results;
	alert("Username Updated");
}

function newUsername(evt) {
	evt.preventDefault();
	const newUsername = document.querySelector('#new-username-field').value;

	fetch(`/change-username.json?newUsername=${newUsername}`)
		.then((response) => response.text())
		.then(replaceUsername);

}

document.querySelector('#change-username-form').addEventListener('submit', newUsername);