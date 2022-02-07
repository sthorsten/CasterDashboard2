import handleMessage from '../helper/mainSocketMessageHandler'

export const state = () => ({
  socket: null,
  connected: false,
  leagues: [],
  seasons: [],
  playdays: [],
  tournaments: [],
  sponsors: [],
  teams: []
})

export const mutations = {
  setSocket (state, socket) {
    state.socket = socket
  },
  setConnected (state, connected) {
    state.connected = connected
  },

  setLeagues (state, leagues) {
    state.leagues = leagues
  },
  setSeasons (state, seasons) {
    state.seasons = seasons
  },
  setPlaydays (state, playdays) {
    state.playdays = playdays
  },
  setTournaments (state, tournaments) {
    state.tournaments = tournaments
  },
  setSponsors (state, sponsors) {
    state.sponsors = sponsors
  },
  setTeams (state, teams) {
    state.teams = teams
  },

  updateLeague (state, league) {
    const listElem = state.leagues.findIndex(l => l.id === league.id)
    if (listElem !== -1) {
      // Copy array for reactivity
      const newState = [...state.leagues]
      newState[listElem] = league
      state.leagues = newState
    } else {
      state.leagues.push(league)
    }
  },
  updateSeason (state, season) {
    const listElem = state.seasons.findIndex(s => s.id === season.id)
    if (listElem !== -1) {
      // Copy array for reactivity
      const newState = [...state.seasons]
      newState[listElem] = season
      state.seasons = newState
    } else {
      state.seasons.push(season)
    }
  },
  updatePlayday (state, playday) {
    const listElem = state.playdays.findIndex(p => p.id === playday.id)
    if (listElem !== -1) {
      // Copy array for reactivity
      const newState = [...state.playdays]
      newState[listElem] = playday
      state.playdays = newState
    } else {
      state.playdays.push(playday)
    }
  },
  updateTournament (state, tournament) {
    const listElem = state.tournaments.findIndex(t => t.id === tournament.id)
    if (listElem !== -1) {
      // Copy array for reactivity
      const newState = [...state.tournaments]
      newState[listElem] = tournament
      state.tournaments = newState
    } else {
      state.tournaments.push(tournament)
    }
  },
  updateSponsor (state, sponsor) {
    const listElem = state.sponsors.findIndex(s => s.id === sponsor.id)
    if (listElem !== -1) {
      // Copy array for reactivity
      const newState = [...state.sponsors]
      newState[listElem] = sponsor
      state.sponsors = newState
    } else {
      state.sponsors.push(sponsor)
    }
  },
  updateTeam (state, team) {
    const listElem = state.teams.findIndex(t => t.id === team.id)
    if (listElem !== -1) {
      // Copy array for reactivity
      const newState = [...state.teams]
      newState[listElem] = team
      state.teams = newState
    } else {
      state.teams.push(team)
    }
  }

}

export const getters = {
  isConnected: (state) => {
    if (!state.socket) { return false }
    return state.socket.readyState === 1
  },
  getLeague: state => (id) => {
    return state.leagues.filter(l => l.id === id)[0]
  },
  getLeagueLogo: (_, getters) => (id, small) => {
    const league = getters.getLeague(id)
    if (!league) { return '' }
    return small ? league.logoSmall : league.logo
  },
  getSeason: state => (id) => {
    return state.seasons.filter(s => s.id === id)[0]
  },
  getSeasonByPlaydayID: (state, getters) => (playdayID) => {
    const playday = getters.getPlayday(playdayID)
    if (!playday) { return null }
    return state.seasons.filter(s => s.id === playday.season)[0]
  },
  getPlayday: state => (id) => {
    return state.playdays.filter(p => p.id === id)[0]
  },
  getTournament: state => (id) => {
    return state.tournaments.filter(t => t.id === id)[0]
  },
  getSponsor: state => (id) => {
    return state.sponsors.filter(s => s.id === id)[0]
  },
  getTeam: state => (id) => {
    return state.teams.filter(t => t.id === id)[0]
  },
  getTeamLogo: (_, getters) => (id, small) => {
    const team = getters.getTeam(id)
    if (!team) { return '' }
    return small ? team.logoSmall : team.logo
  }
}

export const actions = {
  connect ({ commit, dispatch }) {
    return new Promise((resolve, reject) => {
      const socket = new WebSocket(`${this.app.$config.wsBaseURL}/ws/main/`)
      socket.onopen = () => {
        commit('setConnected', true)
        dispatch('getInitialData')
        resolve(socket)
      }
      socket.onmessage = (event) => {
        handleMessage(event, commit)
      }
      socket.onerror = error => reject(error)
      commit('setSocket', socket)
    })
  },

  disconnect ({ state }) {
    state.socket.close()
  },

  getInitialData ({ state }) {
    const leagues = {
      method: 'get',
      model: 'League'
    }
    const seasons = {
      method: 'get',
      model: 'Season'
    }
    const playdays = {
      method: 'get',
      model: 'Playday'
    }
    const tournaments = {
      method: 'get',
      model: 'Tournament'
    }
    const sponsors = {
      method: 'get',
      model: 'Sponsor'
    }
    const teams = {
      method: 'get',
      model: 'Team'
    }

    state.socket.send(JSON.stringify(leagues))
    state.socket.send(JSON.stringify(seasons))
    state.socket.send(JSON.stringify(playdays))
    state.socket.send(JSON.stringify(tournaments))
    state.socket.send(JSON.stringify(sponsors))
    state.socket.send(JSON.stringify(teams))
  }
}
