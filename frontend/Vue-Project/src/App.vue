<template> <!-- HTML -->
	<div>
		<h1>Thirsty Plant</h1>
    <h2>{{ message }}</h2>
		<button @click="changeMessage">Change Message</button>
	</div>
</template>

<script>

export default { // JavaScript
	data() {
		return {
			message: "Test Output"
		}
	},

	async mounted() {
		const res = await fetch ("http://uab420.desverreaux.com:8000/api/hello")
		const data = await res.json()
		this.message = data.message
	},
 
	methods: {
		changeMessage() {
			this.message = "Button Clicked"
		}
	}
}

</script>

<style> /* CSS */
body {
	background-color: #5f464b;
}

h1 {
  font-family: "Merriweather";
  font-size: 4em; /* pm = pixels, em/% = relative to parent element (default is 1em = 16px), rem = relative to html element --> Can also use xx-small to xx-large*/
  font-weight: bold; /*lighter, normal, bold, bolder*/
  font-style: oblique 10deg; /*normal, italic, etc*/
  text-align: left;
  text-decoration: underline; /*Can be customized*/

  color: #a6b07e
}
</style>
