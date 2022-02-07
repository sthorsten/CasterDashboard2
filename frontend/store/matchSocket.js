import handleMessage from '../helper/matchSocketMessageHandler'

export const state = () => ({
  socket: null,
  connected: false,
  lastUpdate: null,
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
  setLastUpdate (state) {
    state.lastUpdate = Date.now()
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
  },

  updateMatch (state, match) {
    const listElem = state.matches.findIndex(m => m.id === match.id)
    if (listElem !== -1) {
      // Copy array for reactivity
      const newState = [...state.matches]
      newState[listElem] = match
      state.matches = newState
    } else {
      state.matches.push(match)
    }
  },
  updateMapBan (state, mapBan) {
    const listElem = state.mapBans.findIndex(m => m.id === mapBan.id)
    if (listElem !== -1) {
      state.mapBans[listElem] = mapBan
    } else {
      state.mapBans.push(mapBan)
    }
  },
  updateMatchMap (state, matchMap) {
    const listElem = state.matchMaps.findIndex(m => m.id === matchMap.id)
    if (listElem !== -1) {
      state.matchMaps[listElem] = matchMap
    } else {
      state.matchMaps.push(matchMap)
    }
  },
  updateOperatorBan (state, operatorBan) {
    const listElem = state.operatorBans.findIndex(o => o.id === operatorBan.id)
    if (listElem !== -1) {
      state.operatorBans[listElem] = operatorBan
    } else {
      state.operatorBans.push(operatorBan)
    }
  },
  updateRound (state, round) {
    const listElem = state.rounds.findIndex(r => r.id === round.id)
    if (listElem !== -1) {
      state.rounds[listElem] = round
    } else {
      state.rounds.push(round)
    }
  }
}

export const getters = {
  isConnected: (state) => {
    if (!state.socket) { return false }
    return state.socket.readyState === 1
  },
  getMatch: state => (id) => {
    return state.matches.filter(m => m.id === id)[0]
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
    return new Promise((resolve, reject) => {
      const socket = new WebSocket(`${this.app.$config.wsBaseURL}/ws/match/`)
      socket.onopen = () => {
        commit('setConnected', true)
        dispatch('getInitialData')
        if (matchID) {
          dispatch('getMatchMaps', matchID)
        }
        resolve(socket)
      }
      socket.onmessage = (event) => {
        handleMessage(event, commit)
      }
      socket.onerror = error => reject(error)
      socket.onclose = () => {
        commit('setConnected', false)
        commit('setSocket', null)
      }
      commit('setSocket', socket)
    })
  },

  disconnect ({ state }) {
    state.socket.close()
  },

  getInitialData ({ state }) {
    const matches = {
      method: 'get',
      model: 'Match'
    }

    state.socket.send(JSON.stringify(matches))
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
    const operatorBans = {
      method: 'get',
      model: 'OperatorBan',
      query: {
        matchMap__match: matchID
      }
    }
    const rounds = {
      method: 'get',
      model: 'Round',
      query: {
        matchMap__match: matchID
      }
    }

    state.socket.send(JSON.stringify(mapBans))
    state.socket.send(JSON.stringify(matchMaps))
    state.socket.send(JSON.stringify(operatorBans))
    state.socket.send(JSON.stringify(rounds))
  }
}
