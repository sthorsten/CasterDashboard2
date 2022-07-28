<script setup lang="ts">
import { CFormInput } from '@coreui/vue';
import { useToast } from 'vue-toastification';
import { useAuthStore } from '@/store/auth';

definePageMeta({
  layout: "login"
})

const router = useRouter()
const toast = useToast()
const authStore = useAuthStore()

// Check login
if (authStore.loggedIn) {
  router.push('/dashboard/home');
}

const username = ref("")
const password = ref("")

const login = async () => {
  await authStore.login(username.value, password.value)
  if (authStore.loggedIn) {
    toast.success(`Login successful. Welcome ${authStore.user.username}!`)
    router.push("/dashboard/home")
  } else {
    toast.error("Login failed. Please check your credentials and try again.")
  }
}

</script>

<template>

  <div class="login-logo">
    <nuxt-link to="/" class="h2">
      R6 Caster Dashboard
    </nuxt-link>
  </div>

  <div class="card">

    <div class="card-body login-card-body">

      <p class="login-box-msg">
        Welcome to the R6 Caster Dashboard!
        <br>
        Please sign in to continue.
      </p>

      <div>

        <div class="input-group mb-3">
          <CFormInput v-model="username" placeholder="Username" class="form-control" />
          <div class="input-group-text">
            <FaIcon icon="fa-solid fa-user" class="form-icon text-secondary" />
          </div>
        </div>

        <div class="input-group mb-3">
          <CFormInput @keyup.enter="login" v-model="password" type="password" placeholder="Password"
            class="form-control" />
          <div class="input-group-text">
            <FaIcon icon="fa-solid fa-lock" class="form-icon text-secondary" />
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="d-grid">
              <button @click="login" class="btn btn-primary btn-block">
                <FaIcon icon="fa-solid fa-right-to-bracket" class="form-icon mr-2" />
                Sign In
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>