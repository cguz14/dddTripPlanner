'use strict';

const btn1s = document.querySelectorAll('#green');
const btn2s = document.querySelectorAll('#red');
let ratings
start();

// User clicks thumbs up button
for (let i=0; i < btn1s.length; i++) {

	let btn1 = btn1s[i]
	let btn2 = btn2s[i]

	let liked

	btn1.addEventListener('click', function(evt) {

		let restaurantId = document.getElementById(`fav-id-${i+1}`).innerHTML;

		evt.preventDefault();
		if (btn2.classList.contains('red')) {
			btn2.classList.remove('red');
		}

		this.classList.toggle('green');
   
		liked = true
		fetch(`/change-likes.json?restaurantId=${restaurantId}&liked=${liked}`)
		.then((response) => response.text())
		.then(changeThumb);

	});
}

// User clicks thumbs down button
for (let i=0; i < btn2s.length; i++) {

	let btn1 = btn1s[i]
	let btn2 = btn2s[i]

	let liked

	btn2.addEventListener('click', function(evt) {
	
		let restaurantId = document.getElementById(`fav-id-${i+1}`).innerHTML;

		console.log(restaurantId)

		evt.preventDefault();
		if (btn1.classList.contains('green')) {
			btn1.classList.remove('green');
		} 
		
		this.classList.toggle('red');

		liked = false
		fetch(`/change-likes.json?restaurantId=${restaurantId}&liked=${liked}`)
		.then((response) => response.text())
		.then(changeThumb);

	});
}

function changeThumb(results) {
	console.log('thumb changed');
	console.log(results);
}

function startingThumbs(results) {

	ratings = results;
	console.log(ratings);

	for (let n=0; n < ratings.length; n++) {
		
		let rating = ratings[n]

		for (let i=0; i < btn1s.length; i++) {

			let btn1 = btn1s[i]
			let btn2 = btn2s[i]

			const restaurantId = document.getElementById(`fav-id-${i+1}`).innerHTML;

			if (rating['restaurant_id'] == restaurantId) {
				if(rating['thumbs_up']) {
					btn1.classList.toggle('green')
					console.log('got in the green')
				}
				else {
					btn2.classList.toggle('red')
					console.log('got in the red')
				};
			};   
		};
	};
}

function start() {

	fetch('/api/ratings.json')
	.then((response) => response.json())
	.then(startingThumbs)

}