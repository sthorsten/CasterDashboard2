<script setup lang="ts">
import { useToast } from 'vue-toastification';
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore()
authStore.logout()

const router = useRouter()
router.push('/login')

const toast = useToast()
toast.success('Logout successful.')

</script>

<template>
</template>