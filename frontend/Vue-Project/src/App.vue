<template> <!-- HTML -->
	<div class="page">
    <header class="header">Thirsty Plant</header>
		
    <main class="content">
      <section class="main">{{ message }}</section>
		  <button @click="changeMessage">Change Message</button>
      <aside class="sidebar">Your Ad Here!</aside>
    </main>
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
		const res = await fetch ("http://uab420.desverreaux.com:8000/api/loremIpsum?wordCount=30")
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
/*
Evergreen - #0E2F15
Dark Spruce - #14591D
Dry Sage - #A6B07E
Smoky Rose - #8B635C
Firey Teracotta - #D1603D

*/
.container {
  width: 100%;
  /*max-width: 1200px;*/
  margin: 0 auto;
}

.page {
  display: grid;
  grid-template-rows: auto 1fr auto; /*auto = distributes columns automatically, _fr sets a fixed size element*/
  height: 100vh; /*__vh = percentage of viewport height*/
	background-color: #14591D;
}

.main {
  padding: 25px;
  /*
  gap --> space between grid items
  padding --> space inside elements
  margin --> space outside elements
  */
}

.content {
  gap: 20px;
  display: grid;
  grid-template-columns: 250px 1fr;
}


.header {
  position: sticky;
  top: 0;
  text-align: left;

  font-family: "Merriweather";
  font-size: 4em; /* pm = pixels, em/% = relative to parent element (default is 1em = 16px), rem = relative to html element --> Can also use xx-small to xx-large*/
  font-weight: bold; /*lighter, normal, bold, bolder*/
  font-style: oblique 10deg; /*normal, italic, etc*/
  text-decoration: underline; /*Can be customized*/

  color: #a6b07e
}

/*
TO-DO:

Stretch:
 - Add scalability for smaller devices
*/
</style>


