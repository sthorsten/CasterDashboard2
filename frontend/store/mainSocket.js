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
    const socket = new WebSocket(`${this.app.$config.wsBaseURL}/ws/main/`)
    socket.onopen = () => {
      commit('setConnected', true)
      dispatch('getInitialData')
    }
    socket.onclose = () => {
      commit('setConnected', false)
      commit('setSocket', null)
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.model === 'League') {
        if (data.partition === 'full') {
          commit('setLeagues', data.data)
        }
      } else if (data.model === 'Season') {
        if (data.partition === 'full') {
          commit('setSeasons', data.data)
        }
      } else if (data.model === 'Playday') {
        if (data.partition === 'full') {
          commit('setPlaydays', data.data)
        }
      } else if (data.model === 'Tournament') {
        if (data.partition === 'full') {
          commit('setTournaments', data.data)
        }
      } else if (data.model === 'Sponsor') {
        if (data.partition === 'full') {
          commit('setSponsors', data.data)
        }
      } else if (data.model === 'Team') {
        if (data.partition === 'full') {
          commit('setTeams', data.data)
        }
      }
    }

    commit('setSocket', socket)
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
