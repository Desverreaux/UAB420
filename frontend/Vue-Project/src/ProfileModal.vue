<!--Profile Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">

      <header class="header">
        <div class="modal_title">User Profile</div>
        <button class="close_button" @click="$emit('close')">X</button>
      </header>
      
      <div class="main">
        <p v-if="logged_in" class="status_message"> Logged in as {{ logged_in_user }} </p>

        <p v-if="error_message" class="error_message"> {{ error_message }} </p>

        <input v-model="user_name" placeholder="Username"/>
        <input v-model="user_password" type="password" placeholder="Password"/>

        <div class="button_row">

          <button class="update_profile" @click="user_login">Login</button>
          <button class="update_profile" @click="create_user">Create User</button>

        </div>
        
      </div>
      
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"

export default {
    props: ["show"],
    emits: ["close"], 
    components: { Modal }, 

  data() {
    return {
      user_name: "",
      user_password: "",

      logged_in: false,
      logged_in_user: "",
      error_message: ""
    }
  },

  methods: {
    async user_login() {
      this.error_message = ""

      try {
        const response = await fetch(
          `/api/login?username=${encodeURIComponent(this.user_name)}&password=${encodeURIComponent(this.user_password)}`,
        {
          method: "POST"
        }
        )

        if (!response.ok) {
          throw new Error(`Login failed. Status: ${response.status}`)
        }

        await response.json()

        this.logged_in = true
        this.logged_in_user = this.user_name

        this.user_password = ""

      } catch (err) {
        console.error("Login failed: ", err)
        this.error_message = "Login Failed. Check your username and password."
      }   
    },

    async create_user() {
      this.error_message = ""

      try {
        const response = await fetch(
          `/api/createUser?username=${encodeURIComponent(this.user_name)}&password=${encodeURIComponent(this.user_password)}`,

        {
          method: "POST"
        }
        )
        
        if (!response.ok) {
          throw new Error(`Create user failed. Status: ${response.status}`)
        }

        await response.json()

        this.logged_in = true
        this.logged_in_user = this.user_name

        this.user_password = ""

      } catch (err) {
        console.error("Create user failed: ", err)
        this.error_message = "Could not create user. Username may already exist."
      }
    }
  }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;

  padding: 0.5rem 1rem 0.25rem 1rem;
}

.modal_title {
  font-size: 3rem;
  color: #0E2F15;
  cursor: default;

  margin: 0;
  line-height: 1;
}

.close_button {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #0E2F15;
  font-weight: bold;
  cursor: pointer;

  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
}

.main {
  display: flex;
  flex-direction: column;
  cursor: default;
  align-items: center;
}

.button_row {
  display: flex;
  gap: 0.75rem;
}

.update_profile {
  border-radius: 25px;
  background-color: #A6B07E;
  color: #0E2F15;
  padding: 0.5rem 1rem;
  border: 2px solid #0E2F15;
  cursor: pointer;
}

.update_profile:hover {
  background-color: #7d855f;
}

.status_message {
  color: #0E2F15;
  font-weight: bold;
}

.error_message {
  color: #7a0000;
  font-weight: bold;
}
</style>