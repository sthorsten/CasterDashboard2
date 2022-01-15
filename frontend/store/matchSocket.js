export const state = () => ({
  socket: null,
  connected: false,
  matches: [],
  mapBans: [],
  matchMaps: [],
  operatorBans: [],
  rounds: []
})

export const mutations = {
  setSocket (state, socket) {
    state.socket = socket
  },
  setConnected (state, connected) {
    state.connected = connected
  },
  setMatches (state, matches) {
    state.matches = matches
  },
  setMapBans (state, mapBans) {
    state.mapBans = mapBans
  },
  setMatchMaps (state, matchMaps) {
    state.matchMaps = matchMaps
  },
  setOperatorBans (state, operatorBans) {
    state.operatorBans = operatorBans
  },
  setRounds (state, rounds) {
    state.rounds = rounds
  }
}

export const getters = {
  isConnected: (state) => {
    if (!state.socket) { return false }
    return state.socket.readyState === 1
  },
  getMatch: state => (id) => {
    return state.matches.filter(l => l.id === id)[0]
  },
  getMapBansByMatch: state => (id) => {
    return state.mapBans.filter(s => s.match === id)[0]
  },
  getMatchMapsByMatch: state => (id) => {
    return state.matchMaps.filter(p => p.match === id)[0]
  },
  getOperatorBansByMatchMap: state => (id) => {
    return state.operatorBans.filter(t => t.matchMap === id)[0]
  },
  getRoundsByMatchMap: state => (id) => {
    return state.rounds.filter(s => s.matchMap === id)[0]
  }
}

export const actions = {
  connect ({ commit, dispatch }, matchID) {
    const socket = new WebSocket(`${this.app.$config.wsBaseURL}/ws/match/`)
    socket.onopen = () => {
      commit('setConnected', true)
      dispatch('getInitialData')
      if (matchID) {
        dispatch('getMatchMaps', matchID)
      }
    }
    socket.onclose = () => {
      commit('setConnected', false)
      commit('setSocket', null)
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.model === 'Match') {
        if (data.partition === 'full') {
          commit('setMatches', data.data)
        }
      } else if (data.model === 'MapBan') {
        if (data.partition === 'full') {
          commit('setMapBans', data.data)
        }
      } else if (data.model === 'MatchMap') {
        if (data.partition === 'full') {
          commit('setMatchMaps', data.data)
        }
      } else if (data.model === 'OperatorBan') {
        if (data.partition === 'full') {
          commit('setOperatorBans', data.data)
        }
      } else if (data.model === 'Round') {
        if (data.partition === 'full') {
          commit('setRounds', data.data)
        }
      }
    }

    commit('setSocket', socket)
  },

  disconnect ({ state }) {
    state.socket.close()
  },

  getInitialData ({ state }) {
    const matches = {
      method: 'get',
      model: 'Match'
    }
    // const mapBans = {
    //   method: 'get',
    //   model: 'MapBan'
    // }
    // const matchMaps = {
    //   method: 'get',
    //   model: 'MatchMap'
    // }
    // const operatorBans = {
    //   method: 'get',
    //   model: 'OperatorBan'
    // }
    // const rounds = {
    //   method: 'get',
    //   model: 'Round'
    // }

    state.socket.send(JSON.stringify(matches))
    // state.socket.send(JSON.stringify(mapBans))
    // state.socket.send(JSON.stringify(matchMaps))
    // state.socket.send(JSON.stringify(operatorBans))
    // state.socket.send(JSON.stringify(rounds))
  },

  getMatchMaps ({ state }, matchID) {
    const mapBans = {
      method: 'get',
      model: 'MapBan',
      query: {
        match: matchID
      }
    }
    const matchMaps = {
      method: 'get',
      model: 'MatchMap',
      query: {
        match: matchID
      }
    }

    state.socket.send(JSON.stringify(mapBans))
    state.socket.send(JSON.stringify(matchMaps))
  }
}
