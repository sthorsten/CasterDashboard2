export default function handleMessage (event, commit) {
  const data = JSON.parse(event.data)

  if (data.model === 'League') {
    if (data.partition === 'full') {
      commit('setLeagues', data.data)
    } else if (data.partition === 'single') {
      commit('updateLeague', data.data)
    }
  } else if (data.model === 'Season') {
    if (data.partition === 'full') {
      commit('setSeasons', data.data)
    } else if (data.partition === 'single') {
      commit('updateSeason', data.data)
    }
  } else if (data.model === 'Playday') {
    if (data.partition === 'full') {
      commit('setPlaydays', data.data)
    } else if (data.partition === 'single') {
      commit('updatePlayday', data.data)
    }
  } else if (data.model === 'Tournament') {
    if (data.partition === 'full') {
      commit('setTournaments', data.data)
    } else if (data.partition === 'single') {
      commit('updateTournament', data.data)
    }
  } else if (data.model === 'Sponsor') {
    if (data.partition === 'full') {
      commit('setSponsors', data.data)
    } else if (data.partition === 'single') {
      commit('updateSponsor', data.data)
    }
  } else if (data.model === 'Team') {
    if (data.partition === 'full') {
      commit('setTeams', data.data)
    } else if (data.partition === 'single') {
      commit('updateTeam', data.data)
    }
  }

  commit('setLastUpdate')
}
