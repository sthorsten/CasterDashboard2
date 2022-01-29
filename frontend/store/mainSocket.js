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
    state.leagues[listElem] = league
  },
  updateSeason (state, season) {
    const listElem = state.seasons.findIndex(s => s.id === season.id)
    state.seasons[listElem] = season
  },
  updatePlayday (state, playday) {
    const listElem = state.playdays.findIndex(p => p.id === playday.id)
    state.playdays[listElem] = playday
  },
  updateTournament (state, tournament) {
    const listElem = state.tournaments.findIndex(t => t.id === tournament.id)
    state.tournaments[listElem] = tournament
  },
  updateSponsor (state, sponsor) {
    const listElem = state.sponsors.findIndex(s => s.id === sponsor.id)
    state.sponsors[listElem] = sponsor
  },
  updateTeam (state, team) {
    const listElem = state.teams.findIndex(t => t.id === team.id)
    state.teams[listElem] = team
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
