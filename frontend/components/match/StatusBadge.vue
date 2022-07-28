<script setup lang="ts">
import { MatchStatus } from '@/types/match/Match';

interface Props {
  status: MatchStatus
}

const { status } = defineProps<Props>()

const colorClass = computed(() => {
  switch (status) {
    case MatchStatus.CREATED:
      return "badge-secondary"
    case MatchStatus.MAP_BAN:
      return "badge-primary"
    case MatchStatus.PLAYING:
      return "badge-success"
    case MatchStatus.CLOSED:
      return "badge-danger"
    case MatchStatus.ARCHIVED:
      return "badge-dark"
    case MatchStatus.DUMMY:
      return "badge-light"
  }
})

</script>

<template>
  <span :class="'badge badge-pill ' + colorClass">
    {{ status }}
  </span>
</template>