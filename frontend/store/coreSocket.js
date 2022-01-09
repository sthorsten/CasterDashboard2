export const state = () => ({
  socket: null,
  connected: false,
  notifications: [],
  mapPools: [],
  maps: [],
  bombSpots: [],
  operators: []
})

export const mutations = {
  setSocket (state, socket) {
    state.socket = socket
  },
  setConnected (state, connected) {
    state.connected = connected
  },
  setNotifications (state, notifications) {
    state.notifications = notifications
  },
  setMapPools (state, mapPools) {
    state.mapPools = mapPools
  },
  setMaps (state, maps) {
    state.maps = maps
  },
  setBombSpots (state, bombSpots) {
    state.bombSpots = bombSpots
  },
  setOperators (state, operators) {
    state.operators = operators
  }
}

export const getters = {
  isConnected: (state) => {
    if (!state.socket) { return false }
    return state.socket.readyState === 1
  },
  getMapPool: state => (name) => {
    return state.maps.filter(m => m.name === name)[0]
  },
  getMap: state => (id) => {
    return state.maps.filter(m => m.id === id)[0]
  },
  getBombSpotsByMap: state => (mapId) => {
    return state.bombSpots.filter(b => b.map === mapId)
  },
  getOperatorsBySide: state => (side) => {
    return state.operators.filter(o => o.side === side)
  }
}

export const actions = {
  connect ({ commit, dispatch }) {
    const socket = new WebSocket('wss://dev.thorshero.de/ws/core/')
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
      if (data.model === 'Notification') {
        if (data.partition === 'full') {
          commit('setNotifications', data.data)
        }
      } else if (data.model === 'MapPool') {
        if (data.partition === 'full') {
          commit('setMapPools', data.data)
        }
      } else if (data.model === 'Map') {
        if (data.partition === 'full') {
          commit('setMaps', data.data)
        }
      } else if (data.model === 'BombSpot') {
        if (data.partition === 'full') {
          commit('setBombSpots', data.data)
        }
      } else if (data.model === 'Operator') {
        if (data.partition === 'full') {
          commit('setOperators', data.data)
        }
      }
    }

    commit('setSocket', socket)
  },

  disconnect ({ state }) {
    state.socket.close()
  },

  getInitialData ({ state }) {
    const notifications = {
      method: 'get',
      model: 'Notification'
    }
    const mapPools = {
      method: 'get',
      model: 'MapPool'
    }
    const maps = {
      method: 'get',
      model: 'Map'
    }
    const bombSpots = {
      method: 'get',
      model: 'BombSpot'
    }
    const operators = {
      method: 'get',
      model: 'Operator'
    }

    state.socket.send(JSON.stringify(notifications))
    state.socket.send(JSON.stringify(mapPools))
    state.socket.send(JSON.stringify(maps))
    state.socket.send(JSON.stringify(bombSpots))
    state.socket.send(JSON.stringify(operators))
  }
}
