<script setup lang="ts">
import { CTable, CTableHead, CTableBody, CTableRow, CTableHeaderCell, CTableDataCell } from '@coreui/vue'
import { formatLocalTime } from '@/extra/dateString'
import { useMatchDataStore } from '@/store/matchData'
import { useMainDataStore } from '@/store/mainData';

const matchDataStore = useMatchDataStore()
matchDataStore.connect()

const mainData = useMainDataStore()

const router = useRouter()
const goToMatch = (matchId: number) => {
  const url = `/dashboard/matches/${matchId}/overview`
  router.push(url)
}

</script>

<template>

  <NuxtLayout name="main">
    <MainPage title="Match List" icon="fa-solid fa-list-ol" :breadcrumbs="['Dashboard', 'Matches', 'List']">

      <CustomCard title="Recent matches">

        <CTable striped small responsive>
          <CTableHead>
            <CTableRow>
              <CTableHeaderCell scope="col">ID</CTableHeaderCell>
              <CTableHeaderCell scope="col">Name</CTableHeaderCell>
              <CTableHeaderCell scope="col">League</CTableHeaderCell>
              <CTableHeaderCell scope="col">Team Blue</CTableHeaderCell>
              <CTableHeaderCell scope="col">Team Orange</CTableHeaderCell>
              <CTableHeaderCell scope="col">Date</CTableHeaderCell>
              <CTableHeaderCell scope="col">Status</CTableHeaderCell>
              <CTableHeaderCell scope="col">Score</CTableHeaderCell>
              <CTableHeaderCell scope="col">Action</CTableHeaderCell>
            </CTableRow>
          </CTableHead>
          <CTableBody>
            <CTableRow v-for="match in matchDataStore.matches">
              <CTableHeaderCell scope="row">{{ match.id }}</CTableHeaderCell>
              <CTableDataCell>{{ match.name }}</CTableDataCell>
              <CTableDataCell>
                <LogoAndName :name="match.leagueName" :logoURL="mainData.getLeagueLogoById(match.league)" />
              </CTableDataCell>
              <CTableDataCell>
                <LogoAndName :name="match.teamBlueName" :logoURL="mainData.getTeamLogoById(match.teamBlue)" />
              </CTableDataCell>
              <CTableDataCell>
                <LogoAndName :name="match.teamOrangeName" :logoURL="mainData.getTeamLogoById(match.teamOrange)" />
              </CTableDataCell>
              <CTableDataCell>
                {{ formatLocalTime(match.date) }}
              </CTableDataCell>
              <CTableDataCell>
                <MatchStatusBadge :status="match.status" />
              </CTableDataCell>
              <CTableDataCell>{{ match.scoreBlue }} - {{ match.scoreOrange }}</CTableDataCell>
              <CTableDataCell>
                <button @click="goToMatch(match.id)" class="btn btn-primary btn-sm btn-block">
                  <FaIcon icon="fa-solid fa-arrow-right-long" class="form-icon mr-1" />
                  Go to match
                </button>
              </CTableDataCell>
            </CTableRow>
          </CTableBody>
        </CTable>

      </CustomCard>

    </MainPage>
  </NuxtLayout>

</template>